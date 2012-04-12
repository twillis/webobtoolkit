from setuptools import setup, find_packages
import sys
import os

version = '0.0'
here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

setup(name='webobtoolkit',
      version=version,
      description="",
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[],
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          "Webob"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
