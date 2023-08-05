(window.webpackJsonp=window.webpackJsonp||[]).push([[117],{564:function(s,t,n){"use strict";n.r(t);var a=n(21),e=Object(a.a)({},(function(){var s=this,t=s.$createElement,n=s._self._c||t;return n("ContentSlotsDistributor",{attrs:{"slot-key":s.$parent.slotKey}},[n("h1",{attrs:{id:"加载插件"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#加载插件"}},[s._v("#")]),s._v(" 加载插件")]),s._v(" "),n("p",[s._v("在 "),n("a",{attrs:{href:"creating-a-project"}},[s._v("创建一个完整的项目")]),s._v(" 一章节中，我们已经创建了插件目录 "),n("code",[s._v("awesome_bot/plugins")]),s._v("，现在我们在机器人入口文件中加载它。当然，你也可以单独加载一个插件。")]),s._v(" "),n("h2",{attrs:{id:"加载内置插件"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#加载内置插件"}},[s._v("#")]),s._v(" 加载内置插件")]),s._v(" "),n("p",[s._v("在 "),n("code",[s._v("bot.py")]),s._v(" 文件中添加以下行：")]),s._v(" "),n("div",{staticClass:"language-python line-numbers-mode"},[n("div",{staticClass:"highlight-lines"},[n("br"),n("br"),n("br"),n("br"),n("div",{staticClass:"highlighted"},[s._v(" ")]),n("br"),n("br"),n("br"),n("br"),n("br"),n("br")]),n("pre",{pre:!0,attrs:{class:"language-python"}},[n("code",[n("span",{pre:!0,attrs:{class:"token keyword"}},[s._v("import")]),s._v(" nonebot\n\nnonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("init"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n"),n("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 加载 nonebot 内置插件")]),s._v("\nnonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("load_builtin_plugins"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n\napp "),n("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" nonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("get_asgi"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n\n"),n("span",{pre:!0,attrs:{class:"token keyword"}},[s._v("if")]),s._v(" __name__ "),n("span",{pre:!0,attrs:{class:"token operator"}},[s._v("==")]),s._v(" "),n("span",{pre:!0,attrs:{class:"token string"}},[s._v('"__main__"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n    nonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("run"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n")])]),n("div",{staticClass:"line-numbers-wrapper"},[n("span",{staticClass:"line-number"},[s._v("1")]),n("br"),n("span",{staticClass:"line-number"},[s._v("2")]),n("br"),n("span",{staticClass:"line-number"},[s._v("3")]),n("br"),n("span",{staticClass:"line-number"},[s._v("4")]),n("br"),n("span",{staticClass:"line-number"},[s._v("5")]),n("br"),n("span",{staticClass:"line-number"},[s._v("6")]),n("br"),n("span",{staticClass:"line-number"},[s._v("7")]),n("br"),n("span",{staticClass:"line-number"},[s._v("8")]),n("br"),n("span",{staticClass:"line-number"},[s._v("9")]),n("br"),n("span",{staticClass:"line-number"},[s._v("10")]),n("br")])]),n("p",[s._v("这将会加载 nonebot 内置的插件，它包含：")]),s._v(" "),n("ul",[n("li",[s._v("命令 "),n("code",[s._v("say")]),s._v("：可由"),n("strong",[s._v("superuser")]),s._v("使用，可以将消息内容由特殊纯文本转为富文本")]),s._v(" "),n("li",[s._v("命令 "),n("code",[s._v("echo")]),s._v("：可由任何人使用，将消息原样返回")])]),s._v(" "),n("p",[s._v("以上命令均需要指定机器人，即私聊、群聊内@机器人、群聊内称呼机器人昵称。参考 "),n("router-link",{attrs:{to:"./../api/rule.html#to-me"}},[s._v("Rule: to_me")])],1),s._v(" "),n("h2",{attrs:{id:"加载插件目录"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#加载插件目录"}},[s._v("#")]),s._v(" 加载插件目录")]),s._v(" "),n("p",[s._v("在 "),n("code",[s._v("bot.py")]),s._v(" 文件中添加以下行：")]),s._v(" "),n("div",{staticClass:"language-python line-numbers-mode"},[n("div",{staticClass:"highlight-lines"},[n("br"),n("br"),n("br"),n("br"),n("div",{staticClass:"highlighted"},[s._v(" ")]),n("br"),n("br"),n("br"),n("br"),n("br"),n("br")]),n("pre",{pre:!0,attrs:{class:"language-python"}},[n("code",[n("span",{pre:!0,attrs:{class:"token keyword"}},[s._v("import")]),s._v(" nonebot\n\nnonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("init"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n"),n("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 加载插件目录，该目录下为各插件，以下划线开头的插件将不会被加载")]),s._v("\nnonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("load_plugins"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token string"}},[s._v('"awesome_bot/plugins"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n\napp "),n("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" nonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("get_asgi"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n\n"),n("span",{pre:!0,attrs:{class:"token keyword"}},[s._v("if")]),s._v(" __name__ "),n("span",{pre:!0,attrs:{class:"token operator"}},[s._v("==")]),s._v(" "),n("span",{pre:!0,attrs:{class:"token string"}},[s._v('"__main__"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n    nonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("run"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n")])]),n("div",{staticClass:"line-numbers-wrapper"},[n("span",{staticClass:"line-number"},[s._v("1")]),n("br"),n("span",{staticClass:"line-number"},[s._v("2")]),n("br"),n("span",{staticClass:"line-number"},[s._v("3")]),n("br"),n("span",{staticClass:"line-number"},[s._v("4")]),n("br"),n("span",{staticClass:"line-number"},[s._v("5")]),n("br"),n("span",{staticClass:"line-number"},[s._v("6")]),n("br"),n("span",{staticClass:"line-number"},[s._v("7")]),n("br"),n("span",{staticClass:"line-number"},[s._v("8")]),n("br"),n("span",{staticClass:"line-number"},[s._v("9")]),n("br"),n("span",{staticClass:"line-number"},[s._v("10")]),n("br")])]),n("div",{staticClass:"custom-block tip"},[n("p",{staticClass:"custom-block-title"},[s._v("提示")]),s._v(" "),n("p",[s._v("加载插件目录时，目录下以 "),n("code",[s._v("_")]),s._v(" 下划线开头的插件将不会被加载！")])]),s._v(" "),n("div",{staticClass:"custom-block warning"},[n("p",{staticClass:"custom-block-title"},[s._v("提示")]),s._v(" "),n("p",[n("strong",[s._v("不能存在相同名称的插件！")])])]),s._v(" "),n("div",{staticClass:"custom-block danger"},[n("p",{staticClass:"custom-block-title"},[s._v("警告")]),s._v(" "),n("p",[s._v("插件间不应该存在过多的耦合，如果确实需要导入某个插件内的数据，可以参考 "),n("router-link",{attrs:{to:"./../advanced/export-and-require.html"}},[s._v("进阶-跨插件访问")])],1)]),s._v(" "),n("h2",{attrs:{id:"加载单个插件"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#加载单个插件"}},[s._v("#")]),s._v(" 加载单个插件")]),s._v(" "),n("p",[s._v("在 "),n("code",[s._v("bot.py")]),s._v(" 文件中添加以下行：")]),s._v(" "),n("div",{staticClass:"language-python line-numbers-mode"},[n("div",{staticClass:"highlight-lines"},[n("br"),n("br"),n("br"),n("br"),n("div",{staticClass:"highlighted"},[s._v(" ")]),n("br"),n("div",{staticClass:"highlighted"},[s._v(" ")]),n("br"),n("br"),n("br"),n("br"),n("br"),n("br")]),n("pre",{pre:!0,attrs:{class:"language-python"}},[n("code",[n("span",{pre:!0,attrs:{class:"token keyword"}},[s._v("import")]),s._v(" nonebot\n\nnonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("init"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n"),n("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 加载一个 pip 安装的插件")]),s._v("\nnonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("load_plugin"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token string"}},[s._v('"nonebot_plugin_status"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n"),n("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 加载本地的单独插件")]),s._v("\nnonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("load_plugin"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token string"}},[s._v('"awesome_bot.plugins.xxx"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n\napp "),n("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" nonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("get_asgi"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n\n"),n("span",{pre:!0,attrs:{class:"token keyword"}},[s._v("if")]),s._v(" __name__ "),n("span",{pre:!0,attrs:{class:"token operator"}},[s._v("==")]),s._v(" "),n("span",{pre:!0,attrs:{class:"token string"}},[s._v('"__main__"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n    nonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("run"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n")])]),n("div",{staticClass:"line-numbers-wrapper"},[n("span",{staticClass:"line-number"},[s._v("1")]),n("br"),n("span",{staticClass:"line-number"},[s._v("2")]),n("br"),n("span",{staticClass:"line-number"},[s._v("3")]),n("br"),n("span",{staticClass:"line-number"},[s._v("4")]),n("br"),n("span",{staticClass:"line-number"},[s._v("5")]),n("br"),n("span",{staticClass:"line-number"},[s._v("6")]),n("br"),n("span",{staticClass:"line-number"},[s._v("7")]),n("br"),n("span",{staticClass:"line-number"},[s._v("8")]),n("br"),n("span",{staticClass:"line-number"},[s._v("9")]),n("br"),n("span",{staticClass:"line-number"},[s._v("10")]),n("br"),n("span",{staticClass:"line-number"},[s._v("11")]),n("br"),n("span",{staticClass:"line-number"},[s._v("12")]),n("br")])]),n("h2",{attrs:{id:"子插件-嵌套插件"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#子插件-嵌套插件"}},[s._v("#")]),s._v(" 子插件(嵌套插件)")]),s._v(" "),n("p",[s._v("在插件中同样可以加载子插件，例如如下插件目录结构：")]),s._v(" "),n("pre",{staticClass:"vue-container"},[n("code",[n("p",[s._v("foo_plugin\n├── "),n("code",[s._v("plugins")]),s._v("\n│   ├── "),n("code",[s._v("sub_plugin1")]),s._v("\n│   │  └── __init__.py\n│   └── "),n("code",[s._v("sub_plugin2.py")]),s._v("\n├── "),n("code",[s._v("__init__.py")]),s._v("\n└── config.py")]),s._v("\n")])]),s._v(" "),n("p",[s._v("在插件目录下的 "),n("code",[s._v("__init__.py")]),s._v(" 中添加如下代码：")]),s._v(" "),n("div",{staticClass:"language-python line-numbers-mode"},[n("pre",{pre:!0,attrs:{class:"language-python"}},[n("code",[n("span",{pre:!0,attrs:{class:"token keyword"}},[s._v("from")]),s._v(" pathlib "),n("span",{pre:!0,attrs:{class:"token keyword"}},[s._v("import")]),s._v(" Path\n\n"),n("span",{pre:!0,attrs:{class:"token keyword"}},[s._v("import")]),s._v(" nonebot\n\n"),n("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# store all subplugins")]),s._v("\n_sub_plugins "),n("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" "),n("span",{pre:!0,attrs:{class:"token builtin"}},[s._v("set")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n"),n("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# load sub plugins")]),s._v("\n_sub_plugins "),n("span",{pre:!0,attrs:{class:"token operator"}},[s._v("|")]),n("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" nonebot"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("load_plugins"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),s._v("\n    "),n("span",{pre:!0,attrs:{class:"token builtin"}},[s._v("str")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),s._v("Path"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),s._v("__file__"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("parent "),n("span",{pre:!0,attrs:{class:"token operator"}},[s._v("/")]),s._v(" "),n("span",{pre:!0,attrs:{class:"token string"}},[s._v('"plugins"')]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("resolve"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),n("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v("\n")])]),s._v(" "),n("div",{staticClass:"line-numbers-wrapper"},[n("span",{staticClass:"line-number"},[s._v("1")]),n("br"),n("span",{staticClass:"line-number"},[s._v("2")]),n("br"),n("span",{staticClass:"line-number"},[s._v("3")]),n("br"),n("span",{staticClass:"line-number"},[s._v("4")]),n("br"),n("span",{staticClass:"line-number"},[s._v("5")]),n("br"),n("span",{staticClass:"line-number"},[s._v("6")]),n("br"),n("span",{staticClass:"line-number"},[s._v("7")]),n("br"),n("span",{staticClass:"line-number"},[s._v("8")]),n("br"),n("span",{staticClass:"line-number"},[s._v("9")]),n("br")])]),n("p",[s._v("插件将会被加载并存储于 "),n("code",[s._v("_sub_plugins")]),s._v(" 中。")]),s._v(" "),n("h2",{attrs:{id:"运行结果"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#运行结果"}},[s._v("#")]),s._v(" 运行结果")]),s._v(" "),n("p",[s._v("尝试运行 "),n("code",[s._v("nb run")]),s._v(" 或者 "),n("code",[s._v("python bot.py")]),s._v("，可以看到日志输出了类似如下内容：")]),s._v(" "),n("div",{staticClass:"language-plain line-numbers-mode"},[n("pre",{pre:!0,attrs:{class:"language-text"}},[n("code",[s._v('09-19 21:51:59 [INFO] nonebot | Succeeded to import "nonebot.plugins.base"\n09-19 21:51:59 [INFO] nonebot | Succeeded to import "plugin_in_folder"\n')])]),s._v(" "),n("div",{staticClass:"line-numbers-wrapper"},[n("span",{staticClass:"line-number"},[s._v("1")]),n("br"),n("span",{staticClass:"line-number"},[s._v("2")]),n("br")])])])}),[],!1,null,null,null);t.default=e.exports}}]);