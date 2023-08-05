(window.webpackJsonp=window.webpackJsonp||[]).push([[152],{450:function(t,s,n){"use strict";n.r(s);var a=n(21),e=Object(a.a)({},(function(){var t=this,s=t.$createElement,n=t._self._c||s;return n("ContentSlotsDistributor",{attrs:{"slot-key":t.$parent.slotKey}},[n("h1",{attrs:{id:"钉钉机器人使用指南"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#钉钉机器人使用指南"}},[t._v("#")]),t._v(" 钉钉机器人使用指南")]),t._v(" "),n("p",[t._v("基于企业机器人的 outgoing（回调）机制，用户@机器人之后，钉钉会将消息内容 POST 到开发者的消息接收地址。开发者解析出消息内容、发送者身份，根据企业的业务逻辑，组装响应的消息内容返回，钉钉会将响应内容发送到群里。")]),t._v(" "),n("div",{staticClass:"custom-block warning"},[n("p",{staticClass:"custom-block-title"},[t._v("只有企业内部机器人支持接收消息")]),t._v(" "),n("p",[t._v("普通的机器人尚不支持应答机制，该机制指的是群里成员在聊天@机器人的时候，钉钉回调指定的服务地址，即 Outgoing 机器人。")])]),t._v(" "),n("p",[t._v("首先你需要有钉钉机器人的相关概念，请参阅相关文档：")]),t._v(" "),n("ul",[n("li",[n("a",{attrs:{href:"https://developers.dingtalk.com/document/app/overview-of-group-robots",target:"_blank",rel:"noopener noreferrer"}},[t._v("群机器人概述"),n("OutboundLink")],1)]),t._v(" "),n("li",[n("a",{attrs:{href:"https://developers.dingtalk.com/document/app/develop-enterprise-internal-robots",target:"_blank",rel:"noopener noreferrer"}},[t._v("开发企业内部机器人"),n("OutboundLink")],1)])]),t._v(" "),n("h2",{attrs:{id:"关于-dingadapter-的说明"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#关于-dingadapter-的说明"}},[t._v("#")]),t._v(" 关于 DingAdapter 的说明")]),t._v(" "),n("p",[t._v("你需要显式的注册 ding 这个适配器：")]),t._v(" "),n("div",{staticClass:"language-python line-numbers-mode"},[n("div",{staticClass:"highlight-lines"},[n("br"),n("div",{staticClass:"highlighted"},[t._v(" ")]),n("br"),n("br"),n("br"),n("div",{staticClass:"highlighted"},[t._v(" ")]),n("br"),n("br"),n("br"),n("br"),n("br")]),n("pre",{pre:!0,attrs:{class:"language-python"}},[n("code",[n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("import")]),t._v(" nonebot\n"),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("from")]),t._v(" nonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("adapters"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("ding "),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("import")]),t._v(" Bot "),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("as")]),t._v(" DingBot\n\nnonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("init"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\ndriver "),n("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" nonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("get_driver"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\ndriver"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("register_adapter"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('"ding"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" DingBot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\nnonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("load_builtin_plugins"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n\n"),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("if")]),t._v(" __name__ "),n("span",{pre:!0,attrs:{class:"token operator"}},[t._v("==")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('"__main__"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n    nonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("run"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n")])]),n("div",{staticClass:"line-numbers-wrapper"},[n("span",{staticClass:"line-number"},[t._v("1")]),n("br"),n("span",{staticClass:"line-number"},[t._v("2")]),n("br"),n("span",{staticClass:"line-number"},[t._v("3")]),n("br"),n("span",{staticClass:"line-number"},[t._v("4")]),n("br"),n("span",{staticClass:"line-number"},[t._v("5")]),n("br"),n("span",{staticClass:"line-number"},[t._v("6")]),n("br"),n("span",{staticClass:"line-number"},[t._v("7")]),n("br"),n("span",{staticClass:"line-number"},[t._v("8")]),n("br"),n("span",{staticClass:"line-number"},[t._v("9")]),n("br"),n("span",{staticClass:"line-number"},[t._v("10")]),n("br")])]),n("p",[t._v("注册适配器的目的是将 "),n("code",[t._v("/ding")]),t._v(" 这个路径挂载到程序上，并且和 DingBot 适配器关联起来。之后钉钉把收到的消息回调到 "),n("code",[t._v("http://xx.xxx.xxx.xxx:{port}/ding")]),t._v(" 时，Nonebot 才知道要用什么适配器去处理该消息。")]),t._v(" "),n("h2",{attrs:{id:"第一个命令"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#第一个命令"}},[t._v("#")]),t._v(" 第一个命令")]),t._v(" "),n("p",[t._v("因为 Nonebot 可以根据你的命令处理函数的类型注解来选择使用什么 Adapter 进行处理，所以你如果需要使用钉钉相关的功能，你的 handler 中 "),n("code",[t._v("bot")]),t._v(" 类型的注解需要是 DingBot 及其父类。")]),t._v(" "),n("p",[t._v("对于 Event 来说也是如此，Event 也可以根据标注来判断，比如一个 handler 的 event 标注位 "),n("code",[t._v("PrivateMessageEvent")]),t._v("，那这个 handler 只会处理私聊消息。")]),t._v(" "),n("p",[t._v("举个栗子：")]),t._v(" "),n("div",{staticClass:"language-python line-numbers-mode"},[n("pre",{pre:!0,attrs:{class:"language-python"}},[n("code",[t._v("test "),n("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" on_command"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('"test"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" to_me"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n\n\n"),n("span",{pre:!0,attrs:{class:"token decorator annotation punctuation"}},[t._v("@test"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("handle")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n"),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("async")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("def")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token function"}},[t._v("test_handler1")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("bot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" DingBot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" event"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" PrivateMessageEvent"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n    "),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("await")]),t._v(" test"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("finish"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('"PrivateMessageEvent"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n\n\n"),n("span",{pre:!0,attrs:{class:"token decorator annotation punctuation"}},[t._v("@test"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("handle")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n"),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("async")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("def")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token function"}},[t._v("test_handler2")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("bot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" DingBot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" event"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" GroupMessageEvent"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n    "),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("await")]),t._v(" test"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("finish"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('"GroupMessageEvent"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n")])]),t._v(" "),n("div",{staticClass:"line-numbers-wrapper"},[n("span",{staticClass:"line-number"},[t._v("1")]),n("br"),n("span",{staticClass:"line-number"},[t._v("2")]),n("br"),n("span",{staticClass:"line-number"},[t._v("3")]),n("br"),n("span",{staticClass:"line-number"},[t._v("4")]),n("br"),n("span",{staticClass:"line-number"},[t._v("5")]),n("br"),n("span",{staticClass:"line-number"},[t._v("6")]),n("br"),n("span",{staticClass:"line-number"},[t._v("7")]),n("br"),n("span",{staticClass:"line-number"},[t._v("8")]),n("br"),n("span",{staticClass:"line-number"},[t._v("9")]),n("br"),n("span",{staticClass:"line-number"},[t._v("10")]),n("br"),n("span",{staticClass:"line-number"},[t._v("11")]),n("br")])]),n("p",[t._v("这样 Nonebot 就会根据不同的类型注解使用不同的 handler 来处理消息。")]),t._v(" "),n("p",[t._v("可以查看 Nonebot 官方的这个例子："),n("a",{attrs:{href:"https://github.com/nonebot/nonebot2/tree/dev/tests",target:"_blank",rel:"noopener noreferrer"}},[t._v("https://github.com/nonebot/nonebot2/tree/dev/tests"),n("OutboundLink")],1),t._v("，更详细的了解一个 Bot 的结构。")]),t._v(" "),n("h2",{attrs:{id:"多种消息格式"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#多种消息格式"}},[t._v("#")]),t._v(" 多种消息格式")]),t._v(" "),n("p",[t._v("发送 markdown 消息：")]),t._v(" "),n("div",{staticClass:"language-python line-numbers-mode"},[n("pre",{pre:!0,attrs:{class:"language-python"}},[n("code",[n("span",{pre:!0,attrs:{class:"token decorator annotation punctuation"}},[t._v("@markdown"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("handle")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n"),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("async")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("def")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token function"}},[t._v("markdown_handler")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("bot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" DingBot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n    message "),n("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" MessageSegment"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("markdown"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("\n        "),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('"Hello, This is NoneBot"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n        "),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('"#### NoneBot  \\n> Nonebot 是一款高性能的 Python 机器人框架\\n> ![screenshot](https://v2.nonebot.dev/logo.png)\\n> [GitHub 仓库地址](https://github.com/nonebot/nonebot2) \\n"')]),t._v("\n    "),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n    "),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("await")]),t._v(" markdown"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("finish"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("message"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n")])]),t._v(" "),n("div",{staticClass:"line-numbers-wrapper"},[n("span",{staticClass:"line-number"},[t._v("1")]),n("br"),n("span",{staticClass:"line-number"},[t._v("2")]),n("br"),n("span",{staticClass:"line-number"},[t._v("3")]),n("br"),n("span",{staticClass:"line-number"},[t._v("4")]),n("br"),n("span",{staticClass:"line-number"},[t._v("5")]),n("br"),n("span",{staticClass:"line-number"},[t._v("6")]),n("br"),n("span",{staticClass:"line-number"},[t._v("7")]),n("br")])]),n("p",[t._v("可以按自己的需要发送原生的格式消息（需要使用 "),n("code",[t._v("MessageSegment")]),t._v(" 包裹，可以很方便的实现 @ 等操作）：")]),t._v(" "),n("div",{staticClass:"language-python line-numbers-mode"},[n("pre",{pre:!0,attrs:{class:"language-python"}},[n("code",[n("span",{pre:!0,attrs:{class:"token decorator annotation punctuation"}},[t._v("@raw"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("handle")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n"),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("async")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("def")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token function"}},[t._v("raw_handler")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("bot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" DingBot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" event"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" MessageEvent"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n    message "),n("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" MessageSegment"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("raw"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n        "),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('"msgtype"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('"text"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n        "),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('"text"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n            "),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('"content"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),n("span",{pre:!0,attrs:{class:"token string-interpolation"}},[n("span",{pre:!0,attrs:{class:"token string"}},[t._v('f"@')]),n("span",{pre:!0,attrs:{class:"token interpolation"}},[n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("event"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("senderId"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")])]),n("span",{pre:!0,attrs:{class:"token string"}},[t._v('，你好"')])]),t._v("\n        "),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n    "),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n    message "),n("span",{pre:!0,attrs:{class:"token operator"}},[t._v("+=")]),t._v(" MessageSegment"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("atDingtalkIds"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("event"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("senderId"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n    "),n("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("await")]),t._v(" raw"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("send"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("message"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n")])]),t._v(" "),n("div",{staticClass:"line-numbers-wrapper"},[n("span",{staticClass:"line-number"},[t._v("1")]),n("br"),n("span",{staticClass:"line-number"},[t._v("2")]),n("br"),n("span",{staticClass:"line-number"},[t._v("3")]),n("br"),n("span",{staticClass:"line-number"},[t._v("4")]),n("br"),n("span",{staticClass:"line-number"},[t._v("5")]),n("br"),n("span",{staticClass:"line-number"},[t._v("6")]),n("br"),n("span",{staticClass:"line-number"},[t._v("7")]),n("br"),n("span",{staticClass:"line-number"},[t._v("8")]),n("br"),n("span",{staticClass:"line-number"},[t._v("9")]),n("br"),n("span",{staticClass:"line-number"},[t._v("10")]),n("br")])]),n("p",[t._v("其他消息格式请查看 "),n("a",{attrs:{href:"https://github.com/nonebot/nonebot2/blob/dev/nonebot/adapters/ding/message.py#L8",target:"_blank",rel:"noopener noreferrer"}},[t._v("钉钉适配器的 MessageSegment"),n("OutboundLink")],1),t._v("，里面封装了很多有关消息的方法，比如 "),n("code",[t._v("code")]),t._v("、"),n("code",[t._v("image")]),t._v("、"),n("code",[t._v("feedCard")]),t._v(" 等。")]),t._v(" "),n("h2",{attrs:{id:"创建机器人并连接"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#创建机器人并连接"}},[t._v("#")]),t._v(" 创建机器人并连接")]),t._v(" "),n("p",[t._v("在钉钉官方文档 "),n("a",{attrs:{href:"https://developers.dingtalk.com/document/app/develop-enterprise-internal-robots/title-ufs-4gh-poh",target:"_blank",rel:"noopener noreferrer"}},[t._v("「开发企业内部机器人 -> 步骤一：创建机器人应用」"),n("OutboundLink")],1),t._v(" 中有详细介绍，这里就省去创建的步骤，介绍一下如何连接上程序。")]),t._v(" "),n("h3",{attrs:{id:"本地开发机器人"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#本地开发机器人"}},[t._v("#")]),t._v(" 本地开发机器人")]),t._v(" "),n("p",[t._v("在本地开发机器人的时候可能没有公网 IP，钉钉官方给我们提供一个 "),n("a",{attrs:{href:"https://developers.dingtalk.com/document/resourcedownload/http-intranet-penetration?pnamespace=app",target:"_blank",rel:"noopener noreferrer"}},[t._v("内网穿透工具"),n("OutboundLink")],1),t._v("，方便开发测试。")]),t._v(" "),n("div",{staticClass:"custom-block tip"},[n("p",{staticClass:"custom-block-title"},[t._v("TIP")]),t._v(" "),n("p",[t._v("究其根源这是一个魔改版的 ngrok，钉钉提供了一个服务器。")]),t._v(" "),n("p",[t._v("本工具不保证稳定性，仅适用于开发测试阶段，禁止当作公网域名使用。如线上应用使用本工具造成稳定性问题，后果由自己承担。如使用本工具传播违法不良信息，钉钉将追究法律责任。")])]),t._v(" "),n("p",[t._v("官方文档里已经讲了如何使用。我们再以 Windows（终端使用 Powershell） 为例，来演示一下。")]),t._v(" "),n("ol",[n("li",[t._v("将仓库 clone 到本地，打开 "),n("code",[t._v("windows_64")]),t._v(" 文件夹。")]),t._v(" "),n("li",[t._v("执行 "),n("code",[t._v('.\\ding.exe -config="./ding.cfg" -subdomain=rcnb 8080')]),t._v(" 就可以将 8080 端口暴露到公网中。"),n("br"),t._v("\n你访问 "),n("a",{attrs:{href:"http://rcnb.vaiwan.com/xxxxx",target:"_blank",rel:"noopener noreferrer"}},[t._v("http://rcnb.vaiwan.com/xxxxx"),n("OutboundLink")],1),t._v(" 都会映射到 "),n("a",{attrs:{href:"http://127.0.0.1:8080/xxxxx",target:"_blank",rel:"noopener noreferrer"}},[t._v("http://127.0.0.1:8080/xxxxx"),n("OutboundLink")],1),t._v("。")])]),t._v(" "),n("p",[t._v("假设我们的机器人监听的端口是 "),n("code",[t._v("2333")]),t._v("，并且已经注册了钉钉适配器。那我们就执行 "),n("code",[t._v('.\\ding.exe -config="./ding.cfg" -subdomain=rcnb 2333')]),t._v("，然后在机器人的后台设置 POST 的地址："),n("code",[t._v("http://rcnb.vaiwan.com/ding")]),t._v("。"),n("br"),t._v("\n这样钉钉接收到消息之后就会 POST 消息到 "),n("code",[t._v("http://rcnb.vaiwan.com/ding")]),t._v(" 上，然后这个服务会把消息再转发到我们本地的开发服务器上。")]),t._v(" "),n("h3",{attrs:{id:"生产模式"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#生产模式"}},[t._v("#")]),t._v(" 生产模式")]),t._v(" "),n("p",[t._v("生产模式你的机器需要有一个公网 IP，然后到机器人的后台设置 POST 的地址就好了。")]),t._v(" "),n("h2",{attrs:{id:"示例"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#示例"}},[t._v("#")]),t._v(" 示例")]),t._v(" "),n("p",[t._v("关于钉钉机器人能做啥，你可以查看 "),n("code",[t._v("https://github.com/nonebot/nonebot2/blob/dev/tests/test_plugins/test_ding.py")]),t._v("，里面有一些例子。")])])}),[],!1,null,null,null);s.default=e.exports}}]);