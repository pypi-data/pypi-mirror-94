# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Views."""

from flask import Blueprint, jsonify, request

from invenio_banners.models import Banner

blueprint = Blueprint("invenio_banners", __name__, template_folder="templates")

api_blueprint = Blueprint("invenio_banners_api", __name__)


@api_blueprint.route("/banners/active")
def get_active_banner():
    """Return the active banner."""
    url_path = request.args.get("url_path", None)
    banner = Banner.get_active(url_path)

    result = {}
    if banner:
        result["message"] = banner.message
        result["category"] = banner.category
        result["start_datetime"] = banner.start_datetime.isoformat()
        end = banner.end_datetime.isoformat() if banner.end_datetime else None
        result["end_datetime"] = end

    return jsonify(result)
