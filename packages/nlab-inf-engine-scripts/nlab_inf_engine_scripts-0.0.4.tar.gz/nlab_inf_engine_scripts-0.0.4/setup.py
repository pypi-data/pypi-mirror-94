#!/usr/bin/env python

from distutils.core import setup

setup(
    name='nlab_inf_engine_scripts',
    packages=['nlab_inf_engine_scripts'],
    version='0.0.4',
    license='MIT',
    description='Python scripts for manipulation InfEngine.',
    author='Dmitry Makarov',
    author_email='dmakarov@nanosemantics.ru',
    install_requires=[
        'python-memcached',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            "InfEngineControl = nlab_inf_engine_scripts.InfEngineControl:main"
        ]
    }
)
