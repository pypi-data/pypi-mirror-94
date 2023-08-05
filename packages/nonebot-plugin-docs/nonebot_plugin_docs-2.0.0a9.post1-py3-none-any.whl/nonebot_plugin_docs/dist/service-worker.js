/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "2.0.0a7/advanced/export-and-require.html",
    "revision": "10d0edb9ea68df34f70b87a231492716"
  },
  {
    "url": "2.0.0a7/advanced/index.html",
    "revision": "ddb3bd5c3d7d58d6cec048ed4cac4b9b"
  },
  {
    "url": "2.0.0a7/advanced/permission.html",
    "revision": "23e19354fd0e964d5063525c352e0d1f"
  },
  {
    "url": "2.0.0a7/advanced/publish-plugin.html",
    "revision": "fbed2ca360e4cba61aff47723583aecd"
  },
  {
    "url": "2.0.0a7/advanced/runtime-hook.html",
    "revision": "190b03ec3c3bcca3266df9b3fcd8dced"
  },
  {
    "url": "2.0.0a7/advanced/scheduler.html",
    "revision": "b46cf7ff69d61015889b293c5ca7d48b"
  },
  {
    "url": "2.0.0a7/api/adapters/cqhttp.html",
    "revision": "b6fb51f8c88465d2a42dbe7df8558d92"
  },
  {
    "url": "2.0.0a7/api/adapters/ding.html",
    "revision": "3134417cf932b4beaeb00ce01c39f2a1"
  },
  {
    "url": "2.0.0a7/api/adapters/index.html",
    "revision": "88fe9a3028dd4adff73ccc302eed22f0"
  },
  {
    "url": "2.0.0a7/api/config.html",
    "revision": "82971d5358473aa4a048c1008516269d"
  },
  {
    "url": "2.0.0a7/api/drivers/fastapi.html",
    "revision": "0bab0f4c1174aa6ee3c74419c60bbb2c"
  },
  {
    "url": "2.0.0a7/api/drivers/index.html",
    "revision": "f42ca97a825825d8e32cf9fcd79efb24"
  },
  {
    "url": "2.0.0a7/api/exception.html",
    "revision": "9dfa20f68da0ae93ce97235e924b8287"
  },
  {
    "url": "2.0.0a7/api/index.html",
    "revision": "6249438ac8455790a0b493c506924d7e"
  },
  {
    "url": "2.0.0a7/api/log.html",
    "revision": "f4ce894183cbd723b186b82551ded95e"
  },
  {
    "url": "2.0.0a7/api/matcher.html",
    "revision": "4df43d14f853841a71ae3d4ef36a0a8f"
  },
  {
    "url": "2.0.0a7/api/message.html",
    "revision": "cf92883125ba8359bf45ff49bf0abdfe"
  },
  {
    "url": "2.0.0a7/api/nonebot.html",
    "revision": "eae5d0e663c5158a1b816043697a26e4"
  },
  {
    "url": "2.0.0a7/api/permission.html",
    "revision": "65b62f1f9e527fa37311d8ce1f5e61ec"
  },
  {
    "url": "2.0.0a7/api/plugin.html",
    "revision": "b10ed7bcc5728519853b4d37b7bb486d"
  },
  {
    "url": "2.0.0a7/api/rule.html",
    "revision": "a8d00e842d6081e9bd65b9c310122ef7"
  },
  {
    "url": "2.0.0a7/api/typing.html",
    "revision": "9f3ec594feeccb126d67cd9729472e3a"
  },
  {
    "url": "2.0.0a7/api/utils.html",
    "revision": "46e578fcd6175d30b5d2239fad050e9e"
  },
  {
    "url": "2.0.0a7/guide/basic-configuration.html",
    "revision": "f023565d090c24089ddc02390e8d2f09"
  },
  {
    "url": "2.0.0a7/guide/creating-a-handler.html",
    "revision": "a57bfebdd84953beeb137478237cd2ea"
  },
  {
    "url": "2.0.0a7/guide/creating-a-matcher.html",
    "revision": "1961fd56978e3a46e67f87979abfe1b5"
  },
  {
    "url": "2.0.0a7/guide/creating-a-plugin.html",
    "revision": "42e0c32046d5158d40944625e81ac642"
  },
  {
    "url": "2.0.0a7/guide/creating-a-project.html",
    "revision": "96a34b5af9cbfaa5bb08c20bb74fdf92"
  },
  {
    "url": "2.0.0a7/guide/end-or-start.html",
    "revision": "c1021cc9b8c05be9fd7c8e86193d806a"
  },
  {
    "url": "2.0.0a7/guide/getting-started.html",
    "revision": "d9a22f41262ce008534252b0d9877012"
  },
  {
    "url": "2.0.0a7/guide/index.html",
    "revision": "0b18fe916edae9b2d0bc9bd7e59db764"
  },
  {
    "url": "2.0.0a7/guide/installation.html",
    "revision": "d495098113293fa9f7f4a741a414d405"
  },
  {
    "url": "2.0.0a7/guide/loading-a-plugin.html",
    "revision": "b7a3c49349094d4ad471675dd6179866"
  },
  {
    "url": "2.0.0a7/index.html",
    "revision": "58b1e33baa432d70fe156d240a6bd41b"
  },
  {
    "url": "2.0.0a8.post2/advanced/export-and-require.html",
    "revision": "bdc0b83e08fe6ff53f4eb5b3812bfeda"
  },
  {
    "url": "2.0.0a8.post2/advanced/index.html",
    "revision": "9c973fdec6aee0be088b9c7ef4f5164b"
  },
  {
    "url": "2.0.0a8.post2/advanced/overloaded-handlers.html",
    "revision": "8fee36c6aa73b6ea23dd47084e634d76"
  },
  {
    "url": "2.0.0a8.post2/advanced/permission.html",
    "revision": "d0bfc95317338924d2f0168991d7956d"
  },
  {
    "url": "2.0.0a8.post2/advanced/publish-plugin.html",
    "revision": "b38de5fb0cdde5138a66e949ec2ee548"
  },
  {
    "url": "2.0.0a8.post2/advanced/runtime-hook.html",
    "revision": "143f760376a551c9cf6b7a2deb9e83da"
  },
  {
    "url": "2.0.0a8.post2/advanced/scheduler.html",
    "revision": "f2bb9823d75409f977cbdd28810aefbc"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/cqhttp.html",
    "revision": "c6129efaaac0628bb53c40581218f436"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/ding.html",
    "revision": "0a7a9b54d19a14bc9c74d01f1ce7f27b"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/index.html",
    "revision": "ff3836818119c983ceb216e2ee755d7c"
  },
  {
    "url": "2.0.0a8.post2/api/config.html",
    "revision": "d5ffd830d4608eaf2218292f77af2029"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/fastapi.html",
    "revision": "95c84b24ae9e2631e04da716a665b93e"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/index.html",
    "revision": "8c069954d217c1f211280a5ea0d8f93b"
  },
  {
    "url": "2.0.0a8.post2/api/exception.html",
    "revision": "4289a8afc13f1abad5e44e03240235f1"
  },
  {
    "url": "2.0.0a8.post2/api/index.html",
    "revision": "0bb654fddc2a2c75ce364a66fa5d5694"
  },
  {
    "url": "2.0.0a8.post2/api/log.html",
    "revision": "23cdff315a469c45d8549847c96d3031"
  },
  {
    "url": "2.0.0a8.post2/api/matcher.html",
    "revision": "35c0676948546cdf367c179a1ef44b9e"
  },
  {
    "url": "2.0.0a8.post2/api/message.html",
    "revision": "0eb8da0af7c305c6148683150888db01"
  },
  {
    "url": "2.0.0a8.post2/api/nonebot.html",
    "revision": "2934d8f744ff24648556bc269dce1a98"
  },
  {
    "url": "2.0.0a8.post2/api/permission.html",
    "revision": "e4a7e63ed01c7e4a49e4b43d578cb351"
  },
  {
    "url": "2.0.0a8.post2/api/plugin.html",
    "revision": "dd5dfa0358b9e019b3a80d2dd82e8a5a"
  },
  {
    "url": "2.0.0a8.post2/api/rule.html",
    "revision": "d88cb0ca988a6099cd4746056662d8c5"
  },
  {
    "url": "2.0.0a8.post2/api/typing.html",
    "revision": "29c752104da3f3b3a58ca0162ca56c25"
  },
  {
    "url": "2.0.0a8.post2/api/utils.html",
    "revision": "348bddc82e2bb59d234fa79a71e43833"
  },
  {
    "url": "2.0.0a8.post2/guide/basic-configuration.html",
    "revision": "543e7ebd54d08a2bc3670f2057639a67"
  },
  {
    "url": "2.0.0a8.post2/guide/cqhttp-guide.html",
    "revision": "088bb8015d6a8c57d49fa47bbba2194d"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-handler.html",
    "revision": "3e3e1c81bf67b5d65537aff607959de8"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-matcher.html",
    "revision": "c7d661eeb5fc823d7975eac80afbaf56"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-plugin.html",
    "revision": "5c03094ea5feb409ead53beb549a7459"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-project.html",
    "revision": "2d47927952d7a1a2955dafb5488839ff"
  },
  {
    "url": "2.0.0a8.post2/guide/ding-guide.html",
    "revision": "93e8ab99a46224af465a7134ac05b911"
  },
  {
    "url": "2.0.0a8.post2/guide/end-or-start.html",
    "revision": "eb4f0197f0ff1632d93b5e3833162bf9"
  },
  {
    "url": "2.0.0a8.post2/guide/getting-started.html",
    "revision": "6e320dc9af39162c5eed07a316b2c998"
  },
  {
    "url": "2.0.0a8.post2/guide/index.html",
    "revision": "b243f3d8b5202c5ae00e4a575e493419"
  },
  {
    "url": "2.0.0a8.post2/guide/installation.html",
    "revision": "ae659b07b55c7c1347bfdd417a8d8531"
  },
  {
    "url": "2.0.0a8.post2/guide/loading-a-plugin.html",
    "revision": "bc0cb266e0579fe46179c43fbaaf0d9b"
  },
  {
    "url": "2.0.0a8.post2/index.html",
    "revision": "bac7eed18d545c64a9770bfa5e669129"
  },
  {
    "url": "404.html",
    "revision": "a49aa3aa33199561169560053b0c6388"
  },
  {
    "url": "advanced/export-and-require.html",
    "revision": "e165ab952c5a88fa50803413985be8ae"
  },
  {
    "url": "advanced/index.html",
    "revision": "a232969ca2c01d08a4cf3384cd3170eb"
  },
  {
    "url": "advanced/overloaded-handlers.html",
    "revision": "a3c3e145c16a612dfb37e50867fb857a"
  },
  {
    "url": "advanced/permission.html",
    "revision": "bc909fc20f5c4b4ac0949815cb772c03"
  },
  {
    "url": "advanced/publish-plugin.html",
    "revision": "69d4d3cd2de4cb79610628f164eb50ea"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "a54b6298f439083d80ae72853febcb90"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "dcbc1004621b70381f4f640b85abd5d9"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "fe2a1e35ae184a62ec2d88b97f43f085"
  },
  {
    "url": "api/adapters/ding.html",
    "revision": "3eec826cb93d16e443dafd48d5beef14"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "44e7a51613cc4ab3d21acf4cf4108d96"
  },
  {
    "url": "api/adapters/mirai.html",
    "revision": "abc5c21feb7737c213b5972bedd8606e"
  },
  {
    "url": "api/config.html",
    "revision": "fff5f3966a70524c3f1eafc4a8107f51"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "9897463ad9c29322575208d9d56e173d"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "50c7444b842b66c32d426409beff5e95"
  },
  {
    "url": "api/exception.html",
    "revision": "251970fe2169da574734d1b3cbaefbd2"
  },
  {
    "url": "api/index.html",
    "revision": "8399412d02ec6f6a631fdc0ed9c862bd"
  },
  {
    "url": "api/log.html",
    "revision": "9f447f31f4989ef1e7dc35bfa71530dd"
  },
  {
    "url": "api/matcher.html",
    "revision": "18ec51c57d24c438933557d64c030ec4"
  },
  {
    "url": "api/message.html",
    "revision": "f45f29d154482d2bec20b6df238baae4"
  },
  {
    "url": "api/nonebot.html",
    "revision": "20b880f92cea04cf8643486e15279a73"
  },
  {
    "url": "api/permission.html",
    "revision": "1c955bb8e1f64cc0baefe1e8bd2434dd"
  },
  {
    "url": "api/plugin.html",
    "revision": "51da3c3a77fbe3ee1cc0cecf8e9bbd1d"
  },
  {
    "url": "api/rule.html",
    "revision": "fa3471649fcde838ca7ad823d6a1b8f9"
  },
  {
    "url": "api/typing.html",
    "revision": "99e1477f84ebba9a7278456b6c140213"
  },
  {
    "url": "api/utils.html",
    "revision": "204cd20ad3210935f405ba6ecc20c711"
  },
  {
    "url": "assets/css/0.styles.371e194f.css",
    "revision": "08479179ebbae9149db293d10e3be884"
  },
  {
    "url": "assets/img/search.237d6f6a.svg",
    "revision": "237d6f6a3fe211d00a61e871a263e9fe"
  },
  {
    "url": "assets/img/search.83621669.svg",
    "revision": "83621669651b9a3d4bf64d1a670ad856"
  },
  {
    "url": "assets/js/10.2d526a31.js",
    "revision": "d454db08b1761dc8442ce0b2b9365cc6"
  },
  {
    "url": "assets/js/100.6c92ba01.js",
    "revision": "df14b2fce1b4f3d436e4fcb1c3ff51af"
  },
  {
    "url": "assets/js/101.6feb1de3.js",
    "revision": "000da90f0962ef35533b8c5ba87c2e1b"
  },
  {
    "url": "assets/js/102.9d9edd01.js",
    "revision": "2ddf607b21e5472acd6abb2c899dd325"
  },
  {
    "url": "assets/js/103.8dccc736.js",
    "revision": "0ea055d59c01db00511744d9355b0bde"
  },
  {
    "url": "assets/js/104.d8c2ac09.js",
    "revision": "df4115d99a3d9bd002f830fb4006dc92"
  },
  {
    "url": "assets/js/105.5973e3ac.js",
    "revision": "ec6bbff6339351558b0f52ba1ae52e73"
  },
  {
    "url": "assets/js/106.4900cd74.js",
    "revision": "7cc4cf073ae15bbe25b7fea483938aa6"
  },
  {
    "url": "assets/js/107.3d989ebf.js",
    "revision": "5f9c079786fe859af9ac08d515540f0b"
  },
  {
    "url": "assets/js/108.7c6dd7cb.js",
    "revision": "42eb20ae365888ffbd7eabfcf831f28c"
  },
  {
    "url": "assets/js/109.46920675.js",
    "revision": "7f65f02c1c4d6cb72fb5540bfe1e7bf0"
  },
  {
    "url": "assets/js/11.0aec283a.js",
    "revision": "516e86d065b30a9228a1130d74475054"
  },
  {
    "url": "assets/js/110.2c5a1605.js",
    "revision": "9ed01022a296de0ced501c82f758df4a"
  },
  {
    "url": "assets/js/111.b2b61520.js",
    "revision": "0a2a2c24c3abb406bd343fb579ea0f57"
  },
  {
    "url": "assets/js/112.0426edea.js",
    "revision": "c4a3c22b7b4b403cf3d3cfcecd4080d5"
  },
  {
    "url": "assets/js/113.26dca822.js",
    "revision": "fe40b2051995d36deb60b30bb01eb2ab"
  },
  {
    "url": "assets/js/114.8278351d.js",
    "revision": "32a6570c6057c8fa9a42458751c4d159"
  },
  {
    "url": "assets/js/115.40fcb81a.js",
    "revision": "90262f7e54b708a9c412cf30b7f6174e"
  },
  {
    "url": "assets/js/116.20c6ef41.js",
    "revision": "769fb248e0a5ca17fa36410fd2b85e69"
  },
  {
    "url": "assets/js/117.188a8efb.js",
    "revision": "f83118d567b115f7e64ebb485877967f"
  },
  {
    "url": "assets/js/118.3a630bff.js",
    "revision": "4fe51da2a6f867c4ef60f43dfe96f025"
  },
  {
    "url": "assets/js/119.43cb90bd.js",
    "revision": "2269a1a76c307379d3c0861276b9f17e"
  },
  {
    "url": "assets/js/12.ada4ed0c.js",
    "revision": "48b7ee5a4f23a974bf17e83ad943c41b"
  },
  {
    "url": "assets/js/120.4af71aa9.js",
    "revision": "f5ba15eadc006f6451039de800e1f2cf"
  },
  {
    "url": "assets/js/121.3e6eab2e.js",
    "revision": "9e3bed0b19503894b05d974050f20f54"
  },
  {
    "url": "assets/js/122.7a413004.js",
    "revision": "7e4bee4d5222254422a528f6bb1550ec"
  },
  {
    "url": "assets/js/123.4bf12088.js",
    "revision": "c0f9454c259ced96b00010d93cb34d37"
  },
  {
    "url": "assets/js/124.85f5a818.js",
    "revision": "cf8bf1ff561c935dc5d73fe350d1220c"
  },
  {
    "url": "assets/js/125.6ac41600.js",
    "revision": "5ea13b5e08b7931791258f8c1a3c7019"
  },
  {
    "url": "assets/js/126.3229d4fb.js",
    "revision": "f4b10b2b796f0332728f7027857f66d1"
  },
  {
    "url": "assets/js/127.a5658cbf.js",
    "revision": "2127efec6b923f297be2d1a3c788b1d7"
  },
  {
    "url": "assets/js/128.85eadc4a.js",
    "revision": "ea4b50743e345ea8c0e9f6f27778c744"
  },
  {
    "url": "assets/js/129.a764f15f.js",
    "revision": "fa3c2c572ea454cec9ada61f1b731908"
  },
  {
    "url": "assets/js/13.cae86f08.js",
    "revision": "4f29e42ab7311ecba77bab797e973558"
  },
  {
    "url": "assets/js/130.86f727cd.js",
    "revision": "5b81973c5f4f440f9b5c5f9882b77d51"
  },
  {
    "url": "assets/js/131.1ccbb1c7.js",
    "revision": "11b2cd92366a0066349392818c554796"
  },
  {
    "url": "assets/js/132.97947577.js",
    "revision": "2d6465c31f12eb8bd1639d43a96c0c59"
  },
  {
    "url": "assets/js/133.b4522f91.js",
    "revision": "b4f294b873e001853306865421106f23"
  },
  {
    "url": "assets/js/134.f8db0c49.js",
    "revision": "d52e665d8c29e670c37896bb85d44795"
  },
  {
    "url": "assets/js/135.bb553da9.js",
    "revision": "62d10da05cba3b522ba6b7908ea38739"
  },
  {
    "url": "assets/js/136.27f3840f.js",
    "revision": "b34518e2f3687eb8b18f276b6eb6a26a"
  },
  {
    "url": "assets/js/137.9e74ccdb.js",
    "revision": "bfe03ca21af34932e2a9c7d86cfda75b"
  },
  {
    "url": "assets/js/138.37a606b8.js",
    "revision": "3c5d31a58ceed6b404653673905327f6"
  },
  {
    "url": "assets/js/139.0c83cd5b.js",
    "revision": "b0ffd1104f9d8c27f538b9111c156a7a"
  },
  {
    "url": "assets/js/14.40645430.js",
    "revision": "0bc7d61c4ea1a2770535ef619daf97c9"
  },
  {
    "url": "assets/js/140.9e8578e9.js",
    "revision": "c128887dae02a40b65a8857dadc8c476"
  },
  {
    "url": "assets/js/141.40e8293a.js",
    "revision": "7ea5f1d5801f77fdb0876dc6f549a40b"
  },
  {
    "url": "assets/js/142.45b7d6e0.js",
    "revision": "5e9c7833f3aa4cade873527b57334e5c"
  },
  {
    "url": "assets/js/143.ea227833.js",
    "revision": "ec09a7f811d7d5dc6e768069c9438c22"
  },
  {
    "url": "assets/js/144.d9a2473f.js",
    "revision": "a0736aa45abeed5d72384ea1273656a8"
  },
  {
    "url": "assets/js/145.d2d28014.js",
    "revision": "3831f8e501f334de172dc3b1c9e3b2e7"
  },
  {
    "url": "assets/js/146.727e9c38.js",
    "revision": "6c2983e5cf6934e2c249f420683cfc75"
  },
  {
    "url": "assets/js/147.35787bfe.js",
    "revision": "79ae8c508674f9df84b3cf25e7c2aacc"
  },
  {
    "url": "assets/js/148.15fe2ed5.js",
    "revision": "185e52e605b25458d55d0d9816e3fd6c"
  },
  {
    "url": "assets/js/149.79af7853.js",
    "revision": "c4d8e0cdb6bf2945ed9a99466f92505c"
  },
  {
    "url": "assets/js/15.2719dc91.js",
    "revision": "a42d9045155a1f28c5d13a323ce28599"
  },
  {
    "url": "assets/js/150.6c8aba4c.js",
    "revision": "a3bdd317743e6ffb2b524e8664d8abd3"
  },
  {
    "url": "assets/js/151.59315a5e.js",
    "revision": "9c15da90668dbba25c13926e646b227b"
  },
  {
    "url": "assets/js/152.dc298b46.js",
    "revision": "42a45eac87aad49a143ea74aabbc627a"
  },
  {
    "url": "assets/js/153.1f41971f.js",
    "revision": "5baa8a5a85e51af1aa203125943dcb19"
  },
  {
    "url": "assets/js/154.721a376f.js",
    "revision": "4caf4b61a4da51a6088171e61b966e5a"
  },
  {
    "url": "assets/js/155.6d658ba5.js",
    "revision": "b92e5454fbbdda7a568376793e582223"
  },
  {
    "url": "assets/js/156.c436243e.js",
    "revision": "1e39428783b4ef23f3733a13eaaa15d8"
  },
  {
    "url": "assets/js/157.def09d88.js",
    "revision": "6e0e896d010a0fa697c6fea0f4256d84"
  },
  {
    "url": "assets/js/158.e332156e.js",
    "revision": "721078278684ede3a92b6282ef4fd6e3"
  },
  {
    "url": "assets/js/159.a5e8a74c.js",
    "revision": "8bdb9b803412fabcbcf6dc6841696dc4"
  },
  {
    "url": "assets/js/16.531460cd.js",
    "revision": "4cd133dc74625dce8bd7e1d7e075cadc"
  },
  {
    "url": "assets/js/160.24fa7732.js",
    "revision": "aeb6bd7644eb0e85ef3bddd391bec48d"
  },
  {
    "url": "assets/js/17.e9cdfd31.js",
    "revision": "2cca3353f8ef005b5f69149161ecb972"
  },
  {
    "url": "assets/js/18.75b165ab.js",
    "revision": "2b1008350481102cf9c960f91c16c8c2"
  },
  {
    "url": "assets/js/19.e768bccb.js",
    "revision": "2267d1553cc17777b907ddce815fce49"
  },
  {
    "url": "assets/js/2.9e2d6c06.js",
    "revision": "1e457d6a57e990c8b0812557ace91a12"
  },
  {
    "url": "assets/js/20.b448cbf7.js",
    "revision": "f241f88281c37b9e03cb21e856fc5f20"
  },
  {
    "url": "assets/js/21.2c14a85b.js",
    "revision": "60cbaacaf0c83936528f51deb28b3fc9"
  },
  {
    "url": "assets/js/22.36bf8c31.js",
    "revision": "d66636bdabf76cd7a69065fe32e55788"
  },
  {
    "url": "assets/js/23.c8f6570a.js",
    "revision": "4e1763c8fca6013c4b9b5de17b45d028"
  },
  {
    "url": "assets/js/24.48148f1f.js",
    "revision": "05606c50de57f839390fcdfddcb55286"
  },
  {
    "url": "assets/js/25.65fe0cf6.js",
    "revision": "25ef7b071947271479d5918b7b9d20cb"
  },
  {
    "url": "assets/js/26.be823409.js",
    "revision": "e939072a641d8afe1bcb1b3271a4c3b1"
  },
  {
    "url": "assets/js/27.43694f25.js",
    "revision": "44413edd73269c5fc372db9c79d7b504"
  },
  {
    "url": "assets/js/28.69d80a18.js",
    "revision": "bb0c394baf2c6b510f0aa838348f6ad4"
  },
  {
    "url": "assets/js/29.056638a1.js",
    "revision": "3ba5af812c452f3d683e9f0353e8127c"
  },
  {
    "url": "assets/js/3.d3c911dd.js",
    "revision": "a544e298e23bca602cd07e134bb0c886"
  },
  {
    "url": "assets/js/30.49f1691f.js",
    "revision": "bef21d2e2fcb63d077ecaf62db935653"
  },
  {
    "url": "assets/js/31.ccd02878.js",
    "revision": "241b614b1d46e7117b5c0806df275133"
  },
  {
    "url": "assets/js/32.fd938f53.js",
    "revision": "04c913c7592381474f5c78f0c2d8ce7c"
  },
  {
    "url": "assets/js/33.9ead72e6.js",
    "revision": "677770ce73e0abac29ac8841b105719f"
  },
  {
    "url": "assets/js/34.b4e0763b.js",
    "revision": "3d377177c32d90d124a864cdfab5fe52"
  },
  {
    "url": "assets/js/35.927ba3d0.js",
    "revision": "bc3aad80c30a2a76d659c4435b3c5995"
  },
  {
    "url": "assets/js/36.1a617f8b.js",
    "revision": "41b1274f93f5a13e8bbd150349be762b"
  },
  {
    "url": "assets/js/37.f4c9766e.js",
    "revision": "5d4c593fe7ea8feb1a31c8cc7633cdd7"
  },
  {
    "url": "assets/js/38.fc6a8184.js",
    "revision": "601ac78e42ad6e25ae8932a3514dfb9e"
  },
  {
    "url": "assets/js/39.2fadf61c.js",
    "revision": "7e109bf2eb5986eb96fbea174bc39652"
  },
  {
    "url": "assets/js/4.8df46d24.js",
    "revision": "71fee54f67a404aca2a106ab41e63e5e"
  },
  {
    "url": "assets/js/40.b4254ee2.js",
    "revision": "7443dc5ca7c371e4a5200ddcb6dc81a3"
  },
  {
    "url": "assets/js/41.082e5762.js",
    "revision": "5e58a3256e95d017d0d46b0eaa475f36"
  },
  {
    "url": "assets/js/42.6ce56cc1.js",
    "revision": "b4da8d44deb901ac232d992ed29200cb"
  },
  {
    "url": "assets/js/43.7d03c637.js",
    "revision": "b43337bd0e58dc63541e974b9843403e"
  },
  {
    "url": "assets/js/44.4128924c.js",
    "revision": "2d384ab4c43a0cfb89bde2385364c33e"
  },
  {
    "url": "assets/js/45.ac5f147f.js",
    "revision": "a8531994169e13b805b4b6af42e2d0af"
  },
  {
    "url": "assets/js/46.9c8a2fe1.js",
    "revision": "2a10bacf8a9218ed8a933dbc12e239c3"
  },
  {
    "url": "assets/js/47.169840bd.js",
    "revision": "e94d787e3a8be52c9616f89629e3052e"
  },
  {
    "url": "assets/js/48.f91c1460.js",
    "revision": "f7d5584898a3b17f6849e8428f82d394"
  },
  {
    "url": "assets/js/49.292fc28c.js",
    "revision": "5c91da47bfce34bf2a6ca609fe7d4b7d"
  },
  {
    "url": "assets/js/5.1299c054.js",
    "revision": "077af6c44ce4d6790e08acadf1b55cf6"
  },
  {
    "url": "assets/js/50.cad42a1c.js",
    "revision": "2d90c28f3495ae083cb2b40e12b51d88"
  },
  {
    "url": "assets/js/51.8157b4d4.js",
    "revision": "d4a6d5f4672f41d1ef4bc853273b0962"
  },
  {
    "url": "assets/js/52.0b8f8265.js",
    "revision": "ac7b9a13cc989b28cc05501b17aca3fb"
  },
  {
    "url": "assets/js/53.4bc75f0d.js",
    "revision": "9e799b9f2904c54084d766f1637d1a27"
  },
  {
    "url": "assets/js/54.515ab73e.js",
    "revision": "fbd3a56c58f71296e9e455eb22879629"
  },
  {
    "url": "assets/js/55.cf78aa87.js",
    "revision": "18487bb92d10ebc65cf9413c8746c46a"
  },
  {
    "url": "assets/js/56.00d32bf9.js",
    "revision": "a9f066a7eff70ca6b25bfc8c72bebf29"
  },
  {
    "url": "assets/js/57.ce14412d.js",
    "revision": "43313a17ddebc40b8ffea071183568b8"
  },
  {
    "url": "assets/js/58.6a05644f.js",
    "revision": "f0f6b2d57b6855c308be5bbe540d54e9"
  },
  {
    "url": "assets/js/59.b6540a20.js",
    "revision": "7ab881bfd23749011099d380c41f4f5f"
  },
  {
    "url": "assets/js/6.b71be673.js",
    "revision": "11228413bf4ceab71d2ec31eac9d9a0b"
  },
  {
    "url": "assets/js/60.f1b4522a.js",
    "revision": "7c048f671b4138f9bb07c99e81ba1d3f"
  },
  {
    "url": "assets/js/61.1fe70215.js",
    "revision": "fa17c2d2ea32fe8c3c995f9d827b2a42"
  },
  {
    "url": "assets/js/62.966e30f3.js",
    "revision": "a29568f48a98052d4eee75acab242a14"
  },
  {
    "url": "assets/js/63.5756836c.js",
    "revision": "cf91f8a51d190013bd76f4c22b809310"
  },
  {
    "url": "assets/js/64.6d01c18e.js",
    "revision": "0180ecb79bae5071adda3949c85214d3"
  },
  {
    "url": "assets/js/65.1c57175d.js",
    "revision": "de315c1ffd890a63f16cc39f43c1ffd0"
  },
  {
    "url": "assets/js/66.c21a716a.js",
    "revision": "34c74f225e2d3bc4d6354c56a163ef8d"
  },
  {
    "url": "assets/js/67.582bd0db.js",
    "revision": "5d22c27b35e259ae49b0bb173340eb5b"
  },
  {
    "url": "assets/js/68.ac5a7cca.js",
    "revision": "dc544d4436b43b0d3814b6da9578b27b"
  },
  {
    "url": "assets/js/69.e9bb1ba6.js",
    "revision": "a14052059a0b3d775b083cf30a01e296"
  },
  {
    "url": "assets/js/7.95afef53.js",
    "revision": "7a86d8a66df67c34b9e5b371c386a8c8"
  },
  {
    "url": "assets/js/70.3f5ba8fe.js",
    "revision": "95e23fb8640277eff086b57bf4d2c958"
  },
  {
    "url": "assets/js/71.99347c3a.js",
    "revision": "424420254ea4104e1af53d5ec2cd6223"
  },
  {
    "url": "assets/js/72.6e606825.js",
    "revision": "0dc5aeff4a1ff752fb501d313c27ec8b"
  },
  {
    "url": "assets/js/73.db20037f.js",
    "revision": "40826b1727be597d198d7bae351e968b"
  },
  {
    "url": "assets/js/74.b7d4e733.js",
    "revision": "74ca0cf2f7ffe652006ea74923a850de"
  },
  {
    "url": "assets/js/75.7d309119.js",
    "revision": "5ea57a52fdea74bf7fb836498176a92a"
  },
  {
    "url": "assets/js/76.37665051.js",
    "revision": "83c050928044f4661429d2c5e39a0cea"
  },
  {
    "url": "assets/js/77.8bb75d8b.js",
    "revision": "67e4a5b92cc50737219a4aa8b08495de"
  },
  {
    "url": "assets/js/78.75eeb5f2.js",
    "revision": "7e76be7a4ffff12c7f7391f05ab54a78"
  },
  {
    "url": "assets/js/79.aed48532.js",
    "revision": "01269732b683c5fcfba035c665cbc759"
  },
  {
    "url": "assets/js/8.6151909e.js",
    "revision": "36067ca3f868a72e6f3ae43c93068b2a"
  },
  {
    "url": "assets/js/80.d16ad379.js",
    "revision": "0c6edbf7b222905c2f013eb32a648a69"
  },
  {
    "url": "assets/js/81.e6675344.js",
    "revision": "e217a9709719fd8f85d22e51b0f78c8f"
  },
  {
    "url": "assets/js/82.f0ab5e44.js",
    "revision": "00a74746daa6e4324588255c29d0ee6a"
  },
  {
    "url": "assets/js/83.79079c2c.js",
    "revision": "49658dbe8619e4ccd26d01c3208d9b7b"
  },
  {
    "url": "assets/js/84.d4bc1545.js",
    "revision": "928b35819c53246eaa0a5911467ff07c"
  },
  {
    "url": "assets/js/85.b7123db0.js",
    "revision": "10baa272ae8400a28e548f50a49e713a"
  },
  {
    "url": "assets/js/86.596e5881.js",
    "revision": "53808dfa67af64f9e366de5a3b2e2452"
  },
  {
    "url": "assets/js/87.f47c69c0.js",
    "revision": "c7f7ea72c0e6a7bfdae90246638025f2"
  },
  {
    "url": "assets/js/88.e7aec2f5.js",
    "revision": "888eb739b91febd919c652c17864a47d"
  },
  {
    "url": "assets/js/89.3443c817.js",
    "revision": "705e58e44615b9be9275403fa12c13a2"
  },
  {
    "url": "assets/js/9.2979f5fb.js",
    "revision": "21de61771ae67e0a22a4072a6de45369"
  },
  {
    "url": "assets/js/90.403b7d43.js",
    "revision": "dfa3a8148222d5930cbfa5657164fd80"
  },
  {
    "url": "assets/js/91.525c323f.js",
    "revision": "616647cd367e888f4649e72685e0e200"
  },
  {
    "url": "assets/js/92.87064274.js",
    "revision": "fee35aef02a4417208d3d472628b04ec"
  },
  {
    "url": "assets/js/93.f1b0aede.js",
    "revision": "412e302789fe56c0326c65845b188729"
  },
  {
    "url": "assets/js/94.f41555d7.js",
    "revision": "94f6102472591d019177bf26bba2ac75"
  },
  {
    "url": "assets/js/95.6621545d.js",
    "revision": "63af7ae55069be1a5bf60fb7d094611b"
  },
  {
    "url": "assets/js/96.e9a42a1c.js",
    "revision": "75452f5e48ba4cf1b06203168ae91308"
  },
  {
    "url": "assets/js/97.86b25adc.js",
    "revision": "8ca2ca51c374cdc41d6f235a617a715e"
  },
  {
    "url": "assets/js/98.10f5bcb9.js",
    "revision": "c9cafcb9872e0a0b805e7363b0792ef2"
  },
  {
    "url": "assets/js/99.32742638.js",
    "revision": "34c2e3577a00585298f6fe5db6b306d4"
  },
  {
    "url": "assets/js/app.64bf1123.js",
    "revision": "03d7d4bc0b21e73424f6d23500714278"
  },
  {
    "url": "changelog.html",
    "revision": "dbaab85f6d17e3ad959bd590cb287048"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "b47616348bf6df1f6345af6a92b8faa7"
  },
  {
    "url": "guide/cqhttp-guide.html",
    "revision": "30e1d9fa5ae5a77e4fb9d4d35a19754d"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "1829cf83886a33dc8edf3ad89c50de8f"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "fa2e135c038845147e30c47b47694b5e"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "03f958418077b412d847b3d2ef097378"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "004491b3ab81dbf235ac0ca7ceb79a28"
  },
  {
    "url": "guide/ding-guide.html",
    "revision": "4f963963714df384e2dfde202c67d054"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "446d3656f3a47102743fdd2c0aa0a35a"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "e808dc22cc702e6e1af25ba4f54e0023"
  },
  {
    "url": "guide/index.html",
    "revision": "c16a1bd3e26a75ee5d41df6a58ca966d"
  },
  {
    "url": "guide/installation.html",
    "revision": "7a88a0c32b6ac5ee6c1ed5505d5660da"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "d9a2b37f074adb74a6f2414965a053af"
  },
  {
    "url": "guide/mirai-guide.html",
    "revision": "3ac8259ccde9c38ea8e26e35ab7e72eb"
  },
  {
    "url": "icons/android-chrome-192x192.png",
    "revision": "36b48f1887823be77c6a7656435e3e07"
  },
  {
    "url": "icons/android-chrome-384x384.png",
    "revision": "e0dc7c6250bd5072e055287fc621290b"
  },
  {
    "url": "icons/apple-touch-icon-180x180.png",
    "revision": "b8d652dd0e29786cc95c37f8ddc238de"
  },
  {
    "url": "icons/favicon-16x16.png",
    "revision": "e6c309ee1ea59d3fb1ee0582c1a7f78d"
  },
  {
    "url": "icons/favicon-32x32.png",
    "revision": "d42193f7a38ef14edb19feef8e055edc"
  },
  {
    "url": "icons/mstile-150x150.png",
    "revision": "a76847a12740d7066f602a3e627ec8c3"
  },
  {
    "url": "icons/safari-pinned-tab.svg",
    "revision": "18f1a1363394632fa5fabf95875459ab"
  },
  {
    "url": "index.html",
    "revision": "5cec1509fd497cf97b9b3dea6d7fd705"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/export-and-require.html",
    "revision": "87ee34e170238d8e0982b893b466e0bc"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "e810ad99e557e53ba9a198b6a39e9a06"
  },
  {
    "url": "next/advanced/overloaded-handlers.html",
    "revision": "c454c97eb1c37c65bf27bddb13096b3c"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "bbf5d13891c8c6874a91d8ef2ee69e9d"
  },
  {
    "url": "next/advanced/publish-plugin.html",
    "revision": "3fcccbbfe9fb5cd00768c5fb1d9bd55f"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "bee1338d78f5287d9243f8d55e843231"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "a222aa3da9263fa77fd88338ca0d1da7"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "95f4558e38a48f31a93fd598af9cb76c"
  },
  {
    "url": "next/api/adapters/ding.html",
    "revision": "c5a4e25f608dd21f003dbcfb33240e0b"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "7b5ea919a64e4e30aeb5f8544eacef17"
  },
  {
    "url": "next/api/adapters/mirai.html",
    "revision": "99bde9c5e44678972c70506a03ab0657"
  },
  {
    "url": "next/api/config.html",
    "revision": "d85fe2d9b0259290ff112191f90cef24"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "276a051d21fb231228eadfe3be0959d5"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "dc291a1b84854d26bf430d69538bac91"
  },
  {
    "url": "next/api/exception.html",
    "revision": "714b058f5670e0f863f6b31b3143efb9"
  },
  {
    "url": "next/api/index.html",
    "revision": "161887b9bbc3bacd1d760e551797dd2e"
  },
  {
    "url": "next/api/log.html",
    "revision": "922a280ca83c8d971577c92c681dbcaa"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "e2be2b852c69ec60557865fe7f3603c4"
  },
  {
    "url": "next/api/message.html",
    "revision": "f46a41e1b67894af15dfbe53a2854ea3"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "a83192f6898a6e4d5e06f39ce6989756"
  },
  {
    "url": "next/api/permission.html",
    "revision": "6704b567791969cb1e52996fea472f4a"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "89aee9ee8f3a4b90e5ab478640f45edd"
  },
  {
    "url": "next/api/rule.html",
    "revision": "9541fece1f8fbcac25b187cb777bbf37"
  },
  {
    "url": "next/api/typing.html",
    "revision": "674e2d1995f6f34525f3c570e8741f39"
  },
  {
    "url": "next/api/utils.html",
    "revision": "1d4a7587ef82127e54417b1aaad79f00"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "03cdd203856b018db8921612fe883495"
  },
  {
    "url": "next/guide/cqhttp-guide.html",
    "revision": "f3c8519bd417dd540c757158f12daa62"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "f8734098b78bc660172bfee6f73cf33c"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "5a190a2e5d86efea0d308e2386932367"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "ccd1be7c5f45a4c591347b6cdc115967"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "aa6f3504c4a64e74e259d8cd01e1954e"
  },
  {
    "url": "next/guide/ding-guide.html",
    "revision": "a1f6704b12f28d6468933482cce91a0e"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "0c66e5340fb886a58b948129eccace78"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "136c1773edf6b884d8a738b6d479895f"
  },
  {
    "url": "next/guide/index.html",
    "revision": "83f5559e8064033b5ff23b9d55dc4f9a"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "0cf574200cc2d60cbb1d19c79e1e7071"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "13f445125c640c056719aae344e9be60"
  },
  {
    "url": "next/guide/mirai-guide.html",
    "revision": "ad6936eae2f7717cbb522a2d0f123396"
  },
  {
    "url": "next/index.html",
    "revision": "cecafe5890587bff447acc68dfbae034"
  },
  {
    "url": "plugin-store.html",
    "revision": "728669c4df990c0f6f06d8912dc1abbf"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
