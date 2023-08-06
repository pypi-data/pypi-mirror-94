#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

install_requires = [
    'boto==2.49.0',
    'tqdm==4.50.2',
    'PyYAML==5.3.1',
    'boto3==1.16.43',
    'appdirs==1.4.4',
    'urllib3==1.25.8',
    'inquirer==2.7.0',
    'colorlog==4.6.2',
    'blessed==1.17.6',
    'awscli==1.18.205',
    'selenium==3.141.0',
    'botocore==1.19.45',
]

setup_options = dict(
    name="bombaat",
    version='1.1.0',
    author="Ravi Boodher",
    author_email="boodher@gmail.com",
    description="Bombaat CLI - awscli / boto AWS API access using Azure Active Directory (AD) service.",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['tests*']),
    package_data={'': ['*']},
    include_package_data=True,
    install_requires=install_requires,
    extras_require={},
    entry_points={
            "console_scripts": [
                "bombaat=bombaat.__main__:main",
            ]
        },

    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        'Environment :: Console',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],
    python_requires='>=3.6',
)

setup(**setup_options)
