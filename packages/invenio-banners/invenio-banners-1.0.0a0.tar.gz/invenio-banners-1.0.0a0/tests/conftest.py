# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration."""

import pytest
from flask import Flask
from flask_babelex import Babel
from invenio_admin import InvenioAdmin
from invenio_db import InvenioDB

from invenio_banners import InvenioBanners
from invenio_banners.views import api_blueprint, blueprint


@pytest.fixture(scope="module")
def app(base_app, database):
    """Override the app fixture to remove ES."""
    yield base_app


@pytest.fixture(scope="module")
def celery_config():
    """Override pytest-invenio fixture."""
    return {}


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""

    def factory(**config):
        app = Flask("testapp", instance_path=instance_path)
        app.config.update(**config)
        Babel(app)
        InvenioDB(app)

        no_permissions = dict(
            permission_factory=None, view_class_factory=lambda x: x
        )
        InvenioAdmin(app, **no_permissions)

        InvenioBanners(app)
        app.register_blueprint(blueprint)
        app.register_blueprint(api_blueprint)
        return app

    return factory
