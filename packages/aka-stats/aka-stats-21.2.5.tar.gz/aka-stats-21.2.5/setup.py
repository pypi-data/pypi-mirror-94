# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aka_stats']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0', 'pytz>=2019.3,<2020.0', 'redis>=3.4.1,<4.0.0']

extras_require = \
{'fastapi': ['fastapi>=0.54.1,<0.55.0']}

entry_points = \
{'pytest11': ['mock_stats = aka_stats.testing']}

setup_kwargs = {
    'name': 'aka-stats',
    'version': '21.2.5',
    'description': 'Module for keeping metrics about your application in Redis. The goal is to have an easy way to measure an application, and then expose these metrics through a HTTP API, either to process it in some web ui, or expose it to Prometheus.',
    'long_description': '# Aka Stats\n\n[![GitHub license](https://img.shields.io/github/license/MichalMazurek/aka_stats)](https://github.com/MichalMazurek/aka_stats/blob/main/LICENSE)\n[![Test/Lint](https://img.shields.io/github/workflow/status/MichalMazurek/aka_stats/Test%20code/main)](https://github.com/MichalMazurek/aka_stats/actions?query=workflow%3A%22Test+code%22)\n[![PyPI](https://img.shields.io/pypi/v/aka_stats)](https://pypi.org/project/aka-stats/)\n\nAka (赤 - red in japanese) Stats.\n\nUnified module for keeping stats in Redis.\n\nThe goal is to have an easy way to measure an application, and then expose these metrics through a HTTP API,\neither to process it in some web ui, or expose it to Prometheus.\n\n```python\nfrom aka_stats import Stats, timer\n\nwith Stats() as stats:\n\n    t = timer()\n    ...\n\n    stats("task_done", next(t).stat)\n\n```\n\nOr for asynchronouse code:\n\n```python\nfrom aka_stats import Stats, timer\n\nasync def process_device(device_id: str):\n\n    async with Stats() as stat:\n        t = timer()\n        ...\n        stats("task_done", next(t).stat, extra_labels={"device_id": device_id})\n```\n\n## Installation\n\nAnd add this package to your project:\n\n```bash\npoetry add aka-stats\n```\n\n## Usage Guide\n\nCheck out the usage guide here: [Usage.md](Usage.md)\n\n## Prometheus formatters\n\nInformation how to write a formatter is here: [PrometheusFormatter.md](PrometheusFormatter.md)\n\n## Optional Standalone HTTP API\n\nCheck out this guide here: [Included HTTP API](<Included http api.md>)\n\n## Pytest plugin\n\nThis module is also a pytest plugin, providing a fixture `mock_stats` which collects stats instead of writing them\nto Redis.\n\n```python\n\ndef test_something(mock_stats):\n    do_something()\n    assert mock_stats[0] == (1612550961, "test", 1, None)\n\n```\n\nAnd the module with function:\n\n```python\n\ndef do_something():\n    with Stats() as stats:\n        stat("test", 1)\n```\n',
    'author': 'Michal Mazurek',
    'author_email': 'mazurek.michal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MichalMazurek/aka_stats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
