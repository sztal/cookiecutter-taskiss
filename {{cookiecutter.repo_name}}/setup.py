#!/usr/bin/env python
# pylint: disable-all
import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

version = '{{ cookiecutter.version }}'
here = os.path.dirname(__file__)
readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://{{ cookiecutter.repo_name }}.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='{{ cookiecutter.repo_name }}',
    version=version,
    description='{{ cookiecutter.project_short_description }}',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='{{ cookiecutter.full_name }}',
    author_email='{{ cookiecutter.email }}',
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}',
    packages=[
        # '{{ cookiecutter.repo_name }}',
        *find_packages()
    ],
    setup_requires=[
        'pytest-runner>=4.2<5',
    ],
    tests_require=[
        'pytest',
        'pylint',
        'pytest-pylint',
        'pytest-profiling',
        'coverage'
    ],
    package_dir={'{{ cookiecutter.repo_name }}': '{{ cookiecutter.repo_name }}'},
    include_package_data=True,
    install_requires=[
        'celery>=4.2.1,<5',
        'redis>=2.10.6,<3',
        'librabbitmq>=2.0.0,<3',
        'networkx>=2.1,<3',
        'matplotlib>=2.2.3,<3',
        'click>=6.7,<7',
        'mongoengine>=0.15.3,<1',
        'scrapy>=1.5.1,<2',
        'scrapy-splash>=0.7.2,<1',
        'dateparser>=0.7.0,<1',
        'tldextract>=2.2.0,<3',
        'cerberus>=1.2,<2'
    ],
    license='MIT',
    zip_safe=False,
    keywords='{{ cookiecutter.repo_name }}',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    entry_points="""
        [console_scripts]
        {{ cookiecutter.cli_name }}={{ cookiecutter.repo_name }}.cli:cli
    """
)
