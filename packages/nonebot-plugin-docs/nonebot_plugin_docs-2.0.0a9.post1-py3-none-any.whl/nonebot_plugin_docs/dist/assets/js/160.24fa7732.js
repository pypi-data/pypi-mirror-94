(window.webpackJsonp=window.webpackJsonp||[]).push([[160],{410:function(n,e,t){"use strict";t.r(e),t.d(e,"register",(function(){return o})),t.d(e,"unregister",(function(){return c}));var r;function o(n,e){void 0===e&&(e={});var t=e.registrationOptions;void 0===t&&(t={}),delete e.registrationOptions;var o=function(n){for(var t=[],r=arguments.length-1;r-- >0;)t[r]=arguments[r+1];e&&e[n]&&e[n].apply(e,t)};"serviceWorker"in navigator&&r.then((function(){Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/))?(!function(n,e,t){fetch(n).then((function(r){404===r.status?(e("error",new Error("Service worker not found at "+n)),c()):-1===r.headers.get("content-type").indexOf("javascript")?(e("error",new Error("Expected "+n+" to have javascript content-type, but received "+r.headers.get("content-type"))),c()):a(n,e,t)})).catch((function(n){return i(e,n)}))}(n,o,t),navigator.serviceWorker.ready.then((function(n){o("ready",n)}))):(a(n,o,t),navigator.serviceWorker.ready.then((function(n){o("ready",n)})))}))}function i(n,e){navigator.onLine||n("offline"),n("error",e)}function a(n,e,t){navigator.serviceWorker.register(n,t).then((function(n){e("registered",n),n.waiting?e("updated",n):n.onupdatefound=function(){e("updatefound",n);var t=n.installing;t.onstatechange=function(){"installed"===t.state&&(navigator.serviceWorker.controller?e("updated",n):e("cached",n))}}})).catch((function(n){return i(e,n)}))}function c(){"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(n){n.unregister()}))}"undefined"!=typeof window&&(r="undefined"!=typeof Promise?new Promise((function(n){return window.addEventListener("load",n)})):{then:function(n){return window.addEventListener("load",n)}})}}]);