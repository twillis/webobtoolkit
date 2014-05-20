from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from distutils.core import Command
import os
import sys

version = '0.2.4'
here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except IOError:
    README = CHANGES = ""

class PyTest(TestCommand):
    test_package_name = 'webobtoolkit'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        _test_args = [
            '--verbose',
            '--ignore=build',
            '--cov={0}'.format(self.test_package_name),
            '--cov-report=term-missing',
        ]
        extra_args = os.environ.get('PYTEST_EXTRA_ARGS')
        if extra_args is not None:
            _test_args.extend(extra_args.split())
        self.test_args = _test_args
        self.test_suite = True

    def run_tests(self):
        import pytest
        from pkg_resources import normalize_path, _namespace_packages

        # Purge modules under test from sys.modules. The test loader will
        # re-import them from the build location. Required when 2to3 is used
        # with namespace packages.
        if sys.version_info >= (3,) and getattr(self.distribution, 'use_2to3', False):
            #module = self.test_args[-1].split('.')[0]
            module = self.test_package_name
            if module in _namespace_packages:
                del_modules = []
                if module in sys.modules:
                    del_modules.append(module)
                module += '.'
                for name in sys.modules:
                    if name.startswith(module):
                        del_modules.append(name)
                map(sys.modules.__delitem__, del_modules)

            ## Run on the build directory for 2to3-built code
            ## This will prevent the old 2.x code from being found
            ## by py.test discovery mechanism, that apparently
            ## ignores sys.path..
            ei_cmd = self.get_finalized_command("egg_info")

            ## Replace the module name with normalized path
            #self.test_args[-1] = normalize_path(ei_cmd.egg_base)
            self.test_args.append(normalize_path(ei_cmd.egg_base))

        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(name='webobtoolkit',
      version=version,
      description="",
      long_description=README + '\n\n' + CHANGES,
      classifiers=["Environment :: Web Environment",
                   "Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: Public Domain",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",],
      keywords='webob HTTP client',
      author='Tom Willis',
      author_email='tom.willis@gmail.com',
      url='https://github.com/twillis/webobtoolkit',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          "Webob>=1.2.2"
      ],
      tests_require = [
          "pytest",
          'pytest-cov',
      ],
      cmdclass={'test': PyTest},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
