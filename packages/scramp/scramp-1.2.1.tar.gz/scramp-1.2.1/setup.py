#!/usr/bin/env python

from setuptools import setup

import versioneer

long_description = """

Scramp
------

A pure-Python implementation of the SCRAM authentication protocol."""

cmdclass = dict(versioneer.get_cmdclass())
version = versioneer.get_version()

setup(
    name="scramp",
    maintainer="Tony Locke",
    maintainer_email="tlocke@tlocke.org.uk",
    version=version,
    cmdclass=cmdclass,
    description="An implementation of the SCRAM protocol.",
    long_description=long_description,
    url="https://github.com/tlocke/scramp",
    license="MIT",
    python_requires='>=3.6',
    install_requires=['asn1crypto==1.4.0'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: Jython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="SCRAM authentication SASL",
    packages=("scramp",)
)
