# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utils."""

from flask import request

from invenio_banners.models import Banner


def get_active_banner_for_request():
    """Get active banner for the current URL path request."""
    url_path = request.path
    return Banner.get_active(url_path)


def style_category(category):
    """Return predefined Boostrap CSS classes for each banner category."""
    css_class = "alert alert-{}"
    if category == "warning":
        css_class = css_class.format("warning")
    elif category == "other":
        css_class = css_class.format("secondary")
    else:
        css_class = css_class.format("primary")
    return css_class
