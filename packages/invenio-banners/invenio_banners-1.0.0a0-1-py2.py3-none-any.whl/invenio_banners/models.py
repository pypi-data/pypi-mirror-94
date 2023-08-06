# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Models."""

from datetime import datetime

from flask import current_app
from invenio_db import db
from sqlalchemy_utils.models import Timestamp


class Banner(db.Model, Timestamp):
    """Defines a message to show to users."""

    __tablename__ = "banners"
    __versioned__ = {"versioning": False}

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text, nullable=False)
    """The message content."""

    url_path = db.Column(db.String(255), nullable=True)
    """Define in which URL /path the message will be visible."""

    category = db.Column(db.String(20), nullable=False)
    """Category of the message, for styling messages per category."""

    start_datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    """Start date and time (UTC), can be immediate or delayed."""

    end_datetime = db.Column(db.DateTime, nullable=True)
    """End date and time (UTC), must be after `start` or forever if null."""

    active = db.Column(db.Boolean(name="active"), nullable=False, default=True)
    """Defines if the message is active, only one at the same time."""

    @classmethod
    def create(
        cls,
        message,
        category,
        url_path=None,
        start_datetime=None,
        end_datetime=None,
        active=False,
    ):
        """Create a new banner."""
        _categories = [t[0] for t in current_app.config["BANNERS_CATEGORIES"]]
        assert category in _categories
        with db.session.begin_nested():
            obj = cls(
                message=message,
                category=category,
                url_path=url_path,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                active=active,
            )
            db.session.add(obj)
        return obj

    @classmethod
    def get_active(cls, url_path=None):
        """Return the active banner, optionally for the given /path or None."""
        url_path = url_path or ""
        now = datetime.utcnow()

        query = (
            cls.query.filter(cls.active.is_(True))
            .filter(cls.start_datetime <= now)
            .filter((cls.end_datetime.is_(None)) | (now <= cls.end_datetime))
        )

        for banner in query.all():
            if banner.url_path is None or url_path.startswith(banner.url_path):
                return banner

        return None

    @classmethod
    def disable_expired(cls):
        """Disable any old still active messages to keep everything clean."""
        now = datetime.utcnow()

        query = (
            cls.query.filter(cls.active.is_(True))
            .filter(cls.end_datetime.isnot(None))
            .filter(cls.end_datetime < now)
        )

        for old in query.all():
            old.active = False

        db.session.commit()
