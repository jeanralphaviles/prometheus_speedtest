"""Build script for setuptools, used to create PyPi package."""
import os

from setuptools import setup
from setuptools import find_packages

from prometheus_speedtest import version


def read_file(rel_path):
    """Reads a relative file, returns contents as a string.

    Args:
      rel_path: relative file path, string.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as rel_file:
        return rel_file.read().strip()

setup(
    name='prometheus_speedtest',
    author='Jean-Ralph Aviles',
    author_email='jeanralph.aviles+pypi@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
    ],
    description=('Performs speedtest-cli tests and pushes metrics to '
                 'Prometheus Pushgateway'),
    entry_points={
        'console_scripts': [
            ('prometheus_speedtest='
             'prometheus_speedtest.prometheus_speedtest:main'),
        ],
    },
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'absl-py==0.7.1',
        'mock==3.0.5',
        'prometheus_client==0.7.1',
        'speedtest-cli==2.1.1',
    ],
    keywords=['prometheus', 'monitoring', 'speedtest', 'speedtest.net'],
    license='Apache License, Version 2.0',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    py_modules=['prometheus_speedtest'],
    setup_requires=['setuptools>=38.6.0'],
    url='https://github.com/jeanralphaviles/prometheus_speedtest',
    version=version.VERSION)
