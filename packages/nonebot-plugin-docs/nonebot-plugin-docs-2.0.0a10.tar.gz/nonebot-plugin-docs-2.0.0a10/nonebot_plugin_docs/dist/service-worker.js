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
    "revision": "cbb598df0920146bff6d92a19de297a5"
  },
  {
    "url": "2.0.0a7/advanced/index.html",
    "revision": "5b0805823bc64348ef4fb57a0bd44ad6"
  },
  {
    "url": "2.0.0a7/advanced/permission.html",
    "revision": "f5f2e774f23e04952128abecab3e9f3d"
  },
  {
    "url": "2.0.0a7/advanced/publish-plugin.html",
    "revision": "d7b42f0258cef2ae51803f40f9d7a03d"
  },
  {
    "url": "2.0.0a7/advanced/runtime-hook.html",
    "revision": "ba944095062848b13b2041d21287fffa"
  },
  {
    "url": "2.0.0a7/advanced/scheduler.html",
    "revision": "e97fb2453abb058434188a953fa75a15"
  },
  {
    "url": "2.0.0a7/api/adapters/cqhttp.html",
    "revision": "fbb4aa19ffa43d66a7732eef6bb32047"
  },
  {
    "url": "2.0.0a7/api/adapters/ding.html",
    "revision": "9c80bb14431f1df4190b7fd0e29d5797"
  },
  {
    "url": "2.0.0a7/api/adapters/index.html",
    "revision": "7fea033ec46a9c9ebba5eb33809a0539"
  },
  {
    "url": "2.0.0a7/api/config.html",
    "revision": "1b90f089721d7de40d2074d9145f8274"
  },
  {
    "url": "2.0.0a7/api/drivers/fastapi.html",
    "revision": "64de67d254f987741a9c6c6392ec673f"
  },
  {
    "url": "2.0.0a7/api/drivers/index.html",
    "revision": "e20762be5fde283926373f3ce62222a8"
  },
  {
    "url": "2.0.0a7/api/exception.html",
    "revision": "397bd048b8659cb6d6be2fc6e9e65f78"
  },
  {
    "url": "2.0.0a7/api/index.html",
    "revision": "19e06651dd86f84a9d8c4926f3f504e0"
  },
  {
    "url": "2.0.0a7/api/log.html",
    "revision": "747cc545f0e6e095febc63418f4ee551"
  },
  {
    "url": "2.0.0a7/api/matcher.html",
    "revision": "f9210c94228e0e43fb209b8cb3006de8"
  },
  {
    "url": "2.0.0a7/api/message.html",
    "revision": "c59799bfc4879cdc2455baaa4d0b4dca"
  },
  {
    "url": "2.0.0a7/api/nonebot.html",
    "revision": "22ac3c899e22ef68febd70a990acbcc1"
  },
  {
    "url": "2.0.0a7/api/permission.html",
    "revision": "57734132af38c8ca578974bc0ebcd36c"
  },
  {
    "url": "2.0.0a7/api/plugin.html",
    "revision": "f0f0fd1740445a85cf54e245f1c3cd04"
  },
  {
    "url": "2.0.0a7/api/rule.html",
    "revision": "334a1812202d846663102f2644e1d849"
  },
  {
    "url": "2.0.0a7/api/typing.html",
    "revision": "cf0fe8f67bba998d06d57e4b5ba890a0"
  },
  {
    "url": "2.0.0a7/api/utils.html",
    "revision": "df03f21dfff616d5bf4755510ef00297"
  },
  {
    "url": "2.0.0a7/guide/basic-configuration.html",
    "revision": "e51e0b962b56cc3f8d2700da8c0819a6"
  },
  {
    "url": "2.0.0a7/guide/creating-a-handler.html",
    "revision": "6c5f15025960bea5eb8acdf14e78bc6a"
  },
  {
    "url": "2.0.0a7/guide/creating-a-matcher.html",
    "revision": "da0dc84c69ecee4f076f05db613ff5f7"
  },
  {
    "url": "2.0.0a7/guide/creating-a-plugin.html",
    "revision": "e0066d036d90e6265d5b6915514017bc"
  },
  {
    "url": "2.0.0a7/guide/creating-a-project.html",
    "revision": "e1804ddfc45aeb17774a9bdc5b7de912"
  },
  {
    "url": "2.0.0a7/guide/end-or-start.html",
    "revision": "04b3223ef7a91b7f2fd34846ea7ad68d"
  },
  {
    "url": "2.0.0a7/guide/getting-started.html",
    "revision": "6be6ba9c9b4de72334f60a28fce04463"
  },
  {
    "url": "2.0.0a7/guide/index.html",
    "revision": "73c745d982a463c80d4e871d6255390a"
  },
  {
    "url": "2.0.0a7/guide/installation.html",
    "revision": "0192d8d5e9d9984b543440c37bcff568"
  },
  {
    "url": "2.0.0a7/guide/loading-a-plugin.html",
    "revision": "27671b89fb1e28dad0169f2360609bf3"
  },
  {
    "url": "2.0.0a7/index.html",
    "revision": "daa00b36cf607262c84c6c9e693be9c6"
  },
  {
    "url": "2.0.0a8.post2/advanced/export-and-require.html",
    "revision": "17b2d1210369e80b6dcb6fd2b9547347"
  },
  {
    "url": "2.0.0a8.post2/advanced/index.html",
    "revision": "49e0c94d3acf2e487f88a376cd649521"
  },
  {
    "url": "2.0.0a8.post2/advanced/overloaded-handlers.html",
    "revision": "169ced7a6a5d38b0f2268eda063f0f2d"
  },
  {
    "url": "2.0.0a8.post2/advanced/permission.html",
    "revision": "3d69a4c44e3a5a815ebd2e6c336cab2c"
  },
  {
    "url": "2.0.0a8.post2/advanced/publish-plugin.html",
    "revision": "d9652620c41ab5eb67136317368bc928"
  },
  {
    "url": "2.0.0a8.post2/advanced/runtime-hook.html",
    "revision": "e6faec9a53f45fa2827a17b1954ba8cb"
  },
  {
    "url": "2.0.0a8.post2/advanced/scheduler.html",
    "revision": "31d3809d619d84a2054ccc560ef8d4cb"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/cqhttp.html",
    "revision": "09acfdb3ee39492cb36033b01d3f0a6d"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/ding.html",
    "revision": "bd12666d1a1cb59f77d0aabdb707b63e"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/index.html",
    "revision": "1a86d1f0d21bbedee2285996b1e39bd2"
  },
  {
    "url": "2.0.0a8.post2/api/config.html",
    "revision": "4764d6df4845fd18c9ce11d731ccda10"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/fastapi.html",
    "revision": "f09d6b93d0a0451a3e4e13f43c3f03f3"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/index.html",
    "revision": "0a88f4dbb4aeedd4b15a06d70a49585f"
  },
  {
    "url": "2.0.0a8.post2/api/exception.html",
    "revision": "6186ddcf9955a7d84035cbd566ad0f67"
  },
  {
    "url": "2.0.0a8.post2/api/index.html",
    "revision": "4870a0915030b491a5021796580b23f2"
  },
  {
    "url": "2.0.0a8.post2/api/log.html",
    "revision": "9a61f2878be66d0cc40ca9bad19d6e38"
  },
  {
    "url": "2.0.0a8.post2/api/matcher.html",
    "revision": "d53cd8c79934cfd0e21a9f505299c8ab"
  },
  {
    "url": "2.0.0a8.post2/api/message.html",
    "revision": "034cc0702ef099373454aaf2064b4006"
  },
  {
    "url": "2.0.0a8.post2/api/nonebot.html",
    "revision": "b260c35118b9beee48f3f4e007634867"
  },
  {
    "url": "2.0.0a8.post2/api/permission.html",
    "revision": "f0e5828bf2b51db4f9d7fecbcdada8a3"
  },
  {
    "url": "2.0.0a8.post2/api/plugin.html",
    "revision": "54c96c9fd274b74dc0b32f84272c948e"
  },
  {
    "url": "2.0.0a8.post2/api/rule.html",
    "revision": "e39561349cfc0a38119adfadc8fa44e2"
  },
  {
    "url": "2.0.0a8.post2/api/typing.html",
    "revision": "f294ebe8c90e9bd06b78a059aef9333a"
  },
  {
    "url": "2.0.0a8.post2/api/utils.html",
    "revision": "d640dc6bdfc41a9f223072e727d757ce"
  },
  {
    "url": "2.0.0a8.post2/guide/basic-configuration.html",
    "revision": "0204594325df503d9a56d9aa37eb7626"
  },
  {
    "url": "2.0.0a8.post2/guide/cqhttp-guide.html",
    "revision": "f0095f1e79c3c8c760613b7b5b5b55a1"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-handler.html",
    "revision": "2ce32d9e3c0bfe17dc63155bf3bd75e6"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-matcher.html",
    "revision": "bd696bd7b462a49d61650532eca925b6"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-plugin.html",
    "revision": "0df361f4c5d0ac290c34544a586211a2"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-project.html",
    "revision": "38ca329746c655c4b05ce75bcd8177cf"
  },
  {
    "url": "2.0.0a8.post2/guide/ding-guide.html",
    "revision": "eb4bedf375d90c78db266269e0c3c391"
  },
  {
    "url": "2.0.0a8.post2/guide/end-or-start.html",
    "revision": "5dea86ffb4663c61a84f4f7b6210eae7"
  },
  {
    "url": "2.0.0a8.post2/guide/getting-started.html",
    "revision": "2302a0318743c0b9d7537f693b1630a4"
  },
  {
    "url": "2.0.0a8.post2/guide/index.html",
    "revision": "6dfa8fa8cfcfdd9b3903a7f812a82033"
  },
  {
    "url": "2.0.0a8.post2/guide/installation.html",
    "revision": "616a0cb3e28ec0c5bad160e4e9897c91"
  },
  {
    "url": "2.0.0a8.post2/guide/loading-a-plugin.html",
    "revision": "a716c96a9b654fbbabf1275a233e63a3"
  },
  {
    "url": "2.0.0a8.post2/index.html",
    "revision": "e056c43a40a4ecb35651de2689cafe7d"
  },
  {
    "url": "404.html",
    "revision": "1f204923bd143a5bf8cf07c6174c83d2"
  },
  {
    "url": "advanced/export-and-require.html",
    "revision": "1788fa1f5fc75e3740740832037c1107"
  },
  {
    "url": "advanced/index.html",
    "revision": "31c3864a67dc6c6077507640e50bdaef"
  },
  {
    "url": "advanced/overloaded-handlers.html",
    "revision": "08168e91b0a8de71370954f241a3527f"
  },
  {
    "url": "advanced/permission.html",
    "revision": "77f648c629af5698f2cc36c39e894fe3"
  },
  {
    "url": "advanced/publish-plugin.html",
    "revision": "c5634f33f393e2776b3bb731099ba8e9"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "146e0b04ba16290caa0cca102f172df5"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "0d9c1f17cf2171336403c6885796a4fc"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "84480bed491491dbc7aa1962f1ecb933"
  },
  {
    "url": "api/adapters/ding.html",
    "revision": "510b4ca60ae73cb1ec9844e25d17d041"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "ef872ca11050105e658014918798aba6"
  },
  {
    "url": "api/adapters/mirai.html",
    "revision": "4dc094990bef9720c045606cb48fad4c"
  },
  {
    "url": "api/config.html",
    "revision": "e395dfc62fb00da9420bd17bdf0355bf"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "7ccc7d383b1209a6b2c4ad9c550074fc"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "99abceebf50551e3f7d36eb0b3c58d97"
  },
  {
    "url": "api/exception.html",
    "revision": "11ea6634daef8005ab9679b3433fc999"
  },
  {
    "url": "api/index.html",
    "revision": "fe8f679878536601199c8a6068db7f0e"
  },
  {
    "url": "api/log.html",
    "revision": "171781a0e4b17df98f1b345c1cd052d8"
  },
  {
    "url": "api/matcher.html",
    "revision": "f7a92e4e2342b7a6b04885b0c6ac52dd"
  },
  {
    "url": "api/message.html",
    "revision": "e2625670a0f3016621a3f11a87ba587a"
  },
  {
    "url": "api/nonebot.html",
    "revision": "63c7117a3c21048f99dfd6e95499f8bd"
  },
  {
    "url": "api/permission.html",
    "revision": "ad01f306419b3f941fb59e049c7a52b2"
  },
  {
    "url": "api/plugin.html",
    "revision": "d1e841144e620c9878e6c211f6f09196"
  },
  {
    "url": "api/rule.html",
    "revision": "5f31bc4a2e0b49ad33ff1811d3346fa1"
  },
  {
    "url": "api/typing.html",
    "revision": "ed068455b10d7ac92cc299986bfbeb99"
  },
  {
    "url": "api/utils.html",
    "revision": "11b43207fa9fceed376817e30987b19d"
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
    "url": "assets/js/10.34c391ea.js",
    "revision": "11e8af2c90cd96da1d71af0e72a9628b"
  },
  {
    "url": "assets/js/100.d274dbe6.js",
    "revision": "df56308f261a771565227ea2c1097158"
  },
  {
    "url": "assets/js/101.1db2e1e6.js",
    "revision": "e9ccd8c34da74b607a609be14bae6cba"
  },
  {
    "url": "assets/js/102.b8dc5f2f.js",
    "revision": "63026af2fb9fc9b6e0600ed0c2ff21e0"
  },
  {
    "url": "assets/js/103.f127f960.js",
    "revision": "3caaa52b090c76803504c6cb16f34b18"
  },
  {
    "url": "assets/js/104.07d5d8bb.js",
    "revision": "f0305ec8d3df8d7d20dc08a982766eed"
  },
  {
    "url": "assets/js/105.94f9871d.js",
    "revision": "205ce1f461216de553a292a979778367"
  },
  {
    "url": "assets/js/106.108ef2c3.js",
    "revision": "3b51fa099d57ae193b67056b3b40e885"
  },
  {
    "url": "assets/js/107.ad85531f.js",
    "revision": "79835189a1555a2d10ae885a10bb0615"
  },
  {
    "url": "assets/js/108.686db53f.js",
    "revision": "fcff9891080b95908cdac87ee809e245"
  },
  {
    "url": "assets/js/109.eeeed3a3.js",
    "revision": "aee80e0c444d6e38c0de8dd9737447a7"
  },
  {
    "url": "assets/js/11.b6653ad2.js",
    "revision": "ca2a06d5e21a2f95cd3e23c8f352249d"
  },
  {
    "url": "assets/js/110.b712c038.js",
    "revision": "55f504d15ac98c0af4e00e6c54c1df79"
  },
  {
    "url": "assets/js/111.4a9a4da3.js",
    "revision": "dfb381fdca6871c9449250be6c18c4ee"
  },
  {
    "url": "assets/js/112.3c0069a9.js",
    "revision": "ab873806e0718fd19914156477946f9e"
  },
  {
    "url": "assets/js/113.e6869526.js",
    "revision": "1909f5ce9bb85d992e8206a0c8f0bca9"
  },
  {
    "url": "assets/js/114.b010fc0e.js",
    "revision": "028b7726923416d5be8d0b200f706cfe"
  },
  {
    "url": "assets/js/115.519f4be4.js",
    "revision": "2f6517126fb9a4d5e878541e6d8babea"
  },
  {
    "url": "assets/js/116.d909d95d.js",
    "revision": "fa3982253bda0591a5d4b93b375d7618"
  },
  {
    "url": "assets/js/117.ea9f1987.js",
    "revision": "d7aaffff26748aa8dd0aff4bf23db5b7"
  },
  {
    "url": "assets/js/118.422a4b00.js",
    "revision": "66d01c8e2da58367dd425edd3ea111f7"
  },
  {
    "url": "assets/js/119.43cb90bd.js",
    "revision": "2269a1a76c307379d3c0861276b9f17e"
  },
  {
    "url": "assets/js/12.bf84e853.js",
    "revision": "ac582671d3512256d4b8c8d31cd459f5"
  },
  {
    "url": "assets/js/120.4af71aa9.js",
    "revision": "f5ba15eadc006f6451039de800e1f2cf"
  },
  {
    "url": "assets/js/121.a8698d37.js",
    "revision": "0c0ad2b98d5687fd09aa488dfc905c54"
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
    "url": "assets/js/127.e8a1bf8e.js",
    "revision": "0f9c61207f9414a8bb1dc98d0b9fc21d"
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
    "url": "assets/js/13.1c3134d0.js",
    "revision": "ac7f3805fb8d4adad0c32fa9ec1647c0"
  },
  {
    "url": "assets/js/130.86f727cd.js",
    "revision": "5b81973c5f4f440f9b5c5f9882b77d51"
  },
  {
    "url": "assets/js/131.87ca5df7.js",
    "revision": "9ccca07b4167c74894b61a22b9fac0c4"
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
    "url": "assets/js/135.59d3348a.js",
    "revision": "90cdbb24a09b403f7907c7871a453208"
  },
  {
    "url": "assets/js/136.5e362aaa.js",
    "revision": "45828e3cc30f804f10384a9fa5bbe820"
  },
  {
    "url": "assets/js/137.bf9803da.js",
    "revision": "a915d9b07d45ced0a00ee929b122a590"
  },
  {
    "url": "assets/js/138.db37b848.js",
    "revision": "70fefd356890b4a04dd8b58b9a3c128d"
  },
  {
    "url": "assets/js/139.5ac0ed22.js",
    "revision": "e3ae3a1f1ceea8eaaa37251b207b6e49"
  },
  {
    "url": "assets/js/14.a5cbdfe9.js",
    "revision": "74756e30fc1fb880fa29f4f23d26f7f0"
  },
  {
    "url": "assets/js/140.0abbbc62.js",
    "revision": "4c04440bc69593a32788990ee7e5905e"
  },
  {
    "url": "assets/js/141.45dafad3.js",
    "revision": "fc60b7642b94e258789b30d1330e1224"
  },
  {
    "url": "assets/js/142.13a9c867.js",
    "revision": "77941877852444e796b3956ef965c39f"
  },
  {
    "url": "assets/js/143.7564c6a3.js",
    "revision": "fb87350df08cf7ca2183cd10a0c40b9f"
  },
  {
    "url": "assets/js/144.881f12a4.js",
    "revision": "8cb493d286ce93fc1025228040cabeae"
  },
  {
    "url": "assets/js/145.d5a0bd41.js",
    "revision": "b330d892f66edf4a55691c636206528b"
  },
  {
    "url": "assets/js/146.1984aa72.js",
    "revision": "3ad6608e9f566331ace952410ac9c364"
  },
  {
    "url": "assets/js/147.0949814e.js",
    "revision": "39510efa207ddbe22f1651a251a85a8a"
  },
  {
    "url": "assets/js/148.b41e01d2.js",
    "revision": "51d14f84cab6b7670d7d0b88c817f805"
  },
  {
    "url": "assets/js/149.b998b4d4.js",
    "revision": "c3bb8cd9925471e005295094cdc59f0a"
  },
  {
    "url": "assets/js/15.cd8f3c0c.js",
    "revision": "645d8febcb0a89d0150eb6f2bba0647a"
  },
  {
    "url": "assets/js/150.4f1188c4.js",
    "revision": "748e0a877d439d03360895f422d07ed8"
  },
  {
    "url": "assets/js/151.c9a83fa7.js",
    "revision": "da6457fda9a0d97044384580abb37f94"
  },
  {
    "url": "assets/js/152.52c8b98b.js",
    "revision": "72c295f6ef400b677d874eb8a2058837"
  },
  {
    "url": "assets/js/153.692ed4c2.js",
    "revision": "792d184605fb6bee87c6747560060419"
  },
  {
    "url": "assets/js/154.956bca09.js",
    "revision": "5bb55c8861de335679a198790e963e9c"
  },
  {
    "url": "assets/js/155.1d5169be.js",
    "revision": "abf1de5a0dc9c6b4faeb60481f155ede"
  },
  {
    "url": "assets/js/156.a1ab11e9.js",
    "revision": "ddb6c082032200e03d3f2d5eb1102144"
  },
  {
    "url": "assets/js/157.181f6eef.js",
    "revision": "8dabbbac5dfe0b73fd9ea8486bdf3fb6"
  },
  {
    "url": "assets/js/158.cb4689bf.js",
    "revision": "9710a61d3b954a775b5a39a6ff079a6a"
  },
  {
    "url": "assets/js/159.34a76301.js",
    "revision": "3400e518eb3c28f9b0eff18f3a8e6f8f"
  },
  {
    "url": "assets/js/16.6361e6e0.js",
    "revision": "4bee1602df63ae9e36b5ce8ab0e56055"
  },
  {
    "url": "assets/js/160.2b34fd51.js",
    "revision": "86e77f14dcd95c170b73e95544fdcba1"
  },
  {
    "url": "assets/js/161.01dbab4d.js",
    "revision": "748142c6ee22538f127c8547af217f19"
  },
  {
    "url": "assets/js/17.286a791f.js",
    "revision": "c16bff10551c4ab6e4edcfb7943b6d15"
  },
  {
    "url": "assets/js/18.c652c7d0.js",
    "revision": "3dbfef4976095e7330f60e2d0d0549e0"
  },
  {
    "url": "assets/js/19.328ae505.js",
    "revision": "9d9e971f01858b4420f9e8c3d1b27184"
  },
  {
    "url": "assets/js/2.9e2d6c06.js",
    "revision": "1e457d6a57e990c8b0812557ace91a12"
  },
  {
    "url": "assets/js/20.498b9284.js",
    "revision": "11fcee19d9636dd25a850cb176274ca9"
  },
  {
    "url": "assets/js/21.0e503512.js",
    "revision": "0c2e566bd7326ba1740696d9af3c207e"
  },
  {
    "url": "assets/js/22.b91b48ef.js",
    "revision": "6697b443b45ca8094b2c290b300e0410"
  },
  {
    "url": "assets/js/23.fabcd764.js",
    "revision": "dd567bb74334822183676724c88a4501"
  },
  {
    "url": "assets/js/24.d830ad62.js",
    "revision": "efab8195cd23469def56792d96825cbe"
  },
  {
    "url": "assets/js/25.87f632af.js",
    "revision": "436ee91a4520cba31d393c4fcaa22ea1"
  },
  {
    "url": "assets/js/26.d7d60a5e.js",
    "revision": "3ea858fbb630d9d1fc299aa1f4d3e044"
  },
  {
    "url": "assets/js/27.82cf396a.js",
    "revision": "e275d81a36d8e6152cdee087720b9c01"
  },
  {
    "url": "assets/js/28.8ea45a6a.js",
    "revision": "3a8d5ca9fffd75feb2c1ab0683f14d12"
  },
  {
    "url": "assets/js/29.a16f0ffa.js",
    "revision": "7eaf3a1c06afb810db54b08bd9f9caab"
  },
  {
    "url": "assets/js/3.08dd197d.js",
    "revision": "553135c328edd8b7ead8b4ea6dc4a561"
  },
  {
    "url": "assets/js/30.f7a032e1.js",
    "revision": "ac2cb999f07057a5a92f91309f849707"
  },
  {
    "url": "assets/js/31.9a0295c2.js",
    "revision": "678f0cb40257aed141b73cc68653b87e"
  },
  {
    "url": "assets/js/32.8a8d2aac.js",
    "revision": "d3ea31f4dd6f5e0a323b212ff6f72853"
  },
  {
    "url": "assets/js/33.2db0e236.js",
    "revision": "d7cb0f73ee71838bf831da05e68c5ea6"
  },
  {
    "url": "assets/js/34.c6299224.js",
    "revision": "0d769d6d9394e83a3d5f5d220030eb13"
  },
  {
    "url": "assets/js/35.c5ee035f.js",
    "revision": "98a4e2212ac3f86ce8b358a66194e885"
  },
  {
    "url": "assets/js/36.cb53e510.js",
    "revision": "19f0bd791ffeea268c089313214659c0"
  },
  {
    "url": "assets/js/37.b11e45b6.js",
    "revision": "ad68baa1aa66d5cb34a86987908baa45"
  },
  {
    "url": "assets/js/38.503e55df.js",
    "revision": "9c3454c097e9c5811ceca86d11a6af1a"
  },
  {
    "url": "assets/js/39.150c5968.js",
    "revision": "b7def67baccfe4637ceed72f161f108b"
  },
  {
    "url": "assets/js/4.8df46d24.js",
    "revision": "71fee54f67a404aca2a106ab41e63e5e"
  },
  {
    "url": "assets/js/40.71ad37e2.js",
    "revision": "833b98b07adc07403d56a89ebe77a3ab"
  },
  {
    "url": "assets/js/41.89371e59.js",
    "revision": "9384833b93e04c1a7207994476cfa84c"
  },
  {
    "url": "assets/js/42.feb87fb3.js",
    "revision": "30f872d2e99b3de64e158caba6c8dbc6"
  },
  {
    "url": "assets/js/43.316468a7.js",
    "revision": "09faac8fe9e67e470add36f6f05a3959"
  },
  {
    "url": "assets/js/44.f9eb910b.js",
    "revision": "c3775be7fc96f9d61a218e0cc51e5064"
  },
  {
    "url": "assets/js/45.106abeb6.js",
    "revision": "428d86f7f2d38660e66725237d7a9848"
  },
  {
    "url": "assets/js/46.7fb2fd84.js",
    "revision": "51ae453ba40dc6bd6d343347f630bb3e"
  },
  {
    "url": "assets/js/47.c39fd7ea.js",
    "revision": "a1693bf1370df67ecf6ab4700bcf5ca0"
  },
  {
    "url": "assets/js/48.f1708c5e.js",
    "revision": "dcd091ce40ec662ca58ace527f27e507"
  },
  {
    "url": "assets/js/49.030e1530.js",
    "revision": "d688425e9028ea46d208535c500cc880"
  },
  {
    "url": "assets/js/5.1299c054.js",
    "revision": "077af6c44ce4d6790e08acadf1b55cf6"
  },
  {
    "url": "assets/js/50.31d90660.js",
    "revision": "637456f7ed7480142a6cd6c7036c78f8"
  },
  {
    "url": "assets/js/51.024f21cc.js",
    "revision": "07b910aff000848768c590ad3399ca8f"
  },
  {
    "url": "assets/js/52.b37ac7c1.js",
    "revision": "2a8a2b3d3083391162441e3d025d6639"
  },
  {
    "url": "assets/js/53.2d70c108.js",
    "revision": "f1a1198a93cc7470c7ef178083d71019"
  },
  {
    "url": "assets/js/54.d59b05ab.js",
    "revision": "151205bfe0c89347dc10669d38a12ec0"
  },
  {
    "url": "assets/js/55.b0b26b93.js",
    "revision": "4398081390da7bd951831e739edb26b4"
  },
  {
    "url": "assets/js/56.15afade3.js",
    "revision": "eed0df180275761d1824af6f504df0ab"
  },
  {
    "url": "assets/js/57.8890cfb4.js",
    "revision": "6ef102138789126437b8c8dbd5d04cbe"
  },
  {
    "url": "assets/js/58.a010dc5e.js",
    "revision": "09509e2ddde23361432113d5e078fa0c"
  },
  {
    "url": "assets/js/59.b218d361.js",
    "revision": "4921d36b0c1fb65d6f71e12982f85de0"
  },
  {
    "url": "assets/js/6.b71be673.js",
    "revision": "11228413bf4ceab71d2ec31eac9d9a0b"
  },
  {
    "url": "assets/js/60.6db21a10.js",
    "revision": "2eb70462399e5f12be25ebadff97a4fc"
  },
  {
    "url": "assets/js/61.0277b5aa.js",
    "revision": "f9491a199dce1c0ad35732427d7aded0"
  },
  {
    "url": "assets/js/62.b4561c72.js",
    "revision": "72d0e872a9c6906c8502d04f2c671608"
  },
  {
    "url": "assets/js/63.44ebdb05.js",
    "revision": "33381ba1e8340ef9fa5975014e33567a"
  },
  {
    "url": "assets/js/64.4537d754.js",
    "revision": "bdb29498eee402f6f7da3d92c0e9c987"
  },
  {
    "url": "assets/js/65.a67c160a.js",
    "revision": "be22c4ac66adfe004018e8afc43c78aa"
  },
  {
    "url": "assets/js/66.7cf298d1.js",
    "revision": "00d82df682b76b5c7834300c55859b4a"
  },
  {
    "url": "assets/js/67.5c73a7cc.js",
    "revision": "7a5dc20871954e0f1b89eece696641ac"
  },
  {
    "url": "assets/js/68.919e673b.js",
    "revision": "71ceae73550b97265cd7a2445cb9a0d2"
  },
  {
    "url": "assets/js/69.dffc8623.js",
    "revision": "0aa0857d045bd6884378dc8b0fa772fe"
  },
  {
    "url": "assets/js/7.a40d52db.js",
    "revision": "62fded7129963a8904133a43d8d99d4e"
  },
  {
    "url": "assets/js/70.2d47437f.js",
    "revision": "16951d457d5f4a904b8659636a43473e"
  },
  {
    "url": "assets/js/71.7eb7089c.js",
    "revision": "62cb64313109d74fff92263225591ac6"
  },
  {
    "url": "assets/js/72.58c11cbc.js",
    "revision": "b00ecede4431ae74ab6589a1064fd33b"
  },
  {
    "url": "assets/js/73.db8bc71f.js",
    "revision": "b5574bfa464635c20097a205d8b91980"
  },
  {
    "url": "assets/js/74.08e83a90.js",
    "revision": "9008998c70af1b18aecd26c4a2c3fb17"
  },
  {
    "url": "assets/js/75.46119b84.js",
    "revision": "6b900ef103b7ccb8cb066d45c3a9b2c8"
  },
  {
    "url": "assets/js/76.602e3acc.js",
    "revision": "0b336b01f45ca47aa47e812c78826e4b"
  },
  {
    "url": "assets/js/77.dd923a81.js",
    "revision": "e4a6a6de8a6dadc3c699612653c48311"
  },
  {
    "url": "assets/js/78.801b73bc.js",
    "revision": "d5c2634140cafae189f3e3c44947ccd7"
  },
  {
    "url": "assets/js/79.bddb250d.js",
    "revision": "4c89704e73ded0d64c15e677ebf301e9"
  },
  {
    "url": "assets/js/8.6151909e.js",
    "revision": "36067ca3f868a72e6f3ae43c93068b2a"
  },
  {
    "url": "assets/js/80.75273eb0.js",
    "revision": "f056fc6c2bd3ccdad2cca8de985ddec5"
  },
  {
    "url": "assets/js/81.5dbf1d9b.js",
    "revision": "6c3a2ae481ea7fd47300f69307eb9ec0"
  },
  {
    "url": "assets/js/82.6723248f.js",
    "revision": "8f08cdfaa2e397dba0f0b0bd087adc1e"
  },
  {
    "url": "assets/js/83.46b2eb21.js",
    "revision": "7f6d139ecda5327a80a050520ff3be40"
  },
  {
    "url": "assets/js/84.93af41b4.js",
    "revision": "7a03cd370134ec43c2cdb2246d91e947"
  },
  {
    "url": "assets/js/85.5068371c.js",
    "revision": "58cde65b4a5b0d49e607542e4b9ff97c"
  },
  {
    "url": "assets/js/86.757790f7.js",
    "revision": "a1f5d792d30deb61464ff36d9a47eefa"
  },
  {
    "url": "assets/js/87.3b08dca4.js",
    "revision": "bd08bde5e680bc983d9dfbe02e34096a"
  },
  {
    "url": "assets/js/88.961359da.js",
    "revision": "e7fae83ba499a4259c1f5221122963da"
  },
  {
    "url": "assets/js/89.a00ec3c5.js",
    "revision": "4e1c93a7c3e816724bf77185ad464155"
  },
  {
    "url": "assets/js/9.9f7b0cf9.js",
    "revision": "24dd82137f4e68a475fb61d8bfb54186"
  },
  {
    "url": "assets/js/90.75b27e14.js",
    "revision": "9a6a7f54f89c804d2e1f784c2f1bff4c"
  },
  {
    "url": "assets/js/91.e227d9f1.js",
    "revision": "8cb8f4cc01d0e998cf7c7d283566327c"
  },
  {
    "url": "assets/js/92.e90f3cb1.js",
    "revision": "9bbf5e70ff9412f1c9ea530d0c53ac13"
  },
  {
    "url": "assets/js/93.1a1dc759.js",
    "revision": "65773bcce4e1ebc633b0876909420bfd"
  },
  {
    "url": "assets/js/94.c5d79a0a.js",
    "revision": "ab9b990ba4c97388e392ecdb1aeb8ca6"
  },
  {
    "url": "assets/js/95.0e3a5bc9.js",
    "revision": "bde78e4b14ec67478221cf4516bff279"
  },
  {
    "url": "assets/js/96.3d651c55.js",
    "revision": "2d34133f7a7a484b3d973f0d7f6dd9f1"
  },
  {
    "url": "assets/js/97.c0235193.js",
    "revision": "ce7a2778cf995a864b41abe1eb31babb"
  },
  {
    "url": "assets/js/98.664492db.js",
    "revision": "86644a26cbbe6053da8f46686dca02ae"
  },
  {
    "url": "assets/js/99.de72ad58.js",
    "revision": "f4dce9233ba255767b5c0285f0b54810"
  },
  {
    "url": "assets/js/app.38788b32.js",
    "revision": "8908c4f198fb493eddb0b0648ecd0977"
  },
  {
    "url": "changelog.html",
    "revision": "927d16a97188cb6afac82b0a5c7eafcb"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "6946361616f683c8d941c8feb10cfdd7"
  },
  {
    "url": "guide/cqhttp-guide.html",
    "revision": "b95141513f55b7ed1f8c0bc5f2cf74a0"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "c9c9b79a1f2e203444371ec3ec7b551f"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "67bf39914b621c23d4ef577b4f2a3a65"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "86de3bac9f5ad539520f0fe141973fd1"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "c49768c7b16ebf4a575017ec10ee2c74"
  },
  {
    "url": "guide/ding-guide.html",
    "revision": "6e3913a729dc35c36fea4bc1a41c3b8b"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "4f9b190e3ada84fda850815a8a44fe0d"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "da9b334c915d30a8b9549f9d5a730aac"
  },
  {
    "url": "guide/index.html",
    "revision": "ccf1a0817a4e9d0417e3e84583e0bb29"
  },
  {
    "url": "guide/installation.html",
    "revision": "61cf5cc3bf6258ad25c22eed2e1bc90a"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "07df92b2e4fec69a80ddfbf968cc4687"
  },
  {
    "url": "guide/mirai-guide.html",
    "revision": "5c73a830988e25ae99ae86f5bac766ca"
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
    "revision": "d4b400b452e2560a1d3660f36ace604b"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/export-and-require.html",
    "revision": "17338c52c9840d91e6492d0b0b923951"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "2100aa0c82858ccebaab34ba04fbe08e"
  },
  {
    "url": "next/advanced/overloaded-handlers.html",
    "revision": "6d5af9c138a7edcbad78a3fd66cf2064"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "4c0d3c8baf5b2a44582c89d65ba5e4cb"
  },
  {
    "url": "next/advanced/publish-plugin.html",
    "revision": "35f5dcfc0eea7b756c197f7ff7de98d4"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "ec82872e70ccd74b57a68963dfc9c0df"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "4559376fa6924e1c0d6bdc8f63734d67"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "96d3f6176586540302aa249fef84cc67"
  },
  {
    "url": "next/api/adapters/ding.html",
    "revision": "0647be650554cd5716041544b998d7b8"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "408b13be899cd3a7ed3957b7175dcaad"
  },
  {
    "url": "next/api/adapters/mirai.html",
    "revision": "2e13172fd909393d86e358b36272d228"
  },
  {
    "url": "next/api/config.html",
    "revision": "1d66150569e6433f5613c67ef2cc5dea"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "10dbbf959dc8a5f302e54af6169ea4d0"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "bfd97a1945620fbd1aadca7213d557b9"
  },
  {
    "url": "next/api/drivers/quart.html",
    "revision": "508f7cb04d286ad5b97fa4321d1f5edb"
  },
  {
    "url": "next/api/exception.html",
    "revision": "3e65cb4a061c8edcc5b3268186425e2d"
  },
  {
    "url": "next/api/index.html",
    "revision": "3fa71a731351c8f779146ac0def50c24"
  },
  {
    "url": "next/api/log.html",
    "revision": "01c431027b98671186b0174fc797d0f7"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "9aadc8ef54cf28db7fbea0f3cc54cc30"
  },
  {
    "url": "next/api/message.html",
    "revision": "78bc22a7e3d88bfff9c49fff274debfa"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "1e5c9d27bfc7811de68854ae4a4331d7"
  },
  {
    "url": "next/api/permission.html",
    "revision": "bae11183ddca0c11dd2425a4f92df267"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "fee3bfdb59eb347e5ca961efbe12f3ba"
  },
  {
    "url": "next/api/rule.html",
    "revision": "98b1747339c7cc013ef653db8f29cecd"
  },
  {
    "url": "next/api/typing.html",
    "revision": "575ea838a250d023e2863a3c0d3d025c"
  },
  {
    "url": "next/api/utils.html",
    "revision": "cdf1d427b230bcb1095a6cc84894e80c"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "0e7b86e9487c57f6c1d7e728fcbe6ba6"
  },
  {
    "url": "next/guide/cqhttp-guide.html",
    "revision": "37fcec1d34699a5c31d3a48456ef836a"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "3f944c2c7c961b4866a9e4ff775e5c5f"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "557ec55aee4a5363d8d69dca41138c28"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "ffa7200426b8bfc95d12ab0497a8ab9d"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "9e8e3428e51947e20196301aeac2cf49"
  },
  {
    "url": "next/guide/ding-guide.html",
    "revision": "63e5351357c7f27e8e675c43372cd3c7"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "60a7539205e79d771050514677e2ed00"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "43517093acc3b368ed6e8c184b62376c"
  },
  {
    "url": "next/guide/index.html",
    "revision": "d86f61a1e4151e1f3458859c3b6c8ba7"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "97a381998d8cc236e0a75831d38f3d2d"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "6f5ac23e129c25e95778486205d4cd6f"
  },
  {
    "url": "next/guide/mirai-guide.html",
    "revision": "4fa6f4cc29691a9f6d0aae4ca82d62c6"
  },
  {
    "url": "next/index.html",
    "revision": "af0ceefbd60fffb9cc3f062ed387ffc2"
  },
  {
    "url": "plugin-store.html",
    "revision": "94f03818b068489c42895940cca32c41"
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
