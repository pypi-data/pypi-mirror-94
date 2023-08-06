# -*- coding: utf-8 -*-

import setuptools
from equit_ease.main import __equity_version__

version = __equity_version__

long_description = open("README.md").read()

setuptools.setup(
    name="EquitEase",
    version= version,
    url="https://github.com/danmurphy1217/equit-ease",
    entry_points={
        "console_scripts": ['equity=equit_ease.main:run']
    },
    description = "The easiest way to retrieve equity data from the command line. Search Stocks, Options, Cryptocurrencies and other digital assets, and more in a manner of seconds.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author= "Dan Murphy",
    author_email = "danielmurph8@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages= setuptools.find_packages(),
    install_requires = ['PyInquirer==1.0.3', 'requests==2.25.1'],
    python_requires = ">= 3.7"
)