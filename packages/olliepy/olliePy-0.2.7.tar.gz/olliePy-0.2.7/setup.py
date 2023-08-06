# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olliepy',
 'olliepy.utils',
 'reports-templates',
 'reports-templates.interactive-dashboard',
 'reports-templates.regression-error-analysis-report']

package_data = \
{'': ['*'],
 'reports-templates.interactive-dashboard': ['css/*',
                                             'fonts/*',
                                             'img/*',
                                             'js/*'],
 'reports-templates.regression-error-analysis-report': ['css/*',
                                                        'fonts/*',
                                                        'img/*',
                                                        'js/*']}

install_requires = \
['flask>=1.1.0',
 'ipython>=7.0.0',
 'numpy>=1.17.0',
 'pandas>=0.25.0',
 'psutil>=5.7.3',
 'pycryptodome>=3.9.9,<4.0.0',
 'rich>=9.10.0',
 'scikit-learn>=0.22',
 'scipy>=1.3.0']

setup_kwargs = {
    'name': 'olliepy',
    'version': '0.2.7',
    'description': 'OlliePy is a python package which can help data scientists in exploring their data and evaluating and analysing their machine learning experiments by utilising the power and structure of modern web applications. The data scientist only needs to provide the data and any required information and OlliePy will generate the rest.',
    'long_description': '# OlliePy - An alternative approach for data science\n> **OlliePy** is a python package which can help data scientists in\n> exploring their data and evaluating and analysing their machine learning experiments by\n> utilising the power and structure of modern web applications. \n> The data scientist only needs to provide the data and any required \n> information and OlliePy will generate the rest.\n\n## <br/>Documentation\nGet started by following the [guide](https://ahmed-mohamed-sn.github.io/olliePy/)\n### Installation\n`pip install -U olliepy`\n',
    'author': 'ahmed.mohamed',
    'author_email': 'hanoush87@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ahmed-mohamed-sn.github.io/olliePy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
