# amiibo棚

amiibo を NFC でスキャンしてコレクション管理する、日本語・無料・登録不要のWebアプリ。

- ログイン対応版（端末間で同期）: https://l4tp.org/amiibo/
- 端末内保存のみ版: https://yousan.github.io/amiibo-shelf/

- Android の Chrome: amiibo をかざして所持登録（Web NFC）
  - はじめてのamiiboは一覧から1回選ぶ → 次からはタグIDで自動判定
- iPhone など: 一覧からタップで登録
- シリーズ別の達成率、ほしいものリスト、JSONでバックアップ
- ログインなしなら端末のブラウザ内（localStorage）にだけ保存。ログインするとサーバー（PHP + SQLite）に保存して複数端末で同期

## 設置（ログイン対応版）

`api.php` が動くPHP 8.1+（pdo_sqlite）のサーバーに全ファイルを置く。DBの場所は `config.php` で公開ディレクトリの外を指定する:

```php
<?php define('AMIIBO_DB', '/path/outside/public_html/amiibo.sqlite');
```

amiibo一覧・画像は [AmiiboAPI](https://amiiboapi.org/)（非公式）から取得しています。
amiibo は任天堂の商標です。本アプリは非公式の個人制作物です。

## Androidアプリ版

https://github.com/yousan/amiibo-shelf/releases/tag/android-latest から `amiibo-shelf.apk` を入れる（提供元不明のアプリの許可が要る）。

- 中身は https://l4tp.org/amiibo/ を表示するだけのアプリ（`android/`）。データはWeb版のアカウントと共通
- NFC はアプリ側で読む。amiibo（NTAG215）の 21〜22 ページにある amiibo ID を読むので、初めてのamiiboでも一覧から選ばずに登録される
- `android/` を変えて main に入れると GitHub Actions が APK を作り直して上のリリースを差し替える
