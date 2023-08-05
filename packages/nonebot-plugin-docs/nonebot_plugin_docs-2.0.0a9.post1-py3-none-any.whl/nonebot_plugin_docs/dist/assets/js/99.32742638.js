(window.webpackJsonp=window.webpackJsonp||[]).push([[99],{546:function(t,e,v){"use strict";v.r(e);var s=v(21),_=Object(s.a)({},(function(){var t=this,e=t.$createElement,v=t._self._c||e;return v("ContentSlotsDistributor",{attrs:{"slot-key":t.$parent.slotKey}},[v("h1",{attrs:{id:"nonebot-message-模块"}},[v("a",{staticClass:"header-anchor",attrs:{href:"#nonebot-message-模块"}},[t._v("#")]),t._v(" NoneBot.message 模块")]),t._v(" "),v("h2",{attrs:{id:"事件处理"}},[v("a",{staticClass:"header-anchor",attrs:{href:"#事件处理"}},[t._v("#")]),t._v(" 事件处理")]),t._v(" "),v("p",[t._v("NoneBot 内部处理并按优先级分发事件给所有事件响应器，提供了多个插槽以进行事件的预处理等。")]),t._v(" "),v("h2",{attrs:{id:"event-preprocessor-func"}},[v("a",{staticClass:"header-anchor",attrs:{href:"#event-preprocessor-func"}},[t._v("#")]),t._v(" "),v("code",[t._v("event_preprocessor(func)")])]),t._v(" "),v("ul",[v("li",[v("p",[v("strong",[t._v("说明")])]),t._v(" "),v("p",[t._v("事件预处理。装饰一个函数，使它在每次接收到事件并分发给各响应器之前执行。")])]),t._v(" "),v("li",[v("p",[v("strong",[t._v("参数")])]),t._v(" "),v("p",[t._v("事件预处理函数接收三个参数。")]),t._v(" "),v("ul",[v("li",[v("p",[v("code",[t._v("bot: Bot")]),t._v(": Bot 对象")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("event: Event")]),t._v(": Event 对象")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("state: T_State")]),t._v(": 当前 State")])])])])]),t._v(" "),v("h2",{attrs:{id:"event-postprocessor-func"}},[v("a",{staticClass:"header-anchor",attrs:{href:"#event-postprocessor-func"}},[t._v("#")]),t._v(" "),v("code",[t._v("event_postprocessor(func)")])]),t._v(" "),v("ul",[v("li",[v("p",[v("strong",[t._v("说明")])]),t._v(" "),v("p",[t._v("事件后处理。装饰一个函数，使它在每次接收到事件并分发给各响应器之后执行。")])]),t._v(" "),v("li",[v("p",[v("strong",[t._v("参数")])]),t._v(" "),v("p",[t._v("事件后处理函数接收三个参数。")]),t._v(" "),v("ul",[v("li",[v("p",[v("code",[t._v("bot: Bot")]),t._v(": Bot 对象")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("event: Event")]),t._v(": Event 对象")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("state: T_State")]),t._v(": 当前事件运行前 State")])])])])]),t._v(" "),v("h2",{attrs:{id:"run-preprocessor-func"}},[v("a",{staticClass:"header-anchor",attrs:{href:"#run-preprocessor-func"}},[t._v("#")]),t._v(" "),v("code",[t._v("run_preprocessor(func)")])]),t._v(" "),v("ul",[v("li",[v("p",[v("strong",[t._v("说明")])]),t._v(" "),v("p",[t._v("运行预处理。装饰一个函数，使它在每次事件响应器运行前执行。")])]),t._v(" "),v("li",[v("p",[v("strong",[t._v("参数")])]),t._v(" "),v("p",[t._v("运行预处理函数接收四个参数。")]),t._v(" "),v("ul",[v("li",[v("p",[v("code",[t._v("matcher: Matcher")]),t._v(": 当前要运行的事件响应器")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("bot: Bot")]),t._v(": Bot 对象")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("event: Event")]),t._v(": Event 对象")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("state: T_State")]),t._v(": 当前 State")])])])])]),t._v(" "),v("h2",{attrs:{id:"run-postprocessor-func"}},[v("a",{staticClass:"header-anchor",attrs:{href:"#run-postprocessor-func"}},[t._v("#")]),t._v(" "),v("code",[t._v("run_postprocessor(func)")])]),t._v(" "),v("ul",[v("li",[v("p",[v("strong",[t._v("说明")])]),t._v(" "),v("p",[t._v("运行后处理。装饰一个函数，使它在每次事件响应器运行后执行。")])]),t._v(" "),v("li",[v("p",[v("strong",[t._v("参数")])]),t._v(" "),v("p",[t._v("运行后处理函数接收五个参数。")]),t._v(" "),v("ul",[v("li",[v("p",[v("code",[t._v("matcher: Matcher")]),t._v(": 运行完毕的事件响应器")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("exception: Optional[Exception]")]),t._v(": 事件响应器运行错误（如果存在）")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("bot: Bot")]),t._v(": Bot 对象")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("event: Event")]),t._v(": Event 对象")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("state: T_State")]),t._v(": 当前 State")])])])])]),t._v(" "),v("h2",{attrs:{id:"async-handle-event-bot-event"}},[v("a",{staticClass:"header-anchor",attrs:{href:"#async-handle-event-bot-event"}},[t._v("#")]),t._v(" "),v("em",[t._v("async")]),t._v(" "),v("code",[t._v("handle_event(bot, event)")])]),t._v(" "),v("ul",[v("li",[v("p",[v("strong",[t._v("说明")])]),t._v(" "),v("p",[t._v("处理一个事件。调用该函数以实现分发事件。")])]),t._v(" "),v("li",[v("p",[v("strong",[t._v("参数")])]),t._v(" "),v("ul",[v("li",[v("p",[v("code",[t._v("bot: Bot")]),t._v(": Bot 对象")])]),t._v(" "),v("li",[v("p",[v("code",[t._v("event: Event")]),t._v(": Event 对象")])])])]),t._v(" "),v("li",[v("p",[v("strong",[t._v("示例")])])])]),t._v(" "),v("div",{staticClass:"language-python line-numbers-mode"},[v("pre",{pre:!0,attrs:{class:"language-python"}},[v("code",[v("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("import")]),t._v(" asyncio\nasyncio"),v("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("create_task"),v("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("handle_event"),v("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("bot"),v("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" event"),v("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),v("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n")])]),t._v(" "),v("div",{staticClass:"line-numbers-wrapper"},[v("span",{staticClass:"line-number"},[t._v("1")]),v("br"),v("span",{staticClass:"line-number"},[t._v("2")]),v("br")])])])}),[],!1,null,null,null);e.default=_.exports}}]);