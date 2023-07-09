#!/usr/bin/env python
from setuptools import setup, find_packages
import pkg_resources
import sys
import os
import fastentrypoints


try:
    if int(pkg_resources.get_distribution("pip").version.split('.')[0]) < 6:
        print('pip older than 6.0 not supported, please upgrade pip with:\n\n'
              '    pip install -U pip')
        sys.exit(-1)
except pkg_resources.DistributionNotFound:
    pass

if os.environ.get('CONVERT_README'):
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
else:
    long_description = ''

version = sys.version_info[:2]
if version < (2, 7):
    print('thefuck requires Python version 2.7 or later' +
          ' ({}.{} detected).'.format(*version))
    sys.exit(-1)
elif (3, 0) < version < (3, 5):
    print('thefuck requires Python version 3.5 or later' +
          ' ({}.{} detected).'.format(*version))
    sys.exit(-1)

VERSION = '3.32'

install_requires = ['psutil', 'colorama', 'six']
extras_require = {':python_version<"3.4"': ['pathlib2'],
                  ':python_version<"3.3"': ['backports.shutil_get_terminal_size'],
                  ':python_version<="2.7"': ['decorator<5', 'pyte<0.8.1'],
                  ':python_version>"2.7"': ['decorator', 'pyte'],
                  ":sys_platform=='win32'": ['win_unicode_console']}

if sys.platform == "win32":
    scripts = ['scripts\\fuck.bat', 'scripts\\fuck.ps1']
    entry_points = {'console_scripts': [
                  'thefuck = thefuck.entrypoints.main:main',
                  'thefuck_firstuse = thefuck.entrypoints.not_configured:main']}
else:
    scripts = []
    entry_points = {'console_scripts': [
                  'thefuck = thefuck.entrypoints.main:main',
                  'fuck = thefuck.entrypoints.not_configured:main']}

setup(name='thefuck',
      version=VERSION,
      description="Magnificent app which corrects your previous console command",
      long_description=long_description,
      author='Vladimir Iakovlev',
      author_email='nvbn.rm@gmail.com',
      url='https://github.com/nvbn/thefuck',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples',
                                      'tests', 'tests.*', 'release']),
      include_package_data=True,
      zip_safe=False,
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
      install_requires=install_requires,
      extras_require=extras_require,
      scripts=scripts,
      entry_points=entry_points)
