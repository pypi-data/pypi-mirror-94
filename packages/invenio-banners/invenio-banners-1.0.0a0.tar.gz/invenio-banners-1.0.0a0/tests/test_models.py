# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test models."""

from datetime import datetime, timedelta

import pytest

from invenio_banners.models import Banner

banners = {
    "everywhere": {
        "message": "everywhere",
        "url_path": None,
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "warning": {
        "message": "warning",
        "url_path": None,
        "category": "warning",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "with_end_datetime": {
        "message": "with_end_datetime",
        "url_path": "/",
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "end_datetime": datetime.utcnow() + timedelta(days=1),
        "active": True,
    },
    "records_only": {
        "message": "records_only",
        "url_path": "/records",
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "sub_records_only": {
        "message": "sub_records_only",
        "url_path": "/records/sub",
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "disabled": {
        "message": "disabled",
        "url_path": None,
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": False,
    },
    "expired": {
        "message": "expired",
        "url_path": None,
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=2),
        "end_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
}


def test_category(app, db):
    """Test get first active with with path and date."""
    Banner.create(**banners["warning"])
    db.session.commit()
    assert Banner.get_active().message == "warning"

    with pytest.raises(AssertionError):
        banners["warning"]["category"] = "wrong"
        Banner.create(**banners["warning"])


def test_get_with_path_datetime(app, db):
    """Test get first active with with path and date."""
    Banner.create(**banners["everywhere"])
    Banner.create(**banners["with_end_datetime"])
    Banner.create(**banners["disabled"])
    db.session.commit()

    assert Banner.get_active("/").message == "everywhere"
    assert Banner.get_active("/records").message == "everywhere"


def test_get_with_specific_path_datetime(app, db):
    """Test get first active with specific path and date."""
    Banner.create(**banners["disabled"])
    Banner.create(**banners["records_only"])
    db.session.commit()

    assert Banner.get_active("/records").message == "records_only"
    assert Banner.get_active("/records/other").message == "records_only"
    assert Banner.get_active("/") is None
    assert Banner.get_active("/other") is None


def test_get_with_sub_path_datetime(app, db):
    """Test get first active with sub path and date."""
    Banner.create(**banners["disabled"])
    Banner.create(**banners["sub_records_only"])
    db.session.commit()

    assert Banner.get_active("/records/sub").message == "sub_records_only"
    assert Banner.get_active("/records") is None
    assert Banner.get_active("/") is None
    assert Banner.get_active("/other") is None


def test_get_future_datetime(app, db):
    """Test get first active with future date."""
    Banner.create(**banners["expired"])
    Banner.create(**banners["disabled"])
    Banner.create(**banners["records_only"])
    db.session.commit()

    assert Banner.get_active("/") is None
    assert Banner.get_active("/other") is None
    assert Banner.get_active("/records").message == "records_only"


def test_get_expired_disabled(app, db):
    """Test get first active with future date."""
    Banner.create(**banners["expired"])
    Banner.create(**banners["disabled"])
    db.session.commit()

    assert Banner.get_active("/") is None
    assert Banner.get_active("/other") is None
    assert Banner.get_active("/records") is None


def test_disable_expired(app, db):
    """Test clean up old announcement but still active."""
    Banner.create(**banners["everywhere"])
    Banner.create(**banners["expired"])
    Banner.create(**banners["with_end_datetime"])
    Banner.create(**banners["sub_records_only"])
    db.session.commit()

    assert Banner.query.filter(Banner.active.is_(True)).count() == 4

    Banner.disable_expired()

    _banners = Banner.query.filter(Banner.active.is_(True)).all()
    assert len(_banners) == 3
    assert _banners[0].message == "everywhere"
    assert _banners[1].message == "with_end_datetime"
    assert _banners[2].message == "sub_records_only"
