# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Configuration variables."""

from invenio_banners.utils import style_category

BANNERS_CATEGORIES = [
    ("info", "Info"),
    ("warning", "Warning"),
    ("other", "Other"),
]
"""Categories to define different types of messages. List of (id, label)."""

BANNERS_CATEGORIES_TO_STYLE = style_category
"""Function to transform the banner category to a specific CSS class."""
