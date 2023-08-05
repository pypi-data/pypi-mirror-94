# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_authorization']

package_data = \
{'': ['*']}

install_requires = \
['flask-login>=0.5.0,<0.6.0', 'flask>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'flask-authorization',
    'version': '1.4',
    'description': 'Simple user authorization to use alongside with Flask-Login',
    'long_description': '# Flask-Authorization\n\n[![Downloads](https://pepy.tech/badge/flask-authorization)](https://pepy.tech/project/flask-authorization)\n[![Downloads](https://pepy.tech/badge/flask-authorization/month)](https://pepy.tech/project/flask-authorization)\n[![Downloads](https://pepy.tech/badge/flask-authorization/week)](https://pepy.tech/project/flask-authorization)\n\nSimple user authorization to use alongside with Flask-Login.\n\n## Installation\n```\npip3 install Flask-Authorization\n```\n\n## Usage\n```python\nfrom flask_Authorization import Authorize\nauthorize = Authorize()\n\n# Initialize Extension\nauthorize.init_app(app)\n```\n\nFor Flask-Authorization to work properly, your user models needs to implement a function called `get_permissions()` that returns a list of permissions. You can define any permissions you like, but `"ROOT", "ADMIN", "USER"` are recommended.\nFlask-Authorization will check if the current user has the required permissions on routes decorated with the `@flask_authorization.permission_required(permission)` decorator.\n',
    'author': 'Marcel Kröker',
    'author_email': 'kroeker.marcel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mkrd/flask-authorization',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
