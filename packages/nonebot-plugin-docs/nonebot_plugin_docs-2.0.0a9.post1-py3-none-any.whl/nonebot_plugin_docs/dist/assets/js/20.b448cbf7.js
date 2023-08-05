(window.webpackJsonp=window.webpackJsonp||[]).push([[20],{467:function(t,e,s){"use strict";s.r(e);var v=s(21),_=Object(v.a)({},(function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("ContentSlotsDistributor",{attrs:{"slot-key":t.$parent.slotKey}},[s("h1",{attrs:{id:"nonebot-config-模块"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#nonebot-config-模块"}},[t._v("#")]),t._v(" NoneBot.config 模块")]),t._v(" "),s("h2",{attrs:{id:"配置"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#配置"}},[t._v("#")]),t._v(" 配置")]),t._v(" "),s("p",[t._v("NoneBot 使用 "),s("a",{attrs:{href:"https://pydantic-docs.helpmanual.io/",target:"_blank",rel:"noopener noreferrer"}},[t._v("pydantic"),s("OutboundLink")],1),t._v(" 以及 "),s("a",{attrs:{href:"https://saurabh-kumar.com/python-dotenv/",target:"_blank",rel:"noopener noreferrer"}},[t._v("python-dotenv"),s("OutboundLink")],1),t._v(" 来读取配置。")]),t._v(" "),s("p",[t._v("配置项需符合特殊格式或 json 序列化格式。详情见 "),s("a",{attrs:{href:"https://pydantic-docs.helpmanual.io/usage/types/",target:"_blank",rel:"noopener noreferrer"}},[t._v("pydantic Field Type"),s("OutboundLink")],1),t._v(" 文档。")]),t._v(" "),s("h2",{attrs:{id:"class-env"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#class-env"}},[t._v("#")]),t._v(" "),s("em",[t._v("class")]),t._v(" "),s("code",[t._v("Env")])]),t._v(" "),s("p",[t._v("基类："),s("code",[t._v("pydantic.env_settings.BaseSettings")])]),t._v(" "),s("p",[t._v("运行环境配置。大小写不敏感。")]),t._v(" "),s("p",[t._v("将会从 "),s("code",[t._v("nonebot.init 参数")]),t._v(" > "),s("code",[t._v("环境变量")]),t._v(" > "),s("code",[t._v(".env 环境配置文件")]),t._v(" 的优先级读取配置。")]),t._v(" "),s("h3",{attrs:{id:"environment"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#environment"}},[t._v("#")]),t._v(" "),s("code",[t._v("environment")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("str")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v('"prod"')])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("当前环境名。 NoneBot 将从 "),s("code",[t._v(".env.{environment}")]),t._v(" 文件中加载配置。")])])]),t._v(" "),s("h2",{attrs:{id:"class-config"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#class-config"}},[t._v("#")]),t._v(" "),s("em",[t._v("class")]),t._v(" "),s("code",[t._v("Config")])]),t._v(" "),s("p",[t._v("基类："),s("code",[t._v("nonebot.config.BaseConfig")])]),t._v(" "),s("p",[t._v("NoneBot 主要配置。大小写不敏感。")]),t._v(" "),s("p",[t._v("除了 NoneBot 的配置项外，还可以自行添加配置项到 "),s("code",[t._v(".env.{environment}")]),t._v(" 文件中。\n这些配置将会在 json 反序列化后一起带入 "),s("code",[t._v("Config")]),t._v(" 类中。")]),t._v(" "),s("h3",{attrs:{id:"driver"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#driver"}},[t._v("#")]),t._v(" "),s("code",[t._v("driver")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("str")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v('"nonebot.drivers.fastapi"')])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("NoneBot 运行所使用的 "),s("code",[t._v("Driver")]),t._v(" 。继承自 "),s("code",[t._v("nonebot.driver.BaseDriver")]),t._v(" 。")])])]),t._v(" "),s("h3",{attrs:{id:"host"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#host"}},[t._v("#")]),t._v(" "),s("code",[t._v("host")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("IPvAnyAddress")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v("127.0.0.1")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("NoneBot 的 HTTP 和 WebSocket 服务端监听的 IP/主机名。")])])]),t._v(" "),s("h3",{attrs:{id:"port"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#port"}},[t._v("#")]),t._v(" "),s("code",[t._v("port")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("int")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v("8080")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("NoneBot 的 HTTP 和 WebSocket 服务端监听的端口。")])])]),t._v(" "),s("h3",{attrs:{id:"debug"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#debug"}},[t._v("#")]),t._v(" "),s("code",[t._v("debug")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("bool")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v("False")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("是否以调试模式运行 NoneBot。")])])]),t._v(" "),s("h3",{attrs:{id:"api-root"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#api-root"}},[t._v("#")]),t._v(" "),s("code",[t._v("api_root")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("Dict[str, str]")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v("{}")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("以机器人 ID 为键，上报地址为值的字典，环境变量或文件中应使用 json 序列化。")])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("示例")])])])]),t._v(" "),s("div",{staticClass:"language-default line-numbers-mode"},[s("pre",{pre:!0,attrs:{class:"language-text"}},[s("code",[t._v('API_ROOT={"123456": "http://127.0.0.1:5700"}\n')])]),t._v(" "),s("div",{staticClass:"line-numbers-wrapper"},[s("span",{staticClass:"line-number"},[t._v("1")]),s("br")])]),s("h3",{attrs:{id:"api-timeout"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#api-timeout"}},[t._v("#")]),t._v(" "),s("code",[t._v("api_timeout")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("Optional[float]")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v("30.")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("API 请求超时时间，单位: 秒。")])])]),t._v(" "),s("h3",{attrs:{id:"access-token"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#access-token"}},[t._v("#")]),t._v(" "),s("code",[t._v("access_token")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("Optional[str]")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v("None")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("API 请求以及上报所需密钥，在请求头中携带。")])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("示例")])])])]),t._v(" "),s("div",{staticClass:"language-http line-numbers-mode"},[s("pre",{pre:!0,attrs:{class:"language-http"}},[s("code",[s("span",{pre:!0,attrs:{class:"token request-line"}},[s("span",{pre:!0,attrs:{class:"token property"}},[t._v("POST")]),t._v(" /cqhttp/ HTTP/1.1")]),t._v("\n"),s("span",{pre:!0,attrs:{class:"token header-name keyword"}},[t._v("Authorization:")]),t._v(" Bearer kSLuTF2GC2Q4q4ugm3\n")])]),t._v(" "),s("div",{staticClass:"line-numbers-wrapper"},[s("span",{staticClass:"line-number"},[t._v("1")]),s("br"),s("span",{staticClass:"line-number"},[t._v("2")]),s("br")])]),s("h3",{attrs:{id:"secret"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#secret"}},[t._v("#")]),t._v(" "),s("code",[t._v("secret")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("Optional[str]")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v("None")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("HTTP POST 形式上报所需签名，在请求头中携带。")])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("示例")])])])]),t._v(" "),s("div",{staticClass:"language-http line-numbers-mode"},[s("pre",{pre:!0,attrs:{class:"language-http"}},[s("code",[s("span",{pre:!0,attrs:{class:"token request-line"}},[s("span",{pre:!0,attrs:{class:"token property"}},[t._v("POST")]),t._v(" /cqhttp/ HTTP/1.1")]),t._v("\n"),s("span",{pre:!0,attrs:{class:"token header-name keyword"}},[t._v("X-Signature:")]),t._v(" sha1=f9ddd4863ace61e64f462d41ca311e3d2c1176e2\n")])]),t._v(" "),s("div",{staticClass:"line-numbers-wrapper"},[s("span",{staticClass:"line-number"},[t._v("1")]),s("br"),s("span",{staticClass:"line-number"},[t._v("2")]),s("br")])]),s("h3",{attrs:{id:"superusers"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#superusers"}},[t._v("#")]),t._v(" "),s("code",[t._v("superusers")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("Set[int]")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v("set()")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("机器人超级用户。")])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("示例")])])])]),t._v(" "),s("div",{staticClass:"language-default line-numbers-mode"},[s("pre",{pre:!0,attrs:{class:"language-text"}},[s("code",[t._v("SUPER_USERS=[12345789]\n")])]),t._v(" "),s("div",{staticClass:"line-numbers-wrapper"},[s("span",{staticClass:"line-number"},[t._v("1")]),s("br")])]),s("h3",{attrs:{id:"nickname"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#nickname"}},[t._v("#")]),t._v(" "),s("code",[t._v("nickname")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("Set[str]")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v("set()")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("机器人昵称。")])])]),t._v(" "),s("h3",{attrs:{id:"command-start"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#command-start"}},[t._v("#")]),t._v(" "),s("code",[t._v("command_start")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("Set[str]")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v('{"/"}')])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("命令的起始标记，用于判断一条消息是不是命令。")])])]),t._v(" "),s("h3",{attrs:{id:"command-sep"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#command-sep"}},[t._v("#")]),t._v(" "),s("code",[t._v("command_sep")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("Set[str]")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v('{"."}')])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("命令的分隔标记，用于将文本形式的命令切分为元组（实际的命令名）。")])])]),t._v(" "),s("h3",{attrs:{id:"session-expire-timeout"}},[s("a",{staticClass:"header-anchor",attrs:{href:"#session-expire-timeout"}},[t._v("#")]),t._v(" "),s("code",[t._v("session_expire_timeout")])]),t._v(" "),s("ul",[s("li",[s("p",[s("strong",[t._v("类型")]),t._v(": "),s("code",[t._v("timedelta")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("默认值")]),t._v(": "),s("code",[t._v("timedelta(minutes=2)")])])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("说明")])]),t._v(" "),s("p",[t._v("等待用户回复的超时时间。")])]),t._v(" "),s("li",[s("p",[s("strong",[t._v("示例")])])])]),t._v(" "),s("div",{staticClass:"language-default line-numbers-mode"},[s("pre",{pre:!0,attrs:{class:"language-text"}},[s("code",[t._v("SESSION_EXPIRE_TIMEOUT=120  # 单位: 秒\nSESSION_EXPIRE_TIMEOUT=[DD ][HH:MM]SS[.ffffff]\nSESSION_EXPIRE_TIMEOUT=P[DD]DT[HH]H[MM]M[SS]S  # ISO 8601\n")])]),t._v(" "),s("div",{staticClass:"line-numbers-wrapper"},[s("span",{staticClass:"line-number"},[t._v("1")]),s("br"),s("span",{staticClass:"line-number"},[t._v("2")]),s("br"),s("span",{staticClass:"line-number"},[t._v("3")]),s("br")])])])}),[],!1,null,null,null);e.default=_.exports}}]);