# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os

import django
import pytest

from contrast.test.apptest.base_test import BaseContrastTest


@pytest.mark.django_db
class BaseDjangoTest(BaseContrastTest):
    @property
    def middleware_request_context(self):
        # TODO: PYT-1102
        if os.environ.get("USE_DJANGO_WSGI"):
            return "contrast.wsgi.middleware.RequestContext"
        return (
            "contrast.agent.middlewares.django_middleware.RequestContext"
            if django.VERSION >= (1, 10)
            else "contrast.agent.middlewares.legacy_django_middleware.RequestContext"
        )

    @property
    def application_module_name(self):
        return "app.wsgi"

    @property
    def application_attribute_name(self):
        return "application"
