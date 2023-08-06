# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_styledstr']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-alpha.10,<3.0.0', 'pyyaml>=5.4.1,<6.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-styledstr',
    'version': '0.1.2',
    'description': 'A Styled String Managing Plugin for Nonebot 2',
    'long_description': "# nonebot-plugin-styledstr\n\nNonebot 2 风格化字符串管理插件。\n\n[![time tracker](https://wakatime.com/badge/github/jks15satoshi/nonebot_plugin_styledstr.svg)](https://wakatime.com/badge/github/jks15satoshi/nonebot_plugin_styledstr)\n\n> 由于本人 Python 水平低下，因此源码可能会令人不适，烦请谅解。\n\n## 介绍\n\n风格化字符串管理，或称字符串资源管理，即通过字符串标签来标识和获取一个字符串内容。设计初衷是用于灵活控制机器人的输出内容。\n\n### 字符串标签\n\n字符串标签用以在风格预设文件中唯一标识一个字符串内容。字符串标签使用点记法表示层级结构。举个例子，如果一个字符串在预设文件中的层级结构是这样的：\n\n````yaml\none:\n    sample:\n        structure: something\n````\n\n那么这个字符串 `something` 的标签即为 `one.sample.structure`。\n\n### 占位符\n\n如果字符串中的某些部分需要在运行时改变内容，那么可以在其中加入占位符，标记需要修改的部分。\n\n占位符由两部分组成：用以标识占位符的占位符名称，以及包围占位符名称的指示符 `$`。占位符名称是由英文字母、数字与下划线组成的非空字符串，且首字符仅可为英文字母，长度不超过 24 个字符。例如 `$Placeholder_Here$`。\n\n占位符名称对大小写不敏感，但在调用程序方法进行占位符替换时，占位符名称只能为小写字母（数字和下划线不受影响）。使用方法可以参考 [使用用例](#用例：通过占位符替换文本内容)。\n\n### 风格预设\n\n该插件可以通过不同的风格预设来切换相同字符串标签的内容，通过这种方式，你可以为你的 ~~GLADoS~~ 机器人加装各种“人格核心”，或者让它变成一个“语言通”（即国际化）。使用方法可以参考 [使用用例](#用例：通过风格预设切换不同风格的字符串内容)。\n\n> 这也是为何我将这个插件命名为“风格化字符串管理”而非诸如“字符串资源管理”一类的名称（虽然这名称依旧很烂）。\n\n## 安装\n\n> 注意：你的 Python 版本不应低于 3.8。\n\n### 使用 `nb-cli` 安装\n\n````shell\nnb plugin install nonebot-plugin-styledstr\n````\n\n### 使用 Poetry 安装\n\n````shell\npoetry add nonebot-plugin-styledstr\n````\n\n### 使用 `pip` 安装\n\n````shell\npip install nonebot-plugin-styledstr\n````\n\n## 使用\n\n### 配置\n\n> 注意：使用该插件前，请务必在项目中创建存放字符串资源的目录，并通过下面的配置项指定其为资源目录。关于如何设置插件配置项，参考 Nonebot 2 官方文档的 [基本配置](https://v2.nonebot.dev/guide/basic-configuration.html) 章节。\n\n该插件可通过在配置文件中添加如下配置项对部分功能进行配置。\n\n- **`STYLEDSTR_RESPATH`**：字符串资源目录（**必填项**。建议在 `bot.py` 文件中使用 `pathlib` 进行配置或使用绝对路径，若使用相对路径请确保工作目录为项目根目录）；\n- **`STYLEDSTR_PRESET`**：风格预设，默认为 `default`。\n\n### 为项目添加风格预设文件\n\n在上一节创建的字符串资源目录下根据需要创建风格预设文件。风格预设文件以 YAML 或 JSON 文件存储，并需确保文件名与风格预设配置一致，文件名对大小写不敏感。例如若风格预设配置为 `default`，则需要保证字符串资源目录下存在文件 `default.yaml` 或 `default.json`。\n\n如果在资源目录下同时存在多个满足同一预设的文件（例如同时存在 `default.yaml` 与 `default.json`），则所读取的预设文件是不确定的，因此应避免出现此种情况。\n\n### 加载插件并获取解析器对象\n\n参考 Nonebot 2 官方文档的 [加载插件](https://v2.nonebot.dev/guide/loading-a-plugin.html) 章节，在项目中加载该插件。\n\n使用前，请通过 `require` 获取 `parser` 解析器对象。\n\n````python\n>>> from nonebot import require\n>>> parser = require('nonebot_plugin_styledstr').parser\n# 调用 parse 方法解析字符串标签\n>>> parser.parse('token.sample')\n````\n\n详细使用方法请见下面的 [使用用例](#使用用例) 部分。\n\n## 使用用例\n\n你可以通过以下用例来大致了解该插件的功能。\n\n> 以下用例中出现的 Python 语句默认获取了该插件。\n\n### 用例：通过风格预设切换不同风格的字符串内容\n\n假设在你的项目目录下存在如下的风格预设文件：\n\n````yaml\n# default.yaml\nhelp:\n    prompt: 请输入你需要获取的帮助内容\n\n# customer_service.yaml\nhelp:\n    prompt: 亲，请问您需要什么帮助？\n````\n\n则可以根据实际配置的风格预设，获取对应预设文件的字符串内容：\n\n> 关于如何配置风格预设，请见 [配置](#配置) 一节。\n\n````python\n>>> parser.parse('help.prompt')\n# STYLEDSTR_PRESET=DEFAULT\n'请输入你需要获取的帮助内容'\n# STYLEDSTR_PRESET=CUSTOMER_SERVICE\n'亲，请问您需要什么帮助？'\n````\n\n或者强制以某个预设获取字符串内容：\n\n````python\n>>> parser.parse('help.prompt', preset='customer_service')\n'亲，请问您需要什么帮助？'\n````\n\n类似地，也可以通过创建多语言预设实现国际化 (i18n) 功能。\n\n### 用例：通过占位符替换文本内容\n\n假设在你的项目目录下存在如下的风格预设文件：\n\n````yaml\n# default.yaml\ndemo:\n    clock: 当前的时间为$TIME$。\n````\n\n则在该风格预设下，可以通过如下方式将占位符 `$TIME$` 替换为实际的时间：\n\n````python\n>>> from time import gmtime, strftime\n>>> current_time = strftime(r'%Y年%m月%d日 %H:%M:%S', gmtime(1609459200))\n>>> parser.parse('demo.clock', time=current_time)\n'当前的时间为2021年1月1日 00:00:00。'\n````\n\n## 许可协议\n\n该项目以 MIT 协议开放源代码，详阅 [LICENSE](LICENSE) 文件。\n",
    'author': 'Satoshi Jek',
    'author_email': 'jks15satoshi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
