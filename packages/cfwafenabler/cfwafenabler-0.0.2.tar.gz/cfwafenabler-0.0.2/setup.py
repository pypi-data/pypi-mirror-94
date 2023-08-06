# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfwafenabler']

package_data = \
{'': ['*']}

install_requires = \
['cloudflare>=2.8.15,<3.0.0',
 'configparser>=5.0.1,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'simple-term-menu>=0.10.5,<0.11.0']

entry_points = \
{'console_scripts': ['cfwafenabler = cfwafenabler.__main__:main']}

setup_kwargs = {
    'name': 'cfwafenabler',
    'version': '0.0.2',
    'description': 'Allows to mass modify rules in CloudFlare WAF',
    'long_description': "# cfwafenabler\n\nCloudFlare doesn't allow to set their entire WAF in Simulate mode. Instead, they suggest you to use the API.\ncfwafenabler allows you to mass-modify all the rules to put your WAF in Simulate mode\n\n# Installation\n\nTo install cfwafenabler just use [pipx](https://github.com/pipxproject/pipx)\n```\npipx install cfwafenabler\n```\n\n# Usage\n\nBefore executing cfwafenabler, you need to set some CloudFlare environment variables.\nIf you use API key ( global permissions ) you need to set:\n\n```\nexport CF_API_EMAIL=your@email.com\nexport CF_API_KEY=YouApiKey\n```\n\nIf you are using CloudFlare API tokens, you only need to set (it's the same env variable, they reuse it):\n```\nexport CF_API_KEY=YouApiToken\n```\nThis token needs the following permissions:\n```\nZone.Zone:Read, Zone.Firewall Services:Edit\n```\n\n# Credits\n\nBased in [canozokur's](https://github.com/canozokur/cloudflare-waf-simulate) work.\n\nThis package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [byt3bl33d3r/pythoncookie](https://github.com/byt3bl33d3r/pythoncookie) project template.\n",
    'author': 'David Lladro',
    'author_email': 'david.lladro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nomex/cfwafenabler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
