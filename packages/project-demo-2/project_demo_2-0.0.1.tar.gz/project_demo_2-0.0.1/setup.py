#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='project_demo_2',
    version='0.0.1',
    author='test_author',
    author_email='18800102039@163.com',
    url='https://github.com/pypa/sampleproject',
    description=u'吃枣药丸',
    packages=['project_demo_2'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'jujube=project_demo_2:jujube',
            'pill=project_demo_2:pill'
        ]
    }
)
