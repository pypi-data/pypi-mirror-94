# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clerk']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.7.3,<4.0.0', 'pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'clerk-sdk-python',
    'version': '0.1.0',
    'description': 'Python SDK for clerk.dev',
    'long_description': '# Unofficial Clerk.dev Python SDK\n\n## What is Clerk.dev?\n\nSee https://clerk.dev\n\n## Installation\n\n`pip install clerk-sdk-python`\n\n## Usage\n\n```python\nimport asyncio\n\nfrom clerk import Client\n\n\nasync def main():\n    async with Client("my-token") as client:\n        users = await client.users.list()\n        for user in users:\n            print(f"Got user {user.id} -> {user.first_name} {user.last_name}")\n\n\nasyncio.run(main())\n```\n',
    'author': 'Elijah Wilson',
    'author_email': 'dev.tizz98@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://clerk.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
