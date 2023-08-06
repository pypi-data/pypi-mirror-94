# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convpandas', 'convpandas.command']

package_data = \
{'': ['*']}

install_requires = \
['click', 'openpyxl', 'pandas>=1.2.1,<2.0.0']

entry_points = \
{'console_scripts': ['convpandas = convpandas.__main__:cli']}

setup_kwargs = {
    'name': 'convpandas',
    'version': '0.2.0',
    'description': 'Convert file format with pandas',
    'long_description': '# convert-fileformat-with-pandas\nConvert file format with [pandas](https://pandas.pydata.org/).\n\n[![Build Status](https://travis-ci.org/yuji38kwmt/convpandas.svg?branch=master)](https://travis-ci.org/yuji38kwmt/convpandas)\n[![PyPI version](https://badge.fury.io/py/convpandas.svg)](https://badge.fury.io/py/convpandas)\n[![Python Versions](https://img.shields.io/pypi/pyversions/convpandas.svg)](https://pypi.org/project/convpandas/)\n\n# Requirements\n* Python 3.7+\n\n# Install\n\n```\n$ pip install convpandas\n```\n\nhttps://pypi.org/project/convpandas/\n\n\n# Usage\n\n## csv2xlsx\nConvert csv file to xlsx file.\n\n```\n$ convpandas csv2xlsx --help\nUsage: convpandas csv2xlsx [OPTIONS] [CSV_FILE]... XLSX_FILE\n\n  Convert csv file to xlsx file.\n\nOptions:\n  --sep TEXT                   Delimiter to use when reading csv.  [default:,]\n\n  --encoding TEXT              Encoding to use when reading csv. List of Python standard encodings. (https://docs.python.org/3/library/codecs.html#standard-encodings) [default: utf-8]\n\n  --quotechar TEXT             The character used to denote the start and end of a quoted item when reading csv.\n\n  --string_to_numeric BOOLEAN  If true, convert string to numeric. [default:true]\n```\n\n\nConvert `in.csv` to `out.xlsx` .\n\n```\n$ convpandas csv2xlsx in.csv out.xlsx\n```\n\n\nWhen specifying `-` for `CSV_FILE`, get from STDIN. \n\n```\n$ convpandas csv2xlsx - out.xlsx < in.csv\n```\n\nConvert `in1.csv` and `in2.csv` to `out.xlsx` . Sheet name is csv filename without its suffix.  \n\n```\n$ convpandas csv2xlsx in1.csv in2.csv out.xlsx\n```\n\n![](/home/vagrant/Documents/convert-fileformat-with-pandas/docs/img/output_xlsx_file_from_multiple_csv.png)\n\n\n## xlsx2csv\nConvert xlsx file to csv file.\n\n```\n$ convpandas xlsx2csv --help\nUsage: convpandas xlsx2csv [OPTIONS] XLSX_FILE CSV_FILE\n\n  Convert xlsx file to csv file.\n\nOptions:\n  --sheet_name TEXT  Sheet name when reading xlsx. If not specified, read 1st sheet.\n\n  --sep TEXT         Field delimiter for the output file.  [default: ,]\n\n  --encoding TEXT    A string representing the encoding to use in the output file.  [default: utf-8]\n\n  --quotechar TEXT   Character used to quote fields. \n\n  --help             Show this message and exit.\n```\n\n\nConvert `in.xlsx` to `out.csv` .\n\n```\n$ convpandas csv2xlsx in.xlsx out.csv\n```\n\n\nWhen specifying `-` for `CSV_FILE`, write to STDOUT. \n\n```\n$ convpandas csv2xlsx in.xlsx -\nname,age\nAlice,23\n```\n\nWith specifying `--sheet_name`, you can select sheet name that you want to convert.\n\n```\n$ convpandas csv2xlsx in.xlsx out.csv --sheet_name sheet2\n```\n',
    'author': 'yuji38kwmt',
    'author_email': None,
    'maintainer': 'yuji38kwmt',
    'maintainer_email': None,
    'url': 'https://github.com/yuji38kwmt/convert-fileformat-with-pandas.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
