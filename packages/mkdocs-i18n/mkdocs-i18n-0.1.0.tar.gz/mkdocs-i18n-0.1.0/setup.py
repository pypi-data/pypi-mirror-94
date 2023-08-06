#!/bin/env python3
# -*- coding: utf-8 -*-
#
#   Copyright © 2020, 2021 Simó Albert i Beltran
#
#   This file is part of MkDocs i18n plugin.
#
#   Mkdocs i18n plugin is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   Foobar is distributed in the hope that it will be useful, but WITHOUT ANY
#   WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#   FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#   details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with MkDocs i18n plugin. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

""" Setup for mkdocs-i18n """

from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent.resolve()

setup(
    name="mkdocs-i18n",
    version="0.1.0",
    description="MkDocs i18n plugin",
    long_description=(here / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mkdocs-i18n/mkdocs-i18n",
    author="Simó Albert i Beltran",
    author_email="sim6@bona.gent",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or "
        "later (AGPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="mkdocs, plugin, i18n",
    packages=find_packages(),
    python_requires=">=3.7, <4",
    install_requires=["mkdocs>=1.1", "mkdocs-material"],
    extras_require={
        "test": [
            "isort",
            "black",
            "bandit",
            "flake8",
            "pylint",
            "mamba",
            "bs4",
            "lxml",
            "expects",
            "coverage",
            "pypi-version-check",
        ],
    },
    entry_points={"mkdocs.plugins": ["i18n = mkdocs_i18n:I18n"]},
    project_urls={
        "Bug Reports": "https://gitlab.com/mkdocs-i18n/mkdocs-i18n/-/issues",
        "Funding": "https://liberapay.com/mkdocs-i18n/donate",
        "Source": "https://gitlab.com/mkdocs-i18n/mkdocs-i18n/-/tree/main",
    },
    license="AGPL-3.0-or-later",
)
