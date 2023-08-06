#!/usr/bin/env python
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os

with open('README.md') as f:
    long_description = f.read()


with open(os.path.join(os.path.split(__file__)[0], 'requirements.txt')) as f:
    reqs = f.read().splitlines()

def get_version():
    return open('version.txt', 'r').read().strip()


class NumpyBuildExt(build_ext):
    """build_ext command for use when numpy headers are needed."""

    def run(self):

        # Import numpy here, only when headers are needed
        import numpy  # noqa

        # Add numpy headers to include_dirs
        self.include_dirs.append(numpy.get_include())

        # Call original build_ext command
        build_ext.run(self)


setup(name='dativascrubber',
      version=get_version(),
      description='Dativa scrubber for automatic file cleansing',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://bitbucket.org/deductive/scrubber/',
      author='Deductive',
      author_email='hello@deductive.com',
      license='MIT',
      zip_safe=False,
      packages=['dativa.analyzer',
                'dativa.scrubber'],
      include_package_data=True,
      setup_requires=[
          'setuptools>=38.6.0',
          'wheel>=0.31.0',
          'numpy>=1.13.3'],
      install_requires=reqs,
      scripts=['bin/fanalyzer'],
      test_suite='nose.collector',
      tests_require=['nose', 'coverage'],
      cmdclass={'build_ext': NumpyBuildExt},
      ext_modules=[Extension(name="dativa.scrubber.distance", sources=["dativa/scrubber/distance.pyx"])],
        classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.6'],
      keywords='dativa, data cleansing, data pipeline, deductive'
      )
