<?php
// amiibo棚 API: ユーザー登録/ログインとコレクションの保存（SQLite）
// データベースは公開ディレクトリの外に置く（config.php の AMIIBO_DB、無ければ ../amiibo-shelf-data/）
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

const COOKIE = 'amiibo_session';
const SESSION_DAYS = 365;
const MAX_STATE_BYTES = 2_000_000;

if (is_file(__DIR__ . '/config.php')) require __DIR__ . '/config.php';
$dbPath = defined('AMIIBO_DB') ? AMIIBO_DB : dirname(__DIR__) . '/amiibo-shelf-data/amiibo.sqlite';

function out(int $code, array $body): never { http_response_code($code); echo json_encode($body, JSON_UNESCAPED_UNICODE); exit; }
function fail(int $code, string $msg): never { out($code, ['ok' => false, 'error' => $msg]); }

// 他サイトからのフォーム送信対策: 書き込み系はカスタムヘッダ必須（クロスオリジンだとプリフライトで止まる）
$action = $_GET['action'] ?? '';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && ($_SERVER['HTTP_X_AMIIBO'] ?? '') !== '1') fail(400, 'bad request');

if (!is_dir(dirname($dbPath))) mkdir(dirname($dbPath), 0700, true);
$db = new PDO('sqlite:' . $dbPath, null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
$db->exec('PRAGMA journal_mode=WAL; PRAGMA busy_timeout=3000;');
$db->exec('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT UNIQUE COLLATE NOCASE NOT NULL, pass TEXT NOT NULL, state TEXT, updated_at TEXT, created_at TEXT NOT NULL)');
$db->exec('CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY, user_id INTEGER NOT NULL, expires_at INTEGER NOT NULL)');
$db->exec('CREATE TABLE IF NOT EXISTS attempts (ip TEXT NOT NULL, at INTEGER NOT NULL)');

function body(): array { $j = json_decode(file_get_contents('php://input') ?: '{}', true); return is_array($j) ? $j : []; }
function now(): string { return gmdate('Y-m-d\TH:i:s\Z'); }

function currentUser(PDO $db): ?array {
  $t = $_COOKIE[COOKIE] ?? '';
  if (!preg_match('/^[a-f0-9]{64}$/', $t)) return null;
  $st = $db->prepare('SELECT u.id, u.name, u.updated_at FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token = ? AND s.expires_at > ?');
  $st->execute([hash('sha256', $t), time()]);
  return $st->fetch() ?: null;
}
function startSession(PDO $db, int $uid): void {
  $t = bin2hex(random_bytes(32));
  $exp = time() + SESSION_DAYS * 86400;
  $db->prepare('INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)')->execute([hash('sha256', $t), $uid, $exp]);
  setcookie(COOKIE, $t, ['expires' => $exp, 'path' => '/', 'secure' => true, 'httponly' => true, 'samesite' => 'Lax']);
}
function rateLimit(PDO $db): void {
  $ip = $_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
  $db->prepare('DELETE FROM attempts WHERE at < ?')->execute([time() - 900]);
  $st = $db->prepare('SELECT COUNT(*) FROM attempts WHERE ip = ?'); $st->execute([$ip]);
  if ((int)$st->fetchColumn() >= 20) fail(429, '試行回数が多すぎます。15分ほど待ってからやり直してください');
  $db->prepare('INSERT INTO attempts (ip, at) VALUES (?, ?)')->execute([$ip, time()]);
}

switch ($action) {
  case 'me':
    $u = currentUser($db);
    out(200, ['ok' => true, 'user' => $u ? ['name' => $u['name'], 'updatedAt' => $u['updated_at']] : null]);

  case 'register': {
    rateLimit($db);
    $b = body(); $name = trim((string)($b['name'] ?? '')); $pass = (string)($b['pass'] ?? '');
    if (!preg_match('/^[\p{L}\p{N}_.\-]{2,32}$/u', $name)) fail(400, 'ユーザー名は2〜32文字（記号は _ . - のみ）にしてください');
    if (strlen($pass) < 6) fail(400, 'パスワードは6文字以上にしてください');
    try {
      $db->prepare('INSERT INTO users (name, pass, created_at) VALUES (?, ?, ?)')->execute([$name, password_hash($pass, PASSWORD_DEFAULT), now()]);
    } catch (PDOException) { fail(409, 'そのユーザー名は使われています'); }
    startSession($db, (int)$db->lastInsertId());
    out(200, ['ok' => true, 'user' => ['name' => $name, 'updatedAt' => null]]);
  }

  case 'login': {
    rateLimit($db);
    $b = body();
    $st = $db->prepare('SELECT id, name, pass, updated_at FROM users WHERE name = ?'); $st->execute([trim((string)($b['name'] ?? ''))]);
    $u = $st->fetch();
    if (!$u || !password_verify((string)($b['pass'] ?? ''), $u['pass'])) fail(401, 'ユーザー名かパスワードが違います');
    startSession($db, (int)$u['id']);
    out(200, ['ok' => true, 'user' => ['name' => $u['name'], 'updatedAt' => $u['updated_at']]]);
  }

  case 'logout':
    if (preg_match('/^[a-f0-9]{64}$/', $_COOKIE[COOKIE] ?? '')) $db->prepare('DELETE FROM sessions WHERE token = ?')->execute([hash('sha256', $_COOKIE[COOKIE])]);
    setcookie(COOKIE, '', ['expires' => 1, 'path' => '/', 'secure' => true, 'httponly' => true, 'samesite' => 'Lax']);
    out(200, ['ok' => true]);

  case 'load': {
    $u = currentUser($db) ?? fail(401, 'ログインしてください');
    $st = $db->prepare('SELECT state, updated_at FROM users WHERE id = ?'); $st->execute([$u['id']]);
    $r = $st->fetch();
    out(200, ['ok' => true, 'state' => $r['state'] ? json_decode($r['state'], true) : null, 'updatedAt' => $r['updated_at']]);
  }

  case 'save': {
    $u = currentUser($db) ?? fail(401, 'ログインしてください');
    $raw = file_get_contents('php://input') ?: '';
    if (strlen($raw) > MAX_STATE_BYTES) fail(413, 'データが大きすぎます');
    $b = json_decode($raw, true);
    if (!is_array($b) || !is_array($b['state'] ?? null)) fail(400, 'bad state');
    $t = now();
    $db->prepare('UPDATE users SET state = ?, updated_at = ? WHERE id = ?')->execute([json_encode($b['state'], JSON_UNESCAPED_UNICODE), $t, $u['id']]);
    out(200, ['ok' => true, 'updatedAt' => $t]);
  }

  default:
    fail(404, 'unknown action');
}
