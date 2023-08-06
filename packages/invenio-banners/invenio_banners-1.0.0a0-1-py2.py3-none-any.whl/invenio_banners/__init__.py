# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create and show banners with useful messages to users."""

from .ext import InvenioBanners
from .version import __version__

__all__ = ("__version__", "InvenioBanners")
