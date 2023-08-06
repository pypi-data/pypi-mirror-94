#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


python -m check_manifest --ignore ".travis-*" && \
python -m sphinx.cmd.build -qnNW docs docs/_build/html && \
python -m pytest
python -m sphinx.cmd.build -qnNW -b doctest docs docs/_build/doctest
tests_exit_code=$?
exit "$tests_exit_code"
