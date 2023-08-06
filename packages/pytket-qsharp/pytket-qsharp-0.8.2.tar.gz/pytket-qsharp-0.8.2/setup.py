# Copyright 2020-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

import setuptools  # type: ignore
from setuptools import setup, find_namespace_packages
import shutil
import os

metadata: dict = {}
with open("_metadata.py") as fp:
    exec(fp.read(), metadata)
shutil.copy(
    "_metadata.py",
    os.path.join("pytket", "extensions", "backends", "qsharp", "_metadata.py"),
)

setup(
    name=metadata["__extension_name__"],
    version=metadata["__extension_version__"],
    author="Alec Edgington",
    author_email="alec.edgington@cambridgequantum.com",
    python_requires=">=3.6",
    url="https://github.com/CQCL/pytket",
    description="Extension for pytket, providing simulators from Microsoft QDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="CQC Software Licence",
    packages=find_namespace_packages(include=["pytket.*"]),
    include_package_data=True,
    install_requires=["pytket ~= 0.7.1", "qsharp ~= 0.14.2011"],
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: Other/Proprietary License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    zip_safe=False,
)
