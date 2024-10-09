# -*- coding: utf-8 -*-
# Generic/Built-in
import logging

import json
from ..lib.APIRequests import APIRequests


class CommonCapellaAPI(APIRequests):

    def __init__(self, url, secret, access, user, pwd, TOKEN_FOR_INTERNAL_SUPPORT=None,
                 TOKEN_FOR_SNAPLOGIC=None):
        super(CommonCapellaAPI, self).__init__(url, secret, access)
        self.user = user
        self.pwd = pwd
        self.internal_url = url.replace("https://cloud", "https://", 1)
        self._log = logging.getLogger(__name__)
        self.perPage = 100
        self.TOKEN_FOR_INTERNAL_SUPPORT = TOKEN_FOR_INTERNAL_SUPPORT
        self.TOKEN_FOR_SNAPLOGIC = TOKEN_FOR_SNAPLOGIC
        self.cbc_api_request_headers = {
            'Authorization': 'Bearer %s' % self.TOKEN_FOR_INTERNAL_SUPPORT,
            'Content-Type': 'application/json'
        }

    def trigger_log_collection(self, cluster_id, hostname='https://cb-engineering.s3.amazonaws.com/', ticketId="", nodeId=""):
        url = self.internal_url + "/internal/support/logcollections/clusters/{}".format(cluster_id)
        payload = {
            "hostname": hostname,
            "ticketId": ticketId,
            "nodeId": nodeId
        }
        resp = self._urllib_request(url, "POST", params=json.dumps(payload),
                                    headers=self.cbc_api_request_headers)
        return resp

    def get_cluster_info_internal(self, cluster_id):
        url = self.internal_url + "/internal/support/clusters/{}".format(cluster_id)
        resp = self._urllib_request(url, "GET",
                                    headers=self.cbc_api_request_headers)
        return resp

    def get_observability_system_metric(self, cluster_id, metric_name):
        url = self.internal_url + "/internal/support/clusters/{}/metrics/{}/dp-ingestor/query".format(cluster_id, metric_name)
        resp = self._urllib_request(url, "GET",
                                    headers=self.cbc_api_request_headers)
        return resp

    def deployement_jobs(self, cluster_id):
        url = "{}/internal/support/clusters/{}/deployment-jobs".format(
            self.internal_url, cluster_id)
        resp = self._urllib_request(url, "GET",
                                    headers=self.cbc_api_request_headers)
        return resp

    def deploy_distribution_point(self, provider, region):
        body = {
            'provider': provider,
            'region': region
        }
        url = self.internal_url + '/internal/support/distribution-points'
        resp = self._urllib_request(url, "POST", params=json.dumps(body),
                                    headers=self.cbc_api_request_headers)
        return resp

    def get_cluster_tasks(self, cluster_id):
        url = self.internal_url + "/internal/support/clusters/{}/pools/default/tasks".format(cluster_id)
        resp = self._urllib_request(url, "GET",
                                    headers=self.cbc_api_request_headers)
        return resp

    def get_all_distribution_endpoints(self):
        url = self.internal_url + "/internal/support/distribution-points"
        resp = self._urllib_request(url, "GET",
                                    headers=self.cbc_api_request_headers)
        return resp

    def get_distribution_endpoint(self, id):
        url = self.internal_url + "/internal/support/distribution-points/{}".format(id)
        resp = self._urllib_request(url, "GET",
                                    headers=self.cbc_api_request_headers)
        return resp

    def delete_distribution_point(self, id):
        url = self.internal_url + "/internal/support/distribution-points/{}".format(id)
        resp = self._urllib_request(url, "DELETE",
                                    headers=self.cbc_api_request_headers)
        return resp

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
            "password": password,
            "termsOfServiceAccepted": True,
            "marketingOptIn": False
        }
        resp = self._urllib_request(url, method="POST",
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
        resp = self._urllib_request(url, method="POST")
        return resp

    def tenant_activation(self):
        url = "{}/f/activations/".format(self.internal_url)
        headers = {
            'Authorization': 'Bearer %s' % self.TOKEN_FOR_SNAPLOGIC,
            'Content-Type': 'application/json'
        }
        resp = self._urllib_request(url, "GET",
                                    headers=headers,
                                    params=json.dumps({}))
        return resp

    def activate_resource_container(self, cloud, body):
        url = "{}/internal/support/csp/{}/resource-container".format(
            self.internal_url, cloud.lower())
        resp = self._urllib_request(url, "POST",
                                    headers=self.cbc_api_request_headers,
                                    params=json.dumps(body))
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

    def revoke_access_secret_key(self, tenant_id, key_id):
        url = "{}/tokens/{}?tenantId={}".format(self.internal_url, key_id, tenant_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def create_circuit_breaker(self, cluster_id, duration_seconds = -1):
        """
        Create a deployment circuit breaker for a cluster, which prevents
        any auto-generated deployments such as auto-scaling up/down, control
        plane initiated rebalances, etc.

        Default circuit breaker duration is 24h.

        See AV-46172 for more.
        """
        url = "{}/internal/support/clusters/{}/deployments-circuit-breaker" \
              .format(self.internal_url, cluster_id)
        params = {}
        if duration_seconds > 0:
            params['timeInSeconds'] = duration_seconds
        resp = self._urllib_request(url, "POST", params=json.dumps(params),
                                    headers=self.cbc_api_request_headers)
        return resp

    def get_circuit_breaker(self, cluster_id):
        """
        Retrieve a deployment circuit breaker for a cluster.

        If circuit breaker is not set for a cluster, this returns a 404.

        See AV-46172 for more.
        """
        url = "{}/internal/support/clusters/{}/deployments-circuit-breaker" \
              .format(self.internal_url, cluster_id)
        resp = self._urllib_request(url, "GET",
                                    headers=self.cbc_api_request_headers)
        return resp

    def delete_circuit_breaker(self, cluster_id):
        """
        Delete circuit breaker for a cluster.

        See AV-46172 for more.
        """
        url = "{}/internal/support/clusters/{}/deployments-circuit-breaker" \
              .format(self.internal_url, cluster_id)
        resp = self._urllib_request(url, "DELETE",
                                    headers=self.cbc_api_request_headers)
        return resp

    def add_user_to_project(self, tenant_id, payload):
        """
        Add a user to the project

        payload = {
            "resourceId": project_ids[project_id],
            "resourceType": "project",
            "roles": [role], "users": [user["userid"]]}
        }
        """
        url = "{}/v2/organizations/{}/permissions".format(self.internal_url, tenant_id)
        resp = self.do_internal_request(url, "PUT", params=payload)
        return resp

    def remove_user_from_project(self, tenant_id, user_id, project_id):
        """
        Remove user from the project

        """
        url = "{}/v2/organizations/{}/permissions/{}/resource/{}"\
            .format(self.internal_url, tenant_id, user_id, project_id)
        resp = self.do_internal_request(url, "DELETE")
        return resp

    def create_project(self, tenant_id, name):
        project_details = {"name": name, "tenantId": tenant_id}

        url = '{}/v2/organizations/{}/projects'.format(self.internal_url, tenant_id)
        capella_api_response = self.do_internal_request(url, method="POST",
                                                        params=json.dumps(project_details))
        return capella_api_response

    def delete_project(self, tenant_id, project_id):
        url = '{}/v2/organizations/{}/projects/{}'.format(self.internal_url, tenant_id,
                                                          project_id)
        capella_api_response = self.do_internal_request(url, method="DELETE",
                                                        params='')
        return capella_api_response

    def access_project(self, tenant_id, project_id):
        url = "{}/v2/organizations/{}/projects/{}".format(self.internal_url, tenant_id,
                                                          project_id)
        capella_api_response = self.do_internal_request(url, method="GET", params='')
        return capella_api_response

    def run_query(self, cluster_id, payload):
        url = "{0}/v2/databases/{1}/proxy/_p/query/query/service" \
            .format(self.internal_url, cluster_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def create_fts_index(self, database_id, fts_index_name, payload):
        url = "{}/v2/databases/{}/proxy/_p/fts/api/bucket/{}/scope/samples/index/{}" \
            .format(self.internal_url, database_id, database_id, fts_index_name)
        resp = self.do_internal_request(url, method="PUT", params=json.dumps(payload))
        return resp

    """
    This method will create new user for capella bypassing email
    verification.
    For this to work, feature flag to bypass email verification should
    be enabled.
    Refer : https://couchbasecloud.atlassian.net/browse/AV-62504
    :param org_id ID of the organisation under which the user has to be
    created.
    :param name Name of the User to be created.
    :param email Email ID of the user to be created.
    :param password Password for the created user.
    :param roles Roles associated with the user.
    """
    def create_user(self, org_id, name, email, password,
                    roles=["organizationOwner"]):
        url = "{}/v2/organizations/{}/users".format(
            self.internal_url, org_id)
        payload = {
            "name": name,
            "email": email,
            "roles": roles,
            "password": password
        }
        resp = self.do_internal_request(
            url, method="POST", params=json.dumps(payload))
        return resp

    """
    This method will delete a capella user
    :param org_id ID of the organisation under which the user has to be
    created.
    :param user_id ID of the capella user to be deleted.
    """
    def delete_user(self, org_id, user_id):
        url = "{}/v2/organizations/{}/users/{}".format(
            self.internal_url, org_id, user_id)

        resp = self.do_internal_request(
            url, method="DELETE")
        return resp

    """
    Method to schedule maintenance jobs.
    """
    def schedule_cluster_maintenance(self, payload):
        url = "{}/internal/support/maintenance/schedules".format(
            self.internal_url)
        resp = self._urllib_request(url, "POST", params=json.dumps(payload),
                                    headers=self.cbc_api_request_headers)
        return resp

    """
    Method to schedule cluster upgrades.
    :param current_images <list> List of AMI versions which needs to be
    upgraded.
    :param new_image <str> New AMI version to which cluster/s have to be
    upgraded.
    :param start_datetime <str> Date and Time in ISO format (
    YYYY-MM-DDTHH:MM:SSZ) when upgrade jobs should start.
    :param end_datetime <str> Date and Time in ISO format (
    YYYY-MM-DDTHH:MM:SSZ) before which upgrade job should end.
    :param queue_datetime <str> Date and Time in ISO format (
    YYYY-MM-DDTHH:MM:SSZ) when the upgrade job will be queued.
    :param cluster_ids <list> List of cluster Ids. For columnar cluster pass
    cluster ID and not instance ID. If not passed, then all clusters with AMI
    version present in current_images will be upgraded.
    :param provider <str> Cloud provider. Accepted value hostedAWS,
    hostedGCP, hostedAzure.
    """
    def schedule_cluster_upgrade(
            self, current_images, new_image, start_datetime, end_datetime,
            queue_datetime, provider, cluster_ids=[]):

        payload = {
            "serviceType": "clusters",
            "config": {
                "type": "upgradeClusterImage",
                "images": {
                    "currentImages": current_images,
                    "newImage": new_image,
                    "provider": provider
                },
                "optional": False,
                "visibility": "visible",
                "title": "Cluster Upgrade",
                "priority": "Upgrade",
                "description": "Cluster Upgrade to {}.format(new_image)",
                "renewClusterCert": True
            },
            "window": {
                "startDate": start_datetime,
                "endDate": end_datetime
            },
            "schedule": {
                "queueAt": queue_datetime
            },
            "scope": "all"
        }
        if cluster_ids:
            payload["clusterIds"] = cluster_ids

        return self.schedule_cluster_maintenance(payload)
