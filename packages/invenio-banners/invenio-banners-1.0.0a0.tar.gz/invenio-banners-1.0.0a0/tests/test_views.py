# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test views."""

from datetime import datetime

from flask import url_for

from invenio_banners.models import Banner
from invenio_banners.utils import style_category


def _create_banner(db, message, category, url_path=None):
    """Util to create a banner."""
    start_datetime = datetime.utcnow()

    banner = Banner.create(
        message=message,
        category=category,
        url_path=url_path,
        start_datetime=start_datetime,
    )
    banner.active = True
    db.session.commit()

    return banner


def test_views(app, db):
    """Test views."""
    banner = _create_banner(
        db, "This is a <br />test message", "info", url_path="/records"
    )

    with app.test_client() as client:
        res = client.get(url_for("invenio_banners_api.get_active_banner"))
        assert res.status_code == 200
        data = res.get_json()
        assert data == dict()

        for url_path in ["/records", "/records/sub"]:
            res = client.get(
                url_for(
                    "invenio_banners_api.get_active_banner", url_path=url_path
                )
            )
            assert res.status_code == 200
            data = res.get_json()
            assert data["message"] == banner.message
            assert data["category"] == banner.category
            assert data["start_datetime"] == banner.start_datetime.isoformat()
            assert data["end_datetime"] == banner.end_datetime


def test_jinja_macro(app, db):
    """Test the rendering of the banner in a template via macro."""

    tpl = """
    <html>
        <body>
            {%- from "invenio_banners/macros/banner.html" import banner -%}
            {{ banner() }}
        </body>
    </html>
    """
    template = app.jinja_env.from_string(tpl)
    # should be empty, no banners
    html = template.render()
    one_line = html.replace("\n", "").replace(" ", "")
    assert one_line == "<html><body></body></html>"

    # add one banner
    EXPECTED_MSG = "Test banner info message"
    EXPECTED_CATEGORY = "info"
    EXPECTED_CSS = "primary"
    banner = _create_banner(db, EXPECTED_MSG, EXPECTED_CATEGORY)
    css = style_category(banner.category)

    html = template.render()
    assert EXPECTED_MSG in html
    assert css.endswith(EXPECTED_CSS)
    assert css in html

    # change message and category
    EXPECTED_MSG = "Test banner warning message"
    EXPECTED_CATEGORY = "warning"
    EXPECTED_CSS = "warning"

    banner.message = EXPECTED_MSG
    banner.category = EXPECTED_CATEGORY
    db.session.commit()

    css = style_category(banner.category)

    html = template.render()
    assert EXPECTED_MSG in html
    assert css.endswith(EXPECTED_CSS)
    assert css in html
