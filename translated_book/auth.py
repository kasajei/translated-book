# -*- coding: utf-8 -*-
from djangae.contrib.gauth.middleware import AuthenticationMiddleware


class CustomAuth(AuthenticationMiddleware):
    def process_request(self, request):
        path = str(request.path)
        if path.startswith("/admin/"):
            return super(CustomAuth, self).process_request(request)
        if path.startswith("/docs/"):
            return super(CustomAuth, self).process_request(request)
        return None