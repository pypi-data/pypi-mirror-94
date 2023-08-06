# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Admin views."""

from flask import current_app
from flask_admin.contrib.sqla import ModelView
from invenio_admin.forms import LazyChoices

from .models import Banner


class BannersModelView(ModelView):
    """Banners admin view."""

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    page_size = 20
    column_exclude_list = ["created", "updated"]
    column_searchable_list = ["message", "url_path"]
    column_default_sort = ("active", True)

    form_columns = (
        "message",
        "url_path",
        "category",
        "start_datetime",
        "end_datetime",
        "active",
    )

    form_choices = {
        "category": LazyChoices(
            lambda: current_app.config["BANNERS_CATEGORIES"]
        )
    }

    column_descriptions = {
        "category": "Banner category.",
        "url_path": "Enter the URL path (including the first /) to define in "
                    "which part of the site the message will be active. For "
                    "example, if you enter `/records`, any URL starting with "
                    "`/records` will return an active banner (/records, "
                    "/records/1234, etc...). Empty value will make the banner "
                    "active for any URL.",
        "start_datetime": "Set to current or future date/time to delay the "
                          "banner. Input date/time in UTC timezone.",
        "end_datetime": "Date/time to make the banner inactive. Empty "
                        "value will make the banner active until manually "
                        "disabled via the active flag. Input date/time in UTC "
                        "timezone.",
    }

    def after_model_change(self, form, model, is_created):
        """Clean up old banners after an action."""
        Banner.disable_expired()

    def after_model_delete(self, model):
        """Clean up old banners after an action."""
        Banner.disable_expired()


banners_adminview = dict(
    modelview=BannersModelView, model=Banner, name="Banners"
)
