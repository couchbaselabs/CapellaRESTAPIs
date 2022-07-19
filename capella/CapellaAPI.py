# -*- coding: utf-8 -*-
# Generic/Built-in
import logging

from .CapellaAPIRequests import CapellaAPIRequests
import json
import base64

class CapellaAPI(CapellaAPIRequests):

    def __init__(self, url, secret, access, user, pwd):
        super(CapellaAPI, self).__init__(url, secret, access)
        self.user = user
        self.pwd = pwd
        self.internal_url = url.replace("cloud", "", 1)
        self._log = logging.getLogger(__name__)
        self.perPage = 100

    def get_authorization_internal(self):
        basic = base64.b64encode('{}:{}'.format(self.user, self.pwd).encode()).decode()
        #basic = base64.encodestring('{}:{}'.format(self.user, self.pwd).encode('utf-8')).decode('utf-8').strip("\n")
        #basic = base64.encodestring('{}:{}'.format(self.user, self.pwd)).strip("\n")
        header = {'Authorization': 'Basic %s' % basic}
        resp = self._urllib_request(
            "{}/sessions".format(self.internal_url), method="POST",
            headers=header)
        jwt = json.loads(resp.content).get("jwt")
        cbc_api_request_headers = {
           'Authorization': 'Bearer %s' % jwt,
           'Content-Type': 'application/json'
        }
        return cbc_api_request_headers

    def set_logging_level(self, level):
        self._log.setLevel(level)

    # Cluster methods
    def get_clusters(self):
        capella_api_response = self.capella_api_get('/v3/clusters')

        return (capella_api_response)

    def get_cluster_info(self, cluster_id):
        capella_api_response = self.capella_api_get('/v3/clusters/' + cluster_id)

        return (capella_api_response)

    def get_cluster_status(self, cluster_id):
        capella_api_response = self.capella_api_get('/v3/clusters/' + cluster_id + '/status')

        return (capella_api_response)

    def create_cluster(self, cluster_configuration):
        capella_api_response = self.capella_api_post('/v3/clusters', cluster_configuration)

        return (capella_api_response)

    def update_cluster_servers(self, cluster_id, new_cluster_server_configuration):
        capella_api_response = self.capella_api_put('/v3/clusters' + '/' + cluster_id + '/servers',
                                                    new_cluster_server_configuration)

        return (capella_api_response)

    def get_cluster_servers(self, cluster_id):
        response_dict = None

        capella_api_response = self.get_cluster_info(True, cluster_id)
        # Did we get the info back ?
        if capella_api_response.status_code == 200:
            # Do we have JSON response ?
            if capella_api_response.headers['content-type'] == 'application/json':
                # Is there anything in it?
                # We use response.text as this is a string
                # response.content is in bytes which we use for json.loads
                if len(capella_api_response.text) > 0:
                    response_dict = capella_api_response.json()['place']

        # return just the servers bit
        return (response_dict)

    def delete_cluster(self, cluster_id):
        capella_api_response = self.capella_api_del('/v3/clusters' + '/' + cluster_id)
        return (capella_api_response)

    def get_cluster_users(self, cluster_id):
        capella_api_response = self.capella_api_get('/v3/clusters' + '/' + cluster_id +
                                                    '/users')
        return (capella_api_response)

    def delete_cluster_user(self, cluster_id, cluster_user):
        capella_api_response = self.capella_api_del('/v3/clusters' + '/' + cluster_id +
                                                    '/users/'+ cluster_user)
        return (capella_api_response)

    # Cluster certificate
    def get_cluster_certificate(self, cluster_id):
        capella_api_response = self.capella_api_get('/v3/clusters' + '/' + cluster_id +
                                                    '/certificate')
        return (capella_api_response)

    # Cluster buckets
    def get_cluster_buckets(self, cluster_id):
        capella_api_response = self.capella_api_get('/v2/clusters' + '/' + cluster_id +
                                                    '/buckets')
        return (capella_api_response)

    def create_cluster_bucket(self, cluster_id, bucket_configuration):
        capella_api_response = self.capella_api_post('/v2/clusters' + '/' + cluster_id +
                                                     '/buckets', bucket_configuration)
        return (capella_api_response)

    def update_cluster_bucket(self, cluster_id, bucket_id, new_bucket_configuration):
        capella_api_response = self.capella_api_put('/v2/clusters' + '/' + cluster_id +
                                                    '/buckets/' + bucket_id , new_bucket_configuration)
        return (capella_api_response)

    def delete_cluster_bucket(self, cluster_id, bucket_configuration):
        capella_api_response = self.capella_api_del('/v2/clusters' + '/' + cluster_id +
                                                    '/buckets', bucket_configuration)
        return (capella_api_response)

    # Cluster Allow lists
    def get_cluster_allowlist(self, cluster_id):
        capella_api_response = self.capella_api_get('/v2/clusters' + '/' + cluster_id +
                                                    '/allowlist')
        return (capella_api_response)

    def delete_cluster_allowlist(self, cluster_id, allowlist_configuration):
        capella_api_response = self.capella_api_del('/v2/clusters' + '/' + cluster_id +
                                                    '/allowlist', allowlist_configuration)
        return (capella_api_response)

    def create_cluster_allowlist(self, cluster_id, allowlist_configuration):
        capella_api_response = self.capella_api_post('/v2/clusters' + '/' + cluster_id +
                                                     '/allowlist', allowlist_configuration)
        return (capella_api_response)

    def update_cluster_allowlist(self, cluster_id, new_allowlist_configuration):
        capella_api_response = self.capella_api_put('/v2/clusters' + '/' + cluster_id +
                                                    '/allowlist', new_allowlist_configuration)
        return (capella_api_response)

    # Cluster user
    def create_cluster_user(self, cluster_id, cluster_user_configuration):
        capella_api_response = self.capella_api_post('/v3/clusters' + '/' + cluster_id +
                                                     '/users', cluster_user_configuration)
        return (capella_api_response)

    # Capella Users
    def get_users(self):
        capella_api_response = self.capella_api_get('/v2/users?perPage=' + str(self.perPage))
        return (capella_api_response)

    def create_project(self, tenant_id, name):
        capella_header = self.get_authorization_internal()
        project_details = {"name": name, "tenantId": tenant_id}

        url = '{}/v2/organizations/{}/projects'.format(self.internal_url, tenant_id)
        capella_api_response = self._urllib_request(url, method="POST",
                                                    params=json.dumps(project_details),
                                                    headers=capella_header)
        return capella_api_response

    def delete_project(self, tenant_id, project_id):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}'.format(self.internal_url, tenant_id,
                                                          project_id)
        capella_api_response = self._urllib_request(url, method="DELETE",
                                                    params='',
                                                    headers=capella_header)
        return capella_api_response

    def create_bucket(self, tenant_id, project_id, cluster_id,
                      bucket_params):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/buckets'.format(url)
        default = {"name": "default", "bucketConflictResolution": "seqno",
                   "memoryAllocationInMb": 100, "flush": False, "replicas": 0,
                   "durabilityLevel": "none", "timeToLive": None}
        default.update(bucket_params)
        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(default),
                                    headers=capella_header)
        return resp

    def get_buckets(self, tenant_id, project_id, cluster_id):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/buckets'.format(url)
        resp = self._urllib_request(url, method="GET", params='',
                                    headers=capella_header)
        return resp

    def flush_bucket(self, tenant_id, project_id, cluster_id, bucket_id):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = url + "/" + bucket_id + "/flush"
        resp = self._urllib_request(url, method="POST",
                                    headers=capella_header)
        return resp

    def delete_bucket(self, tenant_id, project_id, cluster_id,
                      bucket_id):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/buckets/{}'.format(url, bucket_id)
        resp = self._urllib_request(url, method="DELETE",
                                    headers=capella_header)
        return resp

    def update_bucket_settings(self, tenant_id, project_id, cluster_id,
                               bucket_id, bucket_params):
        capella_header = self.get_authorization_internal()
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/{}" \
            .format(self.internal_url, tenant_id, project_id,
                    cluster_id, bucket_id)
        resp = self._urllib_request(url, method="PUT", headers=capella_header,
                                    params=json.dumps(bucket_params))
        return resp

    def jobs(self, project_id, tenant_id, cluster_id):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/jobs'.format(url)
        resp = self._urllib_request(url, method="GET", params='',
                                    headers=capella_header)
        return resp

    def get_cluster_internal(self, tenant_id, project_id, cluster_id):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)

        resp = self._urllib_request(url, method="GET",
                                    params='', headers=capella_header)
        return resp

    def get_nodes(self, tenant_id, project_id, cluster_id):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/nodes'.format(url)
        resp = self._urllib_request(url, method="GET", params='',
                                    headers=capella_header)
        return resp

    def get_db_users(self, tenant_id, project_id, cluster_id,
                     page=1, limit=100):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
              .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = url + '/users?page=%s&perPage=%s' % (page, limit)
        resp = self._urllib_request(url, method="GET", headers=capella_header)
        return resp

    def delete_db_user(self, tenant_id, project_id, cluster_id, user_id):
        capella_header = self.get_authorization_internal()
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/users/{}" \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    user_id)
        resp = self._urllib_request(url, method="DELETE",
                                    params='',
                                    headers=capella_header)
        return resp

    def create_db_user(self, tenant_id, project_id, cluster_id,
                       user, pwd):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        body = {"name": user, "password": pwd,
                "permissions": {"data_reader": {}, "data_writer": {}}}
        url = '{}/users'.format(url)
        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(body),
                                    headers=capella_header)
        return resp

    def allow_my_ip(self, tenant_id, project_id, cluster_id):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self._urllib_request("https://ifconfig.me", method="GET")
        if resp.status_code != 200:
            raise Exception("Fetch public IP failed!")
        body = {"create": [{"cidr": "{}/32".format(resp.content.decode()),
                            "comment": ""}]}
        url = '{}/allowlists-bulk'.format(url)
        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(body),
                                    headers=capella_header)
        return resp

    def add_allowed_ips(self, tenant_id, project_id, cluster_id, ips):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        body = {
            "create": [
                {"cidr": "{}/32".format(ip), "comment": ""} for ip in ips
            ]
        }
        url = '{}/allowlists-bulk'.format(url)
        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(body),
                                    headers=capella_header)
        return resp

    def load_sample_bucket(self, tenant_id, project_id, cluster_id,
                           bucket_name):
        capella_header = self.get_authorization_internal()
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/samples"\
              .format(self.internal_url, tenant_id, project_id, cluster_id)
        param = {'name': bucket_name}
        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(param),
                                    headers=capella_header)
        return resp

    def create_cluster_customAMI(self, tenant_id, config):
        '''
        #Sample Config
        config = {"cidr": "10.0.64.0/20",
          "name": "a_customAMI",
          "description": "",
          "overRide": {"token": "TOKEN_FOR_INTERNAL_SUPPORT",
                       "image": "couchbase-cloud-server-7.2.0-qe",
                       "server": "7.1.0"},
          "projectId": "e51ce483-d067-4d4e-9a66-d0583b9d543e",
          "provider": "hostedAWS",
          "region": "us-east-1",
          "singleAZ": False, "server": None,
          "specs": [
              {"count": 3,
               "services": [{"type": "fts"}, {"type": "index"}, {"type": "kv"}, {"type": "n1ql"}],
               "compute": {"type": "r5.2xlarge", "cpu": 0, "memoryInGb": 0},
               "disk": {"type": "gp3", "sizeInGb": 50, "iops": 3000}}],
          "package": "enterprise"
          }
          '''
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/clusters/deploy'.format(
            self.internal_url, tenant_id)
        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(config),
                                    headers=capella_header)
        return resp

    def get_deployment_options(self, tenant_id):
        """
        Get deployment options, including a suggested CIDR for deploying a
        cluster.

        Example use:

        ```
        resp = client.get_deployment_options(tenant_id)
        suggestedCidr = resp.json().get('suggestedCidr')
        ```
        """
        capella_header = self.get_authorization_internal()
        url = '{}/v2/organizations/{}/clusters/deployment-options' \
              .format(self.internal_url, tenant_id)
        resp = self._urllib_request(url, method="GET", headers=capella_header)
        return resp

    def create_eventing_function(self, cluster_id, name, body, function_scope=None):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/functions/{}'.format(self.internal_url, cluster_id, name)

        if function_scope is not None:
            url += "?bucket={0}&scope={1}".format(function_scope["bucket"],
                                                  function_scope["scope"])

        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(body),
                                    headers=capella_header)
        return resp

    def __set_eventing_function_settings(self, cluster_id, name, body, function_scope=None):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/functions/{}/settings'.format(self.internal_url, cluster_id, name)

        if function_scope is not None:
            url += "?bucket={0}&scope={1}".format(function_scope["bucket"],
                                                  function_scope["scope"])

        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(body),
                                    headers=capella_header)
        return resp

    def pause_eventing_function(self, cluster_id, name, function_scope=None):
        body = {
            "processing_status": False,
            "deployment_status": True,
        }
        return self.__set_eventing_function_settings(cluster_id, name, body, function_scope)

    def resume_eventing_function(self, cluster_id, name, function_scope=None):
        body = {
            "processing_status": True,
            "deployment_status": True,
        }
        return self.__set_eventing_function_settings(cluster_id, name, body, function_scope)

    def deploy_eventing_function(self, cluster_id, name, function_scope=None):
        body = {
            "deployment_status": True,
            "processing_status": True,
        }
        return self.__set_eventing_function_settings(cluster_id, name, body, function_scope)

    def undeploy_eventing_function(self, cluster_id, name, function_scope=None):
        body = {
            "deployment_status": False,
            "processing_status": False
        }
        return self.__set_eventing_function_settings(cluster_id, name, body, function_scope)

    def get_composite_eventing_status(self, cluster_id):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/status'.format(self.internal_url, cluster_id)

        resp = self._urllib_request(url, method="GET",
                                    headers=capella_header)
        return resp

    def get_all_eventing_stats(self, cluster_id, seqs_processed=False):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/stats'.format(self.internal_url, cluster_id)

        if seqs_processed:
            url += "?type=full"
        
        resp = self._urllib_request(url, method="GET",
                                    headers=capella_header)
        return resp

    def delete_eventing_function(self, cluster_id, name, function_scope=None):
        capella_header = self.get_authorization_internal()
        url = '{}/v2/databases/{}/proxy/_p/event/deleteAppTempStore/?name={}'.format(self.internal_url, cluster_id, name)

        if function_scope is not None:
            url += "&bucket={0}&scope={1}".format(function_scope["bucket"],
                                                  function_scope["scope"])
        resp = self._urllib_request(url, method="GET",
                                    headers=capella_header)
        return resp

    def create_private_network(self, tenant_id, project_id, cluster_id, 
                               private_network_params):
        capella_header = self.get_authorization_internal()
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/virtualnetworks"\
              .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(private_network_params),
                                    headers=capella_header)
        return resp

    def get_private_network(self, tenant_id, project_id, cluster_id,
                            private_network_id):
        capella_header = self.get_authorization_internal()
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/virtualnetworks/{}"\
              .format(self.internal_url, tenant_id, project_id, cluster_id, private_network_id)
        resp = self._urllib_request(url, method="GET", headers=capella_header)
        return resp

    def update_specs(self, tenant_id, project_id, cluster_id, specs):
        capella_header = self.get_authorization_internal()
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/specs"\
                .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(specs),
                                    headers=capella_header)
        return resp
                                    
    def restore_from_backup(self, cluster_name, project_name, bucket_name):
        """
        method used to restore from the backup
        :param cluster_name:
        :param project_name:
        :param bucket_name:
        :return: response object
        """
        cluster_id = self.get_cluster_id(cluster_name=cluster_name)
        payload = {"sourceClusterId": cluster_id,
                   "targetClusterId": cluster_id,
                   "options": {"services": ["data", "query", "index", "search"], "filterKeys": "", "filterValues": "",
                               "mapData": "", "includeData": "", "excludeData": "", "autoCreateBuckets": True,
                               "autoRemoveCollections": True, "forceUpdates": True}}
        tenant_id, project_id, _ = self.get_tenant_id(), self.get_project_id(
            project_name), self.get_cluster_id(cluster_name=cluster_name)
        bucket_id = self.get_backups(cluster_name=cluster_name, project_name=project_name, bucket_name=bucket_name)
        url = r"{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/{}/restore" \
            .format(self.internal_url, tenant_id, project_id, cluster_id, bucket_id)
        capella_header = self.get_authorization_internal()
        resp = self._urllib_request(url, method="POST", params=json.dumps(payload), headers=capella_header)
        return resp

    def get_cluster_id(self, cluster_name):
        return self._get_meta_data(cluster_name=cluster_name)['id']

    def get_bucket_id(self, cluster_name, project_name, bucket_name):
        tenant_id, project_id, cluster_id = self.get_tenant_id(), self.get_project_id(
            project_name), self.get_cluster_id(cluster_name=cluster_name)
        resp = self.get_buckets(tenant_id, project_id, cluster_id)
        if resp.status_code != 200:
            raise Exception("Response when trying to fetch buckets.")
        buckets = json.loads(resp.content)['buckets']['data']
        for bucket in buckets:
            if bucket['data']['name'] == bucket_name:
                return bucket['data']['id']

    def get_tenant_id(self):
        return json.loads(self.get_clusters().content)['data']['tenantId']

    def get_project_id(self, cluster_name):
        return self._get_meta_data(cluster_name=cluster_name)['projectId']

    def _get_meta_data(self, cluster_name):
        all_clusters = json.loads(self.get_clusters().content)['data']
        for cluster in all_clusters['items']:
            if cluster['name'] == cluster_name:
                return cluster

    def get_backups(self, cluster_name, project_name, bucket_name):
        """
        method to obtain a list of the current backups from backups tab
        :param cluster_name:
        :param project_name:
        :param bucket_name:
        :return: response object
        """
        tenant_id, project_id, cluster_id = self.get_tenant_id(), self.get_project_id(
            project_name), self.get_cluster_id(cluster_name=cluster_name)
        capella_header = self.get_authorization_internal()
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/backups".format(self.internal_url, tenant_id,
                                                                              project_id, cluster_id)
        resp = self._urllib_request(url, method="GET", headers=capella_header).content
        for bucket in json.loads(resp)['data']:
            if bucket['data']['bucket'] == bucket_name:
                return bucket['data']['bucketId']

    def backup_now(self, cluster_name, project_name, bucket_name):
        """
        method to trigger an on-demand backup
        :param cluster_name:
        :param project_name:
        :param bucket_name:
        :return: response object
        """
        tenant_id, project_id, cluster_id = self.get_tenant_id(), self.get_project_id(
            project_name), self.get_cluster_id(cluster_name=cluster_name)
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/backup".format(self.internal_url, tenant_id,
                                                                             project_id, cluster_id)
        payload = {"bucket": bucket_name}
        capella_header = self.get_authorization_internal()
        resp = self._urllib_request(url, method="POST", headers=capella_header, params=json.dumps(payload))
        return resp
