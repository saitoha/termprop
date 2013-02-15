# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from termprop import __version__, __license__, __author__
import inspect
import os

filename = inspect.getfile(inspect.currentframe())
dirpath = os.path.abspath(os.path.dirname(filename))
readme = open(os.path.join('README.rst')).read()

import termprop
termprop.test()

setup(name                  = 'termprop',
      version               = __version__,
      description           = 'detects some terminal glitches and advanced facilities information',
      long_description      = readme,
      py_modules            = ['termprop'],
      eager_resources       = [],
      classifiers           = ['Development Status :: 4 - Beta',
                               'Topic :: Terminals',
                               'Environment :: Console',
                               'Intended Audience :: Developers',
                               'License :: OSI Approved :: GNU General Public License (GPL)',
                               'Programming Language :: Python'
                               ],
      keywords              = 'terminal',
      author                = __author__,
      author_email          = 'user@zuse.jp',
      url                   = 'https://github.com/saitoha/termprop',
      license               = __license__,
      packages              = find_packages(exclude=['test']),
      zip_safe              = True,
      include_package_data  = False,
      install_requires      = [],
      entry_points          = """
                              [console_scripts]
                              termprop = termprop:main
                              """
      )
