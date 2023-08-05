(window.webpackJsonp=window.webpackJsonp||[]).push([[147],{445:function(e,s,t){"use strict";t.r(s);var r=t(21),n=Object(r.a)({},(function(){var e=this,s=e.$createElement,t=e._self._c||s;return t("ContentSlotsDistributor",{attrs:{"slot-key":e.$parent.slotKey}},[t("h1",{attrs:{id:"cqhttp-协议使用指南"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#cqhttp-协议使用指南"}},[e._v("#")]),e._v(" CQHTTP 协议使用指南")]),e._v(" "),t("h2",{attrs:{id:"配置-cqhttp-协议端-以-qq-为例"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#配置-cqhttp-协议端-以-qq-为例"}},[e._v("#")]),e._v(" 配置 CQHTTP 协议端（以 QQ 为例）")]),e._v(" "),t("p",[e._v("单纯运行 NoneBot 实例并不会产生任何效果，因为此刻 QQ 这边还不知道 NoneBot 的存在，也就无法把消息发送给它，因此现在需要使用一个无头 QQ 来把消息等事件上报给 NoneBot。")]),e._v(" "),t("p",[e._v("QQ 协议端举例:")]),e._v(" "),t("ul",[t("li",[t("a",{attrs:{href:"https://github.com/Mrs4s/go-cqhttp",target:"_blank",rel:"noopener noreferrer"}},[e._v("go-cqhttp"),t("OutboundLink")],1),e._v(" (基于 "),t("a",{attrs:{href:"https://github.com/Mrs4s/MiraiGo",target:"_blank",rel:"noopener noreferrer"}},[e._v("MiraiGo"),t("OutboundLink")],1),e._v(")")]),e._v(" "),t("li",[t("a",{attrs:{href:"https://github.com/yyuueexxiinngg/cqhttp-mirai/tree/embedded",target:"_blank",rel:"noopener noreferrer"}},[e._v("cqhttp-mirai-embedded"),t("OutboundLink")],1)]),e._v(" "),t("li",[t("a",{attrs:{href:"https://github.com/mamoe/mirai",target:"_blank",rel:"noopener noreferrer"}},[e._v("Mirai"),t("OutboundLink")],1),e._v(" + "),t("a",{attrs:{href:"https://github.com/yyuueexxiinngg/cqhttp-mirai",target:"_blank",rel:"noopener noreferrer"}},[e._v("cqhttp-mirai"),t("OutboundLink")],1)]),e._v(" "),t("li",[t("a",{attrs:{href:"https://github.com/mamoe/mirai",target:"_blank",rel:"noopener noreferrer"}},[e._v("Mirai"),t("OutboundLink")],1),e._v(" + "),t("a",{attrs:{href:"https://github.com/iTXTech/mirai-native",target:"_blank",rel:"noopener noreferrer"}},[e._v("Mirai Native"),t("OutboundLink")],1),e._v(" + "),t("a",{attrs:{href:"https://github.com/richardchien/coolq-http-api",target:"_blank",rel:"noopener noreferrer"}},[e._v("CQHTTP"),t("OutboundLink")],1)]),e._v(" "),t("li",[t("a",{attrs:{href:"https://github.com/takayama-lily/onebot",target:"_blank",rel:"noopener noreferrer"}},[e._v("OICQ-http-api"),t("OutboundLink")],1),e._v(" (基于 "),t("a",{attrs:{href:"https://github.com/takayama-lily/oicq",target:"_blank",rel:"noopener noreferrer"}},[e._v("OICQ"),t("OutboundLink")],1),e._v(")")])]),e._v(" "),t("p",[e._v("这里以 "),t("a",{attrs:{href:"https://github.com/Mrs4s/go-cqhttp",target:"_blank",rel:"noopener noreferrer"}},[e._v("go-cqhttp"),t("OutboundLink")],1),e._v(" 为例")]),e._v(" "),t("ol",[t("li",[e._v("下载 go-cqhttp 对应平台的 release 文件，"),t("a",{attrs:{href:"https://github.com/Mrs4s/go-cqhttp/releases",target:"_blank",rel:"noopener noreferrer"}},[e._v("点此前往"),t("OutboundLink")],1)]),e._v(" "),t("li",[e._v("运行 exe 文件或者使用 "),t("code",[e._v("./go-cqhttp")]),e._v(" 启动")]),e._v(" "),t("li",[e._v("生成默认配置文件并修改默认配置")])]),e._v(" "),t("div",{staticClass:"language-hjson line-numbers-mode"},[t("div",{staticClass:"highlight-lines"},[t("br"),t("div",{staticClass:"highlighted"},[e._v(" ")]),t("div",{staticClass:"highlighted"},[e._v(" ")]),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("div",{staticClass:"highlighted"},[e._v(" ")]),t("div",{staticClass:"highlighted"},[e._v(" ")]),t("br"),t("br"),t("br"),t("br"),t("br"),t("div",{staticClass:"highlighted"},[e._v(" ")]),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br"),t("br")]),t("pre",{pre:!0,attrs:{class:"language-text"}},[t("code",[e._v('{\n  uin: 机器人QQ号\n  password: 机器人密码\n  encrypt_password: false\n  password_encrypted: ""\n  enable_db: true\n  access_token: ""\n  relogin: {\n    enabled: true\n    relogin_delay: 3\n    max_relogin_times: 0\n  }\n  _rate_limit: {\n    enabled: false\n    frequency: 1\n    bucket_size: 1\n  }\n  ignore_invalid_cqcode: false\n  force_fragmented: false\n  heartbeat_interval: 0\n  http_config: {\n    enabled: false\n    host: "0.0.0.0"\n    port: 5700\n    timeout: 0\n    post_urls: {}\n  }\n  ws_config: {\n    enabled: false\n    host: "0.0.0.0"\n    port: 6700\n  }\n  ws_reverse_servers: [\n    {\n      enabled: true\n      reverse_url: ws://127.0.0.1:8080/cqhttp/ws\n      reverse_api_url: ws://you_websocket_api.server\n      reverse_event_url: ws://you_websocket_event.server\n      reverse_reconnect_interval: 3000\n    }\n  ]\n  post_message_format: array\n  use_sso_address: false\n  debug: false\n  log_level: ""\n  web_ui: {\n    enabled: false\n    host: 127.0.0.1\n    web_ui_port: 9999\n    web_input: false\n  }\n}\n')])]),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[e._v("1")]),t("br"),t("span",{staticClass:"line-number"},[e._v("2")]),t("br"),t("span",{staticClass:"line-number"},[e._v("3")]),t("br"),t("span",{staticClass:"line-number"},[e._v("4")]),t("br"),t("span",{staticClass:"line-number"},[e._v("5")]),t("br"),t("span",{staticClass:"line-number"},[e._v("6")]),t("br"),t("span",{staticClass:"line-number"},[e._v("7")]),t("br"),t("span",{staticClass:"line-number"},[e._v("8")]),t("br"),t("span",{staticClass:"line-number"},[e._v("9")]),t("br"),t("span",{staticClass:"line-number"},[e._v("10")]),t("br"),t("span",{staticClass:"line-number"},[e._v("11")]),t("br"),t("span",{staticClass:"line-number"},[e._v("12")]),t("br"),t("span",{staticClass:"line-number"},[e._v("13")]),t("br"),t("span",{staticClass:"line-number"},[e._v("14")]),t("br"),t("span",{staticClass:"line-number"},[e._v("15")]),t("br"),t("span",{staticClass:"line-number"},[e._v("16")]),t("br"),t("span",{staticClass:"line-number"},[e._v("17")]),t("br"),t("span",{staticClass:"line-number"},[e._v("18")]),t("br"),t("span",{staticClass:"line-number"},[e._v("19")]),t("br"),t("span",{staticClass:"line-number"},[e._v("20")]),t("br"),t("span",{staticClass:"line-number"},[e._v("21")]),t("br"),t("span",{staticClass:"line-number"},[e._v("22")]),t("br"),t("span",{staticClass:"line-number"},[e._v("23")]),t("br"),t("span",{staticClass:"line-number"},[e._v("24")]),t("br"),t("span",{staticClass:"line-number"},[e._v("25")]),t("br"),t("span",{staticClass:"line-number"},[e._v("26")]),t("br"),t("span",{staticClass:"line-number"},[e._v("27")]),t("br"),t("span",{staticClass:"line-number"},[e._v("28")]),t("br"),t("span",{staticClass:"line-number"},[e._v("29")]),t("br"),t("span",{staticClass:"line-number"},[e._v("30")]),t("br"),t("span",{staticClass:"line-number"},[e._v("31")]),t("br"),t("span",{staticClass:"line-number"},[e._v("32")]),t("br"),t("span",{staticClass:"line-number"},[e._v("33")]),t("br"),t("span",{staticClass:"line-number"},[e._v("34")]),t("br"),t("span",{staticClass:"line-number"},[e._v("35")]),t("br"),t("span",{staticClass:"line-number"},[e._v("36")]),t("br"),t("span",{staticClass:"line-number"},[e._v("37")]),t("br"),t("span",{staticClass:"line-number"},[e._v("38")]),t("br"),t("span",{staticClass:"line-number"},[e._v("39")]),t("br"),t("span",{staticClass:"line-number"},[e._v("40")]),t("br"),t("span",{staticClass:"line-number"},[e._v("41")]),t("br"),t("span",{staticClass:"line-number"},[e._v("42")]),t("br"),t("span",{staticClass:"line-number"},[e._v("43")]),t("br"),t("span",{staticClass:"line-number"},[e._v("44")]),t("br"),t("span",{staticClass:"line-number"},[e._v("45")]),t("br"),t("span",{staticClass:"line-number"},[e._v("46")]),t("br"),t("span",{staticClass:"line-number"},[e._v("47")]),t("br"),t("span",{staticClass:"line-number"},[e._v("48")]),t("br"),t("span",{staticClass:"line-number"},[e._v("49")]),t("br"),t("span",{staticClass:"line-number"},[e._v("50")]),t("br"),t("span",{staticClass:"line-number"},[e._v("51")]),t("br"),t("span",{staticClass:"line-number"},[e._v("52")]),t("br")])]),t("p",[e._v("其中 "),t("code",[e._v("ws://127.0.0.1:8080/cqhttp/ws")]),e._v(" 中的 "),t("code",[e._v("127.0.0.1")]),e._v(" 和 "),t("code",[e._v("8080")]),e._v(" 应分别对应 nonebot 配置的 HOST 和 PORT。")]),e._v(" "),t("p",[t("code",[e._v("cqhttp")]),e._v(" 是前述 "),t("code",[e._v("register_adapter")]),e._v(" 时传入的第一个参数，代表设置的 "),t("code",[e._v("CQHTTPBot")]),e._v(" 适配器的路径，你可以对不同的适配器设置不同路径以作区别。")]),e._v(" "),t("h2",{attrs:{id:"历史性的第一次对话"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#历史性的第一次对话"}},[e._v("#")]),e._v(" 历史性的第一次对话")]),e._v(" "),t("p",[e._v("一旦新的配置文件正确生效之后，NoneBot 所在的控制台（如果正在运行的话）应该会输出类似下面的内容（两条访问日志）：")]),e._v(" "),t("div",{staticClass:"language-default line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-text"}},[t("code",[e._v("09-14 21:31:16 [INFO] uvicorn | ('127.0.0.1', 12345) - \"WebSocket /cqhttp/ws\" [accepted]\n09-14 21:31:16 [INFO] nonebot | WebSocket Connection from CQHTTP Bot 你的QQ号 Accepted!\n")])]),e._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[e._v("1")]),t("br"),t("span",{staticClass:"line-number"},[e._v("2")]),t("br")])]),t("p",[e._v("这表示 CQHTTP 协议端已经成功地使用 CQHTTP 协议连接上了 NoneBot。")]),e._v(" "),t("p",[e._v("现在，尝试向你的机器人账号发送如下内容：")]),e._v(" "),t("div",{staticClass:"language-default line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-text"}},[t("code",[e._v("/echo 你好，世界\n")])]),e._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[e._v("1")]),t("br")])]),t("p",[e._v("到这里如果一切 OK，你应该会收到机器人给你回复了 "),t("code",[e._v("你好，世界")]),e._v("。这一历史性的对话标志着你已经成功地运行了一个 NoneBot 的最小实例，开始了编写更强大的 QQ 机器人的创意之旅！")]),e._v(" "),t("ClientOnly",[t("Messenger",{attrs:{messages:[{position:"right",msg:"/echo 你好，世界"},{position:"left",msg:"你好，世界"}]}})],1)],1)}),[],!1,null,null,null);s.default=n.exports}}]);