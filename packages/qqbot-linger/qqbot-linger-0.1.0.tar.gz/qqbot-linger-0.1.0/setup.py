# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qqbot_linger']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-plugin-7s-roll>=0.1.0,<0.2.0',
 'nonebot-plugin-bam>=0.1.0,<0.2.0',
 'nonebot2>=2.0.0a10,<3.0.0']

entry_points = \
{'console_scripts': ['linger = qqbot_linger.main:main']}

setup_kwargs = {
    'name': 'qqbot-linger',
    'version': '0.1.0',
    'description': 'My QQ Bot for personal use',
    'long_description': '# 玲儿\n\n自用 QQ 机器人。\n\n## 功能\n\n- Bilibili 用户监控，参见：[nonebot-plugin-bam]\n- 跑团骰子，参见 [nonebot-plugin-7s-roll]\n\n## 使用\n\n```bash\npip install qqbot-linger\ncd /a/path/you/want/store/config/and/database\nvim .env # edit this file, see `.env.sample file` for a example\n\n# Start cqhttp server\n# like go-cqhttp, cqhttp-mirai etc\n\nlinger # start the bot\n```\n\n## 截图\n\n以后再弄。\n\n## LICENSE\n\nUnlicense.\n\n[nonebot-plugin-bam]: https://github.com/7sDream/nonebot-plugin-bam\n[nonebot-plugin-7s-roll]: https://github.com/7sDream/nonebot-plugin-7s-roll\n',
    'author': '7sDream',
    'author_email': 'i@7sdre.am',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/7sDream/qqbot-linger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
