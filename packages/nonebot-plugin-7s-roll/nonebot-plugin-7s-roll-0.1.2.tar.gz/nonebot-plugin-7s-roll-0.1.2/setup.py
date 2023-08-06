# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_7s_roll']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-alpha.10,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-7s-roll',
    'version': '0.1.2',
    'description': 'A roll dice plugin for nonebot',
    'long_description': '# Roll Dice\n\n扔骰子小工具。\n\n## 使用\n\n```python\nimport nonebot\nfrom nonebot.adapters.cqhttp import Bot as CQHTTPBot\n\nnonebot.init(_env_file=".env")\ndriver = nonebot.get_driver()\ndriver.register_adapter("cqhttp", CQHTTPBot)\nnonebot.load_builtin_plugins()\n\n# load other plugins\n\nnonebot.load_plugin("nonebot_plugin_7s_roll")\n\nnonebot.run()\n```\n\n其中 .env 文件除了 nonebot 的常规配置项外，还有可添加以下配置属性（示例中的是默认值）：\n\n```env\n# 命令名（在 at 机器人时使用， `@bot /roll 1d10`）\nI7S_ROLL_COMMAND="roll"\n# 关键字（直接使用，无需 at, `roll 1d10`）\nI7S_ROLL_TRIGGER="roll"\n```\n\n## 命令\n\n`roll <expr>[[ ]<operator>[ ]<target>]`\n\n其中：\n\n- `<expr>` 计算表达式，格式为\n  - `<roll>[[ ][+|-][ ]<roll>]...`，其中 `roll` 不超过 20 项，其格式为：\n    - `<times>[d|D]<faces>[ ][<policy>]`，其中\n      - `<times>` 为投掷次数，不超过 20 次\n      - `<faces>` 为骰子面数，不超过 1000 面\n      - `<policy>` 为投掷方式，默认为 `sum`，可选方式有：\n        - `sum` 求和\n        - `min` 取最小值\n        - `max` 取最大值\n        - `avg` 取平均值\n- `operator` 为比较运算，可以为\n  - `>`、`大于`\n  - `<`、`小于`\n  - `>=`、`大于等于`\n  - `<=`、`小于等于`\n- `target` 为期望目标\n\n## 举例\n\n`roll 3d6`（在只有一个 `roll` 时，会显示的比较详细）:\n\n```text\n3d6 投掷结果\n\n第 1 颗：5\n第 2 颗：5\n第 3 颗：6\n\n总和为 16\n```\n\n`roll 3d10+2d6+1 >20`:\n\n```text\n3d10+2d6+1 投掷结果(目标 > 20)：\n(5 + 1 + 9) + (4 + 5) + 1 = 25，通过\n```\n\n`roll 3d100max+4d10`\n\n```text\n3d100max+4d10 投掷结果\n(max[35, 60, 29] = 60) + (1 + 1 + 5 + 8) = 75\n```\n\n## LICENSE\n\nMIT.\n',
    'author': '7sDream',
    'author_email': 'i@7sdre.am',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/7sDream/nonebot_plugin_7s_roll',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
