# -*- coding: utf-8 -*-
# Generic/Built-in
import logging

import json
from ..lib.CapellaAPIRequests import CapellaAPIRequests


class CapellaAPI(CapellaAPIRequests):
    def __init__(self, url, username, password, TOKEN_FOR_INTERNAL_SUPPORT=None):
        super(CapellaAPI, self).__init__(url)
        self.url = url
        self.internal_url = url.replace("cloud", "", 1)

        self.user = username
        self.pwd = password
        self.TOKEN_FOR_INTERNAL_SUPPORT = TOKEN_FOR_INTERNAL_SUPPORT

        self.perPage = 100

    def create_serverless_dataplane(self, config):
        url = "{}/internal/support/serverless-dataplanes".format(self.internal_url)
        cbc_api_request_headers = {
           'Authorization': 'Bearer %s' % self.TOKEN_FOR_INTERNAL_SUPPORT,
           'Content-Type': 'application/json'
        }
        resp = self._urllib_request(url, "POST", params=config,
                                    headers=cbc_api_request_headers)
        return resp

    def get_dataplane_deployment_status(self, dataplane_id):
        url = "{}/internal/support/serverless-dataplanes/{}".format(
            self.internal_url, dataplane_id)
        cbc_api_request_headers = {
           'Authorization': 'Bearer %s' % self.TOKEN_FOR_INTERNAL_SUPPORT,
           'Content-Type': 'application/json'
        }
        resp = self._urllib_request(url, "GET",
                                    headers=cbc_api_request_headers)
        return resp

    def create_serverless_database(self, tenant_id, config):
        url = "{}/v2/organizations/{}/databases".format(self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(config))
        return resp

    def get_serverless_db_info(self, tenant_id, project_id, database_id):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}".format(
            self.internal_url, tenant_id, project_id, database_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_database_debug_info(self, database_id):
        url = "{}//internal/support/serverless-databases/{}".format(
            self.internal_url, database_id)
        cbc_api_request_headers = {
           'Authorization': 'Bearer %s' % self.TOKEN_FOR_INTERNAL_SUPPORT,
           'Content-Type': 'application/json'
        }
        resp = self._urllib_request(url, "GET",
                                    headers=cbc_api_request_headers)
        return resp

    def list_all_databases(self, tenant_id, project_id):
        url = "{}/v2/organizations/{}/projects/{}/clusters?page=1&perPage={}" \
            .format(self.internal_url, tenant_id, project_id, self.perPage)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def add_ip_allowlists(self, tenant_id, database_id, project_id, config):
        # This to to add the list of IPs provided in config for whitelisting
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/allowlists-bulk" \
            .format(self.internal_url, tenant_id, project_id, database_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(config))
        return resp

    def allow_my_ip(self, tenant_id, project_id, cluster_id):
        # This is to white-list the IP of the machine where the code is running.
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self._urllib_request("https://ifconfig.me", method="GET")
        if resp.status_code != 200:
            raise Exception("Fetch public IP failed!")
        body = {"cidr": "{}/32".format(resp.content.decode())}
        url = '{}/allowlists'.format(url)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(body))
        return resp

    def generate_keys(self, tenant_id, project_id, database_id):
        url = "{}/v2/organizations/{}/projects/{}/databases/{}/keys" \
            .format(self.internal_url, tenant_id, project_id, database_id)
        body = {}
        resp = self.do_internal_request(url, method="POST", params=json.dumps(body))
        return resp

    def delete_database(self, tenant_id, project_id, database_id):
        url = "{}/v2/organizations/{}/projects/{}/databases/{}" \
            .format(self.internal_url, tenant_id, project_id, database_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def delete_dataplane(self, dataplane_id):
        url = "{}/internal/support/serverless-dataplanes/{}" \
            .format(self.internal_url, dataplane_id)
        cbc_api_request_headers = {
           'Authorization': 'Bearer %s' % self.TOKEN_FOR_INTERNAL_SUPPORT,
           'Content-Type': 'application/json'
        }
        resp = self._urllib_request(url, "DELETE",
                                    headers=cbc_api_request_headers)
        return resp

    def pause_db(self, database_id):
        url = "{}/internal/support/serverless-hibernation/{}/pause" \
            .format(self.internal_url, database_id)
        cbc_api_request_headers = {
           'Authorization': 'Bearer %s' % self.TOKEN_FOR_INTERNAL_SUPPORT,
           'Content-Type': 'application/json'
        }
        resp = self._urllib_request(url, "DELETE",
                                    headers=cbc_api_request_headers)
        return resp

    def resume_db(self, database_id):
        url = "{}/internal/support/serverless-hibernation/{}/resume" \
            .format(self.internal_url, database_id)
        cbc_api_request_headers = {
           'Authorization': 'Bearer %s' % self.TOKEN_FOR_INTERNAL_SUPPORT,
           'Content-Type': 'application/json'
        }
        resp = self._urllib_request(url, "DELETE",
                                    headers=cbc_api_request_headers)
        return resp
