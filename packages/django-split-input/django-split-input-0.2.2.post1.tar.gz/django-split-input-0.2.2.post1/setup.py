# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_split_input']

package_data = \
{'': ['*'],
 'django_split_input': ['static/django_split_input/css/*',
                        'static/django_split_input/js/*',
                        'templates/django_split_input/*']}

install_requires = \
['Django>=2.0,<4.0']

setup_kwargs = {
    'name': 'django-split-input',
    'version': '0.2.2.post1',
    'description': 'A widget to have a django text input split into multiple HTML inputs.',
    'long_description': '# django_split_input\n\n## About\n\nThis is a django widget for multiple fixed size inputs for one form field. These could be used for those super fancy\nverification code forms. The cursor is moved to the next input field using JS/jQuery.\n\n![django_split_input Showcase](django_split_input_showcase.png)\n\n## Usage\n\n1. Install `django_split_input` and add it to your `INSTALLED_APPS`.\n   ```shell\n   pip install django-split-input\n   ```\n   In your settings.py:\n   ```python\n   "django_split_input",\n   ```\n2. Install `jQuery` using your preferred method (e.g.\n   [django-yarnpkg](https://pypi.org/project/django-yarnpkg/))\n   \n3. Create a form with a `CharField`.\n4. Use `SplitInput` as a widget and supply the sizes of all input fields.\n\n```python\nfrom django import forms\nfrom django_split_input import SplitInput\n\n\nclass VerificationForm(forms.Form):\n   auth_code = forms.CharField(label=\'Code\', widget=SplitInput(sizes=(3, 3, 3)))\n```\n\n',
    'author': 'Julian Leucker',
    'author_email': 'leuckerj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://edugit.org/AlekSIS/libs/django-split-input',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
