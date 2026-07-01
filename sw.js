// PWA Service Worker - enables install to home screen
self.addEventListener('install', function(e){
  self.skipWaiting();
});

self.addEventListener('activate', function(e){
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', function(e){
  e.respondWith(
    caches.match(e.request).then(function(r){
      return r || fetch(e.request).then(function(resp){
        if(resp.ok){
          var clone = resp.clone();
          caches.open('jingdu-v1').then(function(c){ c.put(e.request, clone); });
        }
        return resp;
      });
    })
  );
});
