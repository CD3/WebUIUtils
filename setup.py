import os
from setuptools import setup, find_packages

__version__= '0.1'

setup(
  name = 'webuiutils',
  packages = ['webuiutils'],
  version = __version__,
  description = "A collection of command line utilies to help with building web-based user-interfaces.",
  license='MIT',
  author = 'CD Clark III',
  author_email = 'clifton.clark@gmail.com',
  url = 'https://github.com/CD3/WebUIUtils',
  download_url = f'https://github.com/CD3/WebUIUtils/archive/{__version__}.tar.gz',
  install_requires = ['click','pyyaml','fspathtree','lxml','html5print'],
  entry_points='''
  [console_scripts]
  webui=webuiutils.webui:main
  ''',
)
