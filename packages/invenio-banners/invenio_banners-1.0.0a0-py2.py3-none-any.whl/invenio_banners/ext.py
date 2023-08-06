# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio extension app."""

from . import config
from .utils import get_active_banner_for_request


class InvenioBanners(object):
    """Invenio-Banners extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-banners"] = self
        app.jinja_env.globals[
            "get_active_banner"
        ] = get_active_banner_for_request
        app.jinja_env.filters["style_banner_category"] = app.config[
            "BANNERS_CATEGORIES_TO_STYLE"
        ]

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("BANNERS_"):
                app.config.setdefault(k, getattr(config, k))
