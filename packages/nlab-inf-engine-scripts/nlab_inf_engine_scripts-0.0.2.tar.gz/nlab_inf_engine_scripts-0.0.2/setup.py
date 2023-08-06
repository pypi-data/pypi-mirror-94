#!/usr/bin/env python

from distutils.core import setup

setup(
    name='nlab_inf_engine_scripts',
    packages=['scripts_python'],
    version='0.0.2',
    license='MIT',
    description='Python scripts for manipulation InfEngine.',
    author='Dmitry Makarov',
    author_email='dmakarov@nanosemantics.ru',
    download_url='https://github.com/dmakarov-0/scripts_python/archive/v0.0.1.tar.gz',
    install_requires=[
        'python-memcached',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            "InfEngineControl = scripts_python.InfEngineControl:main"
        ]
    }
)
