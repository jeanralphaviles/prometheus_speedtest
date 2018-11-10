"""Build script for setuptools, used to create PyPi package."""
import os

from setuptools import setup


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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
    ],
    description=('Performs speedtest-cli tests and pushes metrics to '
                 'Prometheus Pushgateway'),
    entry_points={
        'console_scripts': [
            'prometheus_speedtest=prometheus_speedtest:main',
        ],
    },
    install_requires=[
        'glog>=0.3.1',
        'mock>=2.0.0',
        'prometheus_client>=0.3.1',
        'speedtest-cli>=2.0.2',
    ],
    keywords=['prometheus', 'monitoring', 'speedtest', 'speedtest.net'],
    license='Apache License, Version 2.0',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    py_modules=['prometheus_speedtest'],
    setup_requires=['setuptools>=38.6.0'],
    url='https://github.com/jeanralphaviles/prometheus_speedtest',
    version=read_file('version.txt'))
