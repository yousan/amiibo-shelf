// アプリ本体をキャッシュしてオフラインでも開けるようにする（amiibo一覧はlocalStorageに保存済み）
const C = 'amiibo-shelf-v1';
const FILES = ['./', './index.html', './manifest.webmanifest', './icon.svg'];
self.addEventListener('install', e => e.waitUntil(caches.open(C).then(c => c.addAll(FILES))));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k))))));
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (u.origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(r => { const rc = r.clone(); caches.open(C).then(c => c.put(e.request, rc)); return r; }).catch(() => caches.match(e.request)));
});
