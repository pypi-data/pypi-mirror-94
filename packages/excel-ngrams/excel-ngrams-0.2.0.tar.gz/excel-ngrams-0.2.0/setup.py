# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['excel_ngrams']

package_data = \
{'': ['*']}

install_requires = \
['XlsxWriter>=1.3.7,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'nltk>=3.5,<4.0',
 'openpyxl>=3.0.6,<4.0.0',
 'pandas>=1.2.1,<2.0.0',
 'spacy>=2.3.5,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3.4.0,<4.0.0']}

entry_points = \
{'console_scripts': ['excel-ngrams = excel_ngrams.console:main']}

setup_kwargs = {
    'name': 'excel-ngrams',
    'version': '0.2.0',
    'description': 'An app to output n-grams from column in Excel spreadsheet',
    'long_description': "[![Tests](https://github.com/mattyocode/excel-ngrams/workflows/Tests/badge.svg)](https://github.com/mattyocode/excel-ngrams/actions?workflow=Tests)\n\n[![codecov](https://codecov.io/gh/mattyocode/excel-ngrams/branch/main/graph/badge.svg?token=0621CKX30T)](https://codecov.io/gh/mattyocode/excel-ngrams)\n\n[![PyPI](https://img.shields.io/pypi/v/excel-ngrams.svg)](https://pypi.org/project/excel-ngrams/)\n\n# The Excel Ngrams Project\n\nA project to analyse a column of text in an Excel document and\nreturn a CSV file with the most common ngrams from that text. Output\nfile is returned to the same directory as the input file.\n\nYou can choose the maximum n-gram length, and maximum number of\nresults (rows) returned. The app defaults to looking for a column\nnamed'Keyword' but any column name can be passed in as an argument.\n\nThe column of terms to analyse must be the longest (or only) column\nin the document to prevent the addition of NaN as a placeholder in\nfinal cells, which will cause errors.\n\n\nWords are tokenised with Spacy and ngrams are generated with NLTK.\n\n\n\n\n## Installation\n\nTo install the Excel Ngrams Project,\nrun this command in your terminal:\n\n\n$ pip install excel-ngrams\n\n\n![Excel-ngrams-usage](https://media.giphy.com/media/L3QRuhyMhdgUWNtwFp/giphy.gif)\n",
    'author': 'Matthew Oliver',
    'author_email': 'matthewoliver@live.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mattyocode/excel-ngrams',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
