#!/usr/bin/env python
from setuptools import setup

setup(
    name="brother",
    version="0.2.1",
    author="Maciej Bieniek",
    author_email="maciej.bieniek@gmail.com",
    description="Python wrapper for getting data from Brother laser and inkjet \
        printers via SNMP.",
    include_package_data=True,
    url="https://github.com/bieniu/brother",
    license="Apache 2",
    packages=["brother"],
    python_requires=">=3.6",
    install_requires=["pysnmp"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    setup_requires=("pytest-runner"),
    tests_require=("pytest-cov", "pytest-asyncio", "pytest-error-for-skips"),
)
