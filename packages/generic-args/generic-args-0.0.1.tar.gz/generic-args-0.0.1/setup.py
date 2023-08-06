# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['generic_args']

package_data = \
{'': ['*']}

install_requires = \
['documented>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'generic-args',
    'version': '0.0.1',
    'description': 'Given an instantiated generic class, retrieve the type arguments of itself or its parents.',
    'long_description': "# generic-args\n\n[![Build Status](https://github.com/python-platonic/generic-args/workflows/test/badge.svg?branch=master&event=push)](https://github.com/python-platonic/generic-args/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/python-platonic/generic-args/branch/master/graph/badge.svg)](https://codecov.io/gh/python-platonic/generic-args)\n[![Python Version](https://img.shields.io/pypi/pyversions/generic-args.svg)](https://pypi.org/project/generic-args/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nGiven an instantiated generic class, retrieve the type arguments of itself or its parents.\n\nThe packages solves the problem described at [this StackOverflow question](https://stackoverflow.com/q/48572831/1245471).\n\n## Installation\n\n```bash\npip install generic-args\n```\n\n\n## Example\n\nShowcase how your project can be used:\n\n```python\nfrom typing import List\nfrom generic_args import generic_type_args\n\ngeneric_type_args(List[int])\n# (<type 'int'>, )\n```\n\n## License\n\n[MIT](https://github.com/python-platonic/generic-args/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [54efe958f72ac06e912a1423aa14be8b149f988f](https://github.com/wemake-services/wemake-python-package/tree/54efe958f72ac06e912a1423aa14be8b149f988f). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/54efe958f72ac06e912a1423aa14be8b149f988f...master) since then.\n",
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-platonic/generic-args',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
