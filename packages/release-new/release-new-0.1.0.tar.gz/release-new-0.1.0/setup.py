#!/usr/bin/env python
# coding: utf-8

from setuptools import find_packages, setup

distname = "release-new"
version = "0.1.0"
license = "LGPL"
description = ""
author = "Logilab"
author_email = "contact@logilab.fr"
requires = {'redbaron': '>=0.9.2,<0.10'}

install_requires = ["{0} {1}".format(d, v or "").strip() for d, v in requires.items()]

setup(
    name=distname,
    version=version,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    url='https://forge.extranet.logilab.fr/logilab/release-new',
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    entry_points={"console_scripts": ["release-new = release_new.main:main"]},
)
