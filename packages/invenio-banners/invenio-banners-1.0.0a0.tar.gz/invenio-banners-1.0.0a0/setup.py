# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create and show banners with useful messages to users."""

import os

from setuptools import find_packages, setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = ["pytest-invenio>=1.4.0"]

extras_require = {"docs": ["Sphinx>=3"], "tests": tests_require}

extras_require["all"] = []
for reqs in extras_require.values():
    extras_require["all"].extend(reqs)

setup_requires = ["Babel>=2.6"]

install_requires = ["invenio-i18n>=1.0.0", "invenio-admin>=1.0.1"]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("invenio_banners", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="invenio-banners",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    keywords="invenio",
    license="MIT",
    author="CERN",
    author_email="info@inveniosoftware.org",
    url="https://github.com/inveniosoftware/invenio-banners",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={
        "invenio_admin.views": [
            "invenio_banners = invenio_banners.admin:banners_adminview"
        ],
        "invenio_base.apps": [
            "invenio_banners = invenio_banners:InvenioBanners"
        ],
        "invenio_base.api_apps": [
            "invenio_banners = invenio_banners:InvenioBanners"
        ],
        "invenio_base.blueprints": [
            "invenio_banners = invenio_banners.views:blueprint"
        ],
        "invenio_base.api_blueprints": [
            "invenio_banners = invenio_banners.views:api_blueprint"
        ],
        "invenio_db.alembic": ["invenio_banners = invenio_banners:alembic"],
        "invenio_db.models": ["invenio_banners = invenio_banners.models"],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 1 - Planning",
    ],
)
