<?php
// amiibo棚 管理用CLI（写真の判別結果をアカウントに入れる）。公開ディレクトリには置かず、DBと同じ場所に置いて ssh で実行する
//   php admin.php pending                      判別待ちの写真一覧
//   php admin.php add <ユーザー名> <amiiboID>[=メモ] ...   所持に追加（同じものは増やさない）
//   php admin.php done <写真ID> ... [--note=メモ]  写真を「判別済み」にする
//   php admin.php owned <ユーザー名>             所持一覧
declare(strict_types=1);
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }

$dbPath = getenv('AMIIBO_DB') ?: __DIR__ . '/amiibo.sqlite';
$db = new PDO('sqlite:' . $dbPath, null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
$db->exec('PRAGMA busy_timeout=3000;');
function now(): string { $t = microtime(true); return gmdate('Y-m-d\TH:i:s', (int)$t) . sprintf('.%03dZ', (int)(fmod($t, 1) * 1000)); }
function user(PDO $db, string $name): array {
  $st = $db->prepare('SELECT id, name, state FROM users WHERE name = ?'); $st->execute([$name]);
  return $st->fetch() ?: exit("ユーザーが見つかりません: $name\n");
}

$args = array_slice($argv, 1);
$cmd = array_shift($args) ?? '';
switch ($cmd) {
  case 'pending':
    foreach ($db->query("SELECT p.id, u.name, p.file, p.created_at FROM photos p JOIN users u ON u.id = p.user_id WHERE p.status = 'pending' ORDER BY p.id") as $r)
      echo "{$r['id']}\t{$r['name']}\t{$r['created_at']}\t" . __DIR__ . "/photos/{$r['file']}\n";
    break;

  case 'add': {
    $u = user($db, array_shift($args) ?? '');
    $s = json_decode($u['state'] ?? 'null', true) ?: ['owned' => [], 'uids' => [], 'wish' => [], 'log' => []];
    foreach (['owned', 'uids', 'wish'] as $k) $s[$k] = (array)($s[$k] ?? []);
    $added = [];
    foreach ($args as $a) {
      [$id, $memo] = array_pad(explode('=', $a, 2), 2, null);
      if (!preg_match('/^[0-9a-f]{16}$/', $id)) exit("amiiboIDは16桁の16進数: $id\n");
      if (empty($s['owned'][$id]['count'])) { $s['owned'][$id] = ['count' => 1, 'uids' => [], 'addedAt' => now()] + ($memo ? ['memo' => $memo] : []); $added[] = $id; }
      elseif ($memo && empty($s['owned'][$id]['memo'])) $s['owned'][$id]['memo'] = $memo;
      unset($s['wish'][$id]);
    }
    foreach (['owned', 'uids', 'wish'] as $k) if (!$s[$k]) $s[$k] = new stdClass;
    $s['log'][] = date('Y/n/j H:i:s') . '  写真から登録: ' . count($added) . '種類';
    $db->prepare('UPDATE users SET state = ?, updated_at = ? WHERE id = ?')->execute([json_encode($s, JSON_UNESCAPED_UNICODE), now(), $u['id']]);
    echo "追加 " . count($added) . " 種類（指定 " . count($args) . "）: " . implode(' ', $added) . "\n";
    break;
  }

  case 'done': {
    $note = null; $ids = [];
    foreach ($args as $a) str_starts_with($a, '--note=') ? $note = substr($a, 7) : $ids[] = (int)$a;
    $st = $db->prepare("UPDATE photos SET status = 'done', note = COALESCE(?, note) WHERE id = ?");
    foreach ($ids as $id) $st->execute([$note, $id]);
    echo "判別済みにした: " . implode(' ', $ids) . "\n";
    break;
  }

  case 'owned': {
    $u = user($db, array_shift($args) ?? '');
    $s = json_decode($u['state'] ?? 'null', true) ?: [];
    foreach (($s['owned'] ?? []) as $id => $o) echo "$id\t" . ($o['count'] ?? 0) . "\t" . ($o['memo'] ?? '') . "\n";
    break;
  }

  default:
    echo "usage: php admin.php pending | add <user> <id>[=memo]... | done <photoId>... [--note=...] | owned <user>\n";
}
