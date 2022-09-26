# -*- coding: utf-8 -*-
# Generic/Built-in
import logging

import json
from ..lib.CapellaAPIRequests import CapellaAPIRequests


class CommonCapellaAPI(CapellaAPIRequests):

    def __init__(self, url, secret, access, user, pwd):
        super(CommonCapellaAPI, self).__init__(url, secret, access)
        self.user = user
        self.pwd = pwd
        self.internal_url = url.replace("cloud", "", 1)
        self._log = logging.getLogger(__name__)
        self.perPage = 100

    def signup_user(self, full_name, email, password, tenant_name, token=None):
        """
        Invite a new user to the tenant

        Example use:

        ```
        token = "secret-token"
        resp = client.invite_user(tenant_id, user, token)
        verify_token = resp.headers["Vnd-project-Avengers-com-e2e-token"]
        user_id = resp.json()["userId"]
        ```
        """
        headers = {}
        if token:
            headers["Vnd-project-Avengers-com-e2e"] = token
        url = "{}/register".format(self.internal_url)
        body = {
            "tenant": tenant_name,
            "email": email,
            "name": full_name,
            "password": password
        }
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(body),
                                        headers=headers)
        return resp

    def verify_email(self, token):
        """
        Verify an email invitation.

        Example use:

        ```
        token = "email-verify-token"
        resp = client.verify_email(token)
        jwt = resp.json()["jwt"]
        ```
        """
        url = "{}/emails/verify/{}".format(self.internal_url, token)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def list_accessible_tenants(self):
        """
        List tenants that are accessible to the user
        """
        url = "{}/tenants".format(self.internal_url)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def create_access_secret_key(self, name, tenant_id):
        headers = {}
        url = "{}/tokens?tenantId={}".format(self.internal_url, tenant_id)
        body = {
            "name": name,
            "tenantId": tenant_id
        }
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(body),
                                        headers=headers)
        return resp