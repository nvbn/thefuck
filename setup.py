from setuptools import setup, find_packages
import sys


VERSION = '1.46'

deps = ['psutil', 'colorama', 'six']

if sys.version_info < (3,4):
    deps.append('pathlib')

setup(name='thefuck',
      version=VERSION,
      description="Magnificent app which corrects your previous console command",
      author='Vladimir Iakovlev',
      author_email='nvbn.rm@gmail.com',
      url='https://github.com/nvbn/thefuck',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples',
                                      'tests', 'release']),
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
      entry_points={'console_scripts': [
          'thefuck = thefuck.main:main',
          'thefuck-alias = thefuck.shells:app_alias']})
