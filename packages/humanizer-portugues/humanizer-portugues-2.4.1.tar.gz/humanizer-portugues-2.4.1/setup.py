# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['humanizer_portugues']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'humanizer-portugues',
    'version': '2.4.1',
    'description': 'Humanize functions for Portuguese.',
    'long_description': 'Humanizer Portugues\n===================\n\n**SUPERSEEDED BY: https://github.com/staticdev/human-readable.**\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/humanizer-portugues.svg\n   :target: https://pypi.org/project/humanizer-portugues/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/humanizer-portugues\n   :target: https://pypi.org/project/humanizer-portugues\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/humanizer-portugues\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/humanizer-portugues/latest.svg?label=Read%20the%20Docs\n   :target: https://humanizer-portugues.readthedocs.io/\n   :alt: Read the documentation at https://humanizer-portugues.readthedocs.io/\n.. |Tests| image:: https://github.com/staticdev/humanizer-portugues/workflows/Tests/badge.svg\n   :target: https://github.com/staticdev/humanizer-portugues/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/staticdev/humanizer-portugues/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/staticdev/humanizer-portugues\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* This lib contains various humanization methods such as transforming a time difference in a human-readable duration "três minutos atrás" (three minutes ago) or in a phrase.\n\n\nRequirements\n------------\n\n* It works in Python 3.7 and 3.8.\n\n\nInstallation\n------------\n\nYou can install *Humanizer Portugues* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install humanizer-portugues\n\n\nUsage\n-----\n\nImport the lib with:\n\n.. code-block:: python\n\n   import humanizer_portugues\n\n\nHumanization filesizes:\n\n.. code-block:: python\n\n   humanizer_portugues.natural_size(1000000)\n   "1.0 MB"\n\n   humanizer_portugues.natural_size(1000000, binary=True)\n   "976.6 KiB"\n\n   humanizer_portugues.natural_size(1000000, gnu=True)\n   "976.6K"\n\n\nHumanization of lists:\n\n.. code-block:: python\n\n   humanizer_portugues.natural_list(["Cláudio", "Maria"], ",")\n   "Cláudio, Maria"\n\n   humanizer_portugues.natural_list(["Cláudio", "Maria"], ",", "e")\n   "Cláudio e Maria"\n\n   humanizer_portugues.natural_list(["Cláudio", "Maria", "José"], ";", "ou")\n   "Cláudio; Maria ou José"\n\n\nHumanization of integers:\n\n.. code-block:: python\n\n   humanizer_portugues.ap_number(4)\n   "quatro"\n\n   humanizer_portugues.ap_number(41)\n   "41"\n\n   humanizer_portugues.int_comma(12345)\n   "12,345"\n\n   humanizer_portugues.int_word(123455913)\n   "123.5 milhão"\n\n   humanizer_portugues.int_word(12345591313)\n   "12.3 bilhão"\n\n\nHumanization of floating point numbers:\n\n.. code-block:: python\n\n   humanizer_portugues.fractional(1/3)\n   "1/3"\n\n   humanizer_portugues.fractional(1.5)\n   "1 1/2"\n\n   humanizer_portugues.fractional(0.3)\n   "3/10"\n\n   humanizer_portugues.fractional(0.333)\n   "333/1000"\n\n   humanizer_portugues.fractional(1)\n   "1"\n\n\nHumanization of dates and time:\n\n.. code-block:: python\n\n   import datetime\n\n   humanizer_portugues.natural_clock(datetime.time(0, 30, 0))\n   "zero hora e trinta minutos"\n\n   humanizer_portugues.natural_clock(datetime.time(0, 30, 0), formal=False)\n   "meia noite e meia"\n\n   humanizer_portugues.natural_date(datetime.date(2007, 6, 5))\n   "5 de junho de 2007"\n\n   humanizer_portugues.natural_day(datetime.datetime.now())\n   "hoje"\n\n   humanizer_portugues.natural_day(datetime.datetime.now() - datetime.timedelta(days=1))\n   "ontem"\n\n   humanizer_portugues.natural_day(datetime.date(2007, 6, 5))\n   "5 de junho"\n\n   humanizer_portugues.natural_delta(datetime.timedelta(seconds=1001))\n   "16 minutos"\n\n   humanizer_portugues.natural_period(datetime.time(5, 30, 0).hour)\n   "manhã"\n\n   humanizer_portugues.natural_time(datetime.datetime.now() - datetime.timedelta(seconds=1))\n   "há um segundo"\n\n   humanizer_portugues.natural_time(datetime.datetime.now() - datetime.timedelta(seconds=3600))\n   "há uma hora"\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Humanizer Portugues* is free and open source software.\n\n\nCredits\n-------\n\nThis lib is based on original humanize_, with updates for python3, translation fixes for portuguese, changes in return format and the addition of list humanizing. Localization (i18n) was also removed.\n\n\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _pip: https://pip.pypa.io/\n.. _humanize: https://github.com/jmoiron/humanize\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n',
    'author': "Thiago Carvalho D'Ávila",
    'author_email': 'thiagocavila@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticdev/humanizer-portugues',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
