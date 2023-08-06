# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/plugins'}

packages = \
['hk_reporter', 'hk_reporter.platform', 'platform']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'feedparser>=6.0.2,<7.0.0',
 'httpx>=0.16.1,<0.17.0',
 'nonebot2>=2.0.0-alpha.8,<3.0.0',
 'nonebot_plugin_apscheduler>=0.1.2,<0.2.0',
 'pyppeteer>=0.2.5,<0.3.0',
 'tinydb>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-hk-reporter',
    'version': '0.1.0',
    'description': 'Subscribe message from social medias',
    'long_description': '# hk-reporter  通用订阅推送插件\n\n## 简介\n一款自动爬取各种站点，社交平台更新动态，并将信息推送到QQ的机器人。基于 [`NoneBot2`](https://github.com/nonebot/nonebot2 ) 开发。\n\n支持的平台：\n* 微博\n* bilibili\n\n## 文档\nTBD（会写的会写的）\n\n## 功能\n* 定时爬取制定网站\n* 通过图片发送文本，防止风控\n* 使用队列限制发送频率\n\n## 鸣谢\n* [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp)：简单又完善的 cqhttp 实现\n* [`NoneBot2`](https://github.com/nonebot/nonebot2)：超好用的开发框架\n* [`HarukaBot`](https://github.com/SK-415/HarukaBot/): 借鉴了相当多的东西\n\n## License\nMIT\n\n',
    'author': 'felinae98',
    'author_email': 'felinae225@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/felinae98/nonebot-hk-reporter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
