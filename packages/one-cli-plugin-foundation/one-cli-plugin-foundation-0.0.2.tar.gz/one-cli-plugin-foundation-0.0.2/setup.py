#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'gitpython==3.1.12',
    'jinja2==2.11.3',
    'jinja2-ansible-filters==1.3.0'
]

__version__ = '0.0.2'

setup(
    name='one-cli-plugin-foundation',
    version=__version__,
    py_modules=['plugin_kube'],
    include_package_data=True,
    description='This is a one-cli plugin to help create new DNX foundations.',
    license="Apache License 2.0",
    url='https://github.com/DNXLabs/plugin-foundation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='DNX Solutions',
    author_email='contact@dnx.solutions',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=3.6'
)
