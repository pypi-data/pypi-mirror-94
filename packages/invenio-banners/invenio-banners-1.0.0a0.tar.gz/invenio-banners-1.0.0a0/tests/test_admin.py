# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test admin views."""

import html
from datetime import datetime, timedelta

from flask import url_for
from invenio_db import db

from invenio_banners.models import Banner


def test_admin_views(app):
    """Test admin views."""
    start_datetime = datetime.now()
    end_datetime = start_datetime + timedelta(days=2)

    banner = Banner.create(
        message="This is a <br />test message",
        category="info",
        url_path="/records",
        start_datetime=start_datetime,
        end_datetime=end_datetime,
    )
    db.session.commit()

    with app.test_client() as client:
        res = client.get(url_for("banner.index_view"))
        assert res.status_code == 200
        _html = res.get_data(as_text=True)
        assert str(banner.id) in _html
        assert html.escape(banner.message) in _html
        assert banner.category in _html
        assert banner.url_path in _html
        assert start_datetime.strftime("%Y-%m-%d %H:%M:%S") in _html
        assert end_datetime.strftime("%Y-%m-%d %H:%M:%S") in _html
