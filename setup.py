import os

from setuptools import find_packages
from setuptools import setup

def read_file(rel_path):
  here = os.path.abspath(os.path.dirname(__file__))
  with open(os.path.join(here, rel_path), 'r') as f:
    return f.read()

setup(
  name = 'prometheus_speedtest',
  author = 'Jean-Ralph Aviles',
  author_email = 'jeanralph.aviles+pypi@gmail.com',
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Topic :: System :: Monitoring',
    'Topic :: System :: Networking :: Monitoring',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.4',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python',
  ],
  description = (
    'Performs speedtest-cli tests and pushes metrics to Prometheus Pushgateway'
  ),
  entry_points = {
    'console_scripts': [
      'prometheus_speedtest=prometheus_speedtest:main',
    ],
  },
  install_requires = [
    'glog>=0.3.1',
    'mock>=2.0.0',
    'prometheus_client>=0.3.1',
    'speedtest-cli>=2.0.2',
  ],
  keywords = ['prometheus', 'monitoring', 'speedtest', 'speedtest.net'],
  license='Apache License, Version 2.0',
  long_description = read_file('README.md'),
  long_description_content_type = 'text/markdown',
  py_modules = ['prometheus_speedtest'],
  setup_requires=[
    'setuptools>=38.6.0'
  ],
  url = 'https://github.com/jeanralphaviles/prometheus_speedtest',
  version = read_file('version.txt'),
)
