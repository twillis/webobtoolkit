from setuptools import setup, find_packages
from distutils.core import Command
import os

version = '0.1.2'
here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import pytest
        errno = pytest.main("")
        raise SystemExit(errno)

setup(name='webobtoolkit',
      version=version,
      description="",
      long_description=README + '\n\n' + CHANGES,
      classifiers=["Environment :: Web Environment",
                   "Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: Public Domain"],
      keywords='webob HTTP client',
      author='Batterii',
      author_email='tom@batterii.com',
      url='https://github.com/Batterii/webobtoolkit',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          "Webob>=1.2"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      cmdclass={"test": PyTest}
      )
