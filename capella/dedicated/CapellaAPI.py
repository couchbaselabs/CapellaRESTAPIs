# -*- coding: utf-8 -*-
# Generic/Built-in
import base64
import json

from ..common.CapellaAPI import CommonCapellaAPI


class CapellaAPI(CommonCapellaAPI):

    def set_logging_level(self, level):
        self._log.setLevel(level)

    # Cluster methods
    def get_clusters(self, params=None):
        api_response = self.api_get('/v3/clusters', params)
        return (api_response)

    def get_cluster_info(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'.format(
            self.internal_url, tenant_id, project_id, cluster_id
        )
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_project_clusters(self, tenant_id, project_id, page=1, per_page=100):
        url = "{}/v2/organizations/{}/projects/{}/clusters?page={}&perPage={}".format(
            self.internal_url, tenant_id, project_id, page, per_page
        )
        resp = self.do_internal_request(url, method="GET")
        return resp


    def get_cluster_status(self, cluster_id):
        api_response = self.api_get('/v3/clusters/' + cluster_id + '/status')

        return (api_response)

    def create_cluster(self, cluster_configuration):
        api_response = self.api_post('/v3/clusters', cluster_configuration)

        return (api_response)

    def update_cluster_servers(self, cluster_id, new_cluster_server_configuration):
        api_response = self.api_put('/v3/clusters' + '/' + cluster_id + '/servers',
                                                    new_cluster_server_configuration)

        return (api_response)

    def get_cluster_servers(self, cluster_id):
        response_dict = None

        api_response = self.get_cluster_info(True, cluster_id)
        # Did we get the info back ?
        if api_response.status_code == 200:
            # Do we have JSON response ?
            if api_response.headers['content-type'] == 'application/json':
                # Is there anything in it?
                # We use response.text as this is a string
                # response.content is in bytes which we use for json.loads
                if len(api_response.text) > 0:
                    response_dict = api_response.json()['place']

        # return just the servers bit
        return (response_dict)

    def delete_cluster(self, cluster_id):
        api_response = self.api_del('/v3/clusters' + '/' + cluster_id)
        return (api_response)

    def delete_cluster_internal(self, tenant_id, project_id, cluster_id):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}".format(
            self.internal_url, tenant_id, project_id, cluster_id
        )
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def get_cluster_users(self, cluster_id):
        api_response = self.api_get('/v3/clusters' + '/' + cluster_id +
                                                    '/users')
        return (api_response)

    def delete_cluster_user(self, cluster_id, cluster_user):
        api_response = self.api_del('/v3/clusters' + '/' + cluster_id +
                                                    '/users/'+ cluster_user)
        return (api_response)

    # Cluster certificate
    def get_cluster_certificate(self, cluster_id):
        api_response = self.api_get('/v3/clusters' + '/' + cluster_id +
                                                    '/certificate')
        return (api_response)

    # Cluster buckets
    def get_cluster_buckets(self, cluster_id):
        api_response = self.api_get('/v2/clusters' + '/' + cluster_id +
                                                    '/buckets')
        return (api_response)

    def create_cluster_bucket(self, cluster_id, bucket_configuration):
        api_response = self.api_post('/v2/clusters' + '/' + cluster_id +
                                                     '/buckets', bucket_configuration)
        return (api_response)

    def update_cluster_bucket(self, cluster_id, bucket_id, new_bucket_configuration):
        api_response = self.api_put('/v2/clusters' + '/' + cluster_id +
                                                    '/buckets/' + bucket_id , new_bucket_configuration)
        return (api_response)

    def delete_cluster_bucket(self, cluster_id, bucket_configuration):
        api_response = self.api_del('/v2/clusters' + '/' + cluster_id +
                                                    '/buckets', bucket_configuration)
        return (api_response)

    # Cluster Allow lists
    def get_cluster_allowlist(self, cluster_id):
        api_response = self.api_get('/v2/clusters' + '/' + cluster_id +
                                                    '/allowlist')
        return (api_response)

    def delete_cluster_allowlist(self, cluster_id, allowlist_configuration):
        api_response = self.api_del('/v2/clusters' + '/' + cluster_id +
                                                    '/allowlist', allowlist_configuration)
        return (api_response)

    def create_cluster_allowlist(self, cluster_id, allowlist_configuration):
        api_response = self.api_post('/v2/clusters' + '/' + cluster_id +
                                                     '/allowlist', allowlist_configuration)
        return (api_response)

    def update_cluster_allowlist(self, cluster_id, new_allowlist_configuration):
        api_response = self.api_put('/v2/clusters' + '/' + cluster_id +
                                                    '/allowlist', new_allowlist_configuration)
        return (api_response)

    # Cluster user
    def create_cluster_user(self, cluster_id, cluster_user_configuration):
        api_response = self.api_post('/v3/clusters' + '/' + cluster_id +
                                                     '/users', cluster_user_configuration)
        return (api_response)

    # Capella Users
    def get_users(self):
        api_response = self.api_get('/v2/users?perPage=' + str(self.perPage))
        return (api_response)

    def create_bucket(self, tenant_id, project_id, cluster_id,
                      bucket_params):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/buckets'.format(url)
        default = {"name": "default", "bucketConflictResolution": "seqno",
                   "memoryAllocationInMb": 100, "flush": False, "replicas": 0,
                   "durabilityLevel": "none", "timeToLive": None}
        default.update(bucket_params)
        resp = self.do_internal_request(url, method="POST",
                                    params=json.dumps(default))
        return resp

    def get_buckets(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/buckets'.format(url)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_bucket(self, tenant_id, project_id, cluster_id, bucket_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/buckets/{}'.format(url, bucket_id)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def flush_bucket(self, tenant_id, project_id, cluster_id, bucket_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = url + "/buckets/" + bucket_id + "/flush"
        resp = self.do_internal_request(url, method="POST")
        return resp

    def delete_bucket(self, tenant_id, project_id, cluster_id,
                      bucket_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/buckets/{}'.format(url, bucket_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def update_bucket_settings(self, tenant_id, project_id, cluster_id,
                               bucket_id, bucket_params):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/{}" \
            .format(self.internal_url, tenant_id, project_id,
                    cluster_id, bucket_id)
        resp = self.do_internal_request(url, method="PUT", params=json.dumps(bucket_params))
        return resp

    def get_cluster_specs(self, tenant_id, project_id, cluster_id):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/specs" \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def jobs(self, project_id, tenant_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/jobs'.format(url)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_cluster_internal(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)

        resp = self.do_internal_request(url, method="GET",
                                    params='')
        return resp

    def get_nodes(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/nodes'.format(url)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_db_users(self, tenant_id, project_id, cluster_id,
                     page=1, limit=100):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
              .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = url + '/users?page=%s&perPage=%s' % (page, limit)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_db_user(self, tenant_id, project_id, cluster_id, user_id):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/users/{}" \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    user_id)
        resp = self.do_internal_request(url, method="DELETE",
                                    params='')
        return resp

    def create_db_user(self, tenant_id, project_id, cluster_id,
                       user, pwd, credential_type="basic"):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        body = {"name": user, "password": pwd,
                "permissions": {"data_reader": {}, "data_writer": {}},
                "credentialType": credential_type}
        url = '{}/users'.format(url)
        resp = self.do_internal_request(url, method="POST",
                                    params=json.dumps(body))
        return resp

    def allow_my_ip(self, tenant_id, project_id, cluster_id, all=False):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        body = dict()
        if all:
            body = {"create": [{"cidr": "0.0.0.0/0",
                                "comment": ""}]}
        else:
            resp = self._urllib_request("https://ifconfig.me", method="GET")
            if resp.status_code != 200:
                raise Exception("Fetch public IP failed!")
            body = {"create": [{"cidr": "{}/32".format(resp.content.decode()),
                                "comment": ""}]}
        url = '{}/allowlists-bulk'.format(url)
        resp = self.do_internal_request(url, method="POST",
                                    params=json.dumps(body))
        return resp

    def enable_data_api(self, cluster_id, rate=5000):
        """
        Enable data API for a cluster.
        """
        url="{}/internal/support/clusters/{}/data-api".format(self.internal_url, cluster_id)
        data = {
            "enabled": True,
            "rateLimit": rate
        }
        resp = self._urllib_request(url, "PUT", params=json.dumps(data),
                                    headers=self.cbc_api_request_headers)
        return resp

    def add_allowed_ips(self, tenant_id, project_id, cluster_id, ips):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        body = {
            "create": [
                {"cidr": "{}/32".format(ip), "comment": ""} for ip in ips
            ]
        }
        url = '{}/allowlists-bulk'.format(url)
        resp = self.do_internal_request(url, method="POST",
                                    params=json.dumps(body))
        return resp

    def load_sample_bucket(self, tenant_id, project_id, cluster_id,
                           bucket_name):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/samples"\
              .format(self.internal_url, tenant_id, project_id, cluster_id)
        param = {'name': bucket_name}
        resp = self.do_internal_request(url, method="POST",
                                    params=json.dumps(param))
        return resp

    def configure_autoscaling(self, cluster_id, config):
        """
        method to alter compute autoscaling config.
        :param cluster_id:
        :param config:
        :return: response object
        """
        url = "{}/internal/support/clusters/{}/auto-scaling-config"\
            .format(self.internal_url, cluster_id)
        resp = self._urllib_request(url, method="PUT",
                                    params=json.dumps(config),
                                    headers=self.cbc_api_request_headers)
        return resp

    def upgrade_dp_agent(self, cluster_id, version_hash):
        url = "{}/internal/support/clusters/{}/agent-versions/activate"\
              .format(self.internal_url, cluster_id)
        param = {'hash': version_hash}
        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(param),
                                    headers=self.cbc_api_request_headers)
        return resp

    def create_cluster_CPUI(self, tenant_id, config):
        '''
        #Sample Config
        {
            "server": "7.2.0",
            "timezone": "PT",
            "description": "Amazing Cloud",
            "singleAZ": False,
            "specs":
            [
                {
                    "count": 3,
                    "services":
                    [
                        "kv",
                        "n1ql"
                    ],
                    "compute": "n2-standard-8",
                    "disk":
                    {
                        "type": "pd-ssd",
                        "sizeInGb": 500
                    },
                    "provider": "hostedGCP",
                    "diskAutoScaling":
                    {
                        "enabled": True
                    }
                },
                {
                    "count": 3,
                    "services":
                    [
                        "index"
                    ],
                    "compute": "n2-standard-8",
                    "disk":
                    {
                        "type": "pd-ssd",
                        "sizeInGb": 500
                    },
                    "provider": "hostedGCP",
                    "diskAutoScaling":
                    {
                        "enabled": True
                    }
                }
            ],
            "provider": "hostedGCP",
            "name": "riteshagarwal007_gcp_C1",
            "cidr": NONE,
            "region": "us-east1",
            "plan": "Enterprise",
            "projectId": ""
        }
        '''
        url = '{}/v2/organizations/{}/clusters'.format(
            self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
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
        url = '{}/v2/organizations/{}/clusters/deploy'.format(
            self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def upgrade_cluster(self, tenant_id, project_id, cluster_id, config):
        '''
        Sample Config
        {
            "token": "",
            "image": "couchbase-cloud-server-7.1.4-3639-v1.0.17",
            "server": "7.1.4",
            "releaseID": "1.0.17"
        }
        '''
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/version'.format(
            self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def get_deployment_options(
        self, tenant_id, provider="aws", option=None, region=None, plan=None
    ):
        """
        Get deployment options for an operational cluster.

        Required Parameters:
            `tenant_id` (str): The ID of the tenant to get options for.
        Optional Parameters:
            `provider` (str): Cloud service provider (e.g., AWS, GCP).
            `option` (str): Cluster type (e.g. single, multi, custom, free-tier).
            `region` (str): CSP region or location (provider is required if this is specified).
            `plan` (str): The plan type (e.g., free, Basic, Developer Pro, Enterprise).
        """
        url = "{}/v2/organizations/{}/clusters/deployment-options/v2".format(
            self.internal_url, tenant_id
        )
        params = {
            "provider": provider,
            "option": option,
            "region": region,
            "plan": plan,
        }
        param_str = "&".join(
            "{}={}".format(k, v) for k, v in params.items() if v is not None
        )
        if param_str:
            url += "?" + param_str

        resp = self.do_internal_request(url, method="GET")
        return resp

    def create_eventing_function(self, cluster_id, name, body, function_scope=None):
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/functions/{}'.format(self.internal_url, cluster_id, name)

        if function_scope is not None:
            url += "?bucket={0}&scope={1}".format(function_scope["bucket"],
                                                  function_scope["scope"])

        resp = self.do_internal_request(url, method="POST",
                                    params=json.dumps(body))
        return resp

    def get_eventing_functions(self, cluster_id):
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/functions'.format(self.internal_url, cluster_id)

        resp = self.do_internal_request(url, method="GET")
        return resp

    def __set_eventing_function_settings(self, cluster_id, name, body, function_scope=None):
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/functions/{}/settings'.format(self.internal_url, cluster_id, name)

        if function_scope is not None:
            url += "?bucket={0}&scope={1}".format(function_scope["bucket"],
                                                  function_scope["scope"])

        resp = self.do_internal_request(url, method="POST",
                                    params=json.dumps(body))
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
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/status'.format(self.internal_url, cluster_id)

        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_all_eventing_stats(self, cluster_id, seqs_processed=False):
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/stats'.format(self.internal_url, cluster_id)

        if seqs_processed:
            url += "?type=full"

        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_eventing_function(self, cluster_id, name, function_scope=None):
        url = '{}/v2/databases/{}/proxy/_p/event/deleteAppTempStore/?name={}'.format(self.internal_url, cluster_id, name)

        if function_scope is not None:
            url += "&bucket={0}&scope={1}".format(function_scope["bucket"],
                                                  function_scope["scope"])
        resp = self.do_internal_request(url, method="GET")
        return resp

    def create_private_network(self, tenant_id, project_id, cluster_id,
                               private_network_params):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/virtualnetworks"\
              .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(private_network_params))
        return resp

    def get_private_network(self, tenant_id, project_id, cluster_id,
                            private_network_id):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/virtualnetworks/{}"\
              .format(self.internal_url, tenant_id, project_id, cluster_id, private_network_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def update_specs(self, tenant_id, project_id, cluster_id, specs):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/specs"\
                .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST",
                                    params=json.dumps(specs))
        return resp

    def restore_from_backup(self, tenant_id, project_id, cluster_id, bucket_name):
        """
        method used to restore from the backup
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param bucket_name:
        :return: response object
        """
        payload = {"sourceClusterId": cluster_id,
                   "targetClusterId": cluster_id,
                   "options": {"services": ["data", "query", "index", "search"], "filterKeys": "", "filterValues": "",
                               "mapData": "", "includeData": "", "excludeData": "", "autoCreateBuckets": True,
                               "autoRemoveCollections": True, "forceUpdates": True}}
        bucket_id = self.get_backups_bucket_id(tenant_id=tenant_id,
                                               project_id=project_id,
                                               cluster_id=cluster_id,
                                               bucket_name=bucket_name)
        url = r"{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/{}/restore" \
            .format(self.internal_url, tenant_id, project_id, cluster_id, bucket_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
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

    def get_restores(self, tenant_id, project_id, cluster_id, bucket_name):
        """
        method used to obtain list of restores of a given bucket.
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param bucket_name:
        :return: response object
        """

        bucket_id = base64.urlsafe_b64encode(bucket_name.encode()).decode()

        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/{}/restore".format(
            self.internal_url, tenant_id, project_id, cluster_id, bucket_id)

        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_backups(self, tenant_id, project_id, cluster_id):
        """
        method to obtain a list of the current backups from backups tab
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :return: response object
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/backups".format(
            self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_backups_bucket_id(self, tenant_id, project_id, cluster_id, bucket_name):
        """
        method to obtain a list of the current backups from backups tab
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param bucket_name:
        :return: response object
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/backups".format(
            self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="GET").content
        for bucket in json.loads(resp)['data']:
            if bucket['data']['bucket'] == bucket_name:
                return bucket['data']['bucketId']

    def set_backup_ami(self, tenant_id, project_id, cluster_id, backup_ami):
        """
        method to override backup client ami
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param backup_ami:
        :return: response object
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/backup-image".format(
            self.internal_url, tenant_id, project_id, cluster_id)
        payload = {"image": backup_ami}
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def backup_now(self, tenant_id, project_id, cluster_id, bucket_name):
        """
        method to trigger an on-demand backup
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param bucket_name:
        :return: response object
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/backup".format(
            self.internal_url, tenant_id, project_id, cluster_id)
        payload = {"bucket": bucket_name}
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def list_all_bucket_backups(self, tenant_id, project_id, cluster_id, bucket_id):
        """
        method to obtain the list of backups of a bucket
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param bucket_id:
        :return: response object
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/{}/backups" \
            .format(self.internal_url, tenant_id, project_id, cluster_id, bucket_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def begin_export(self, tenant_id, project_id, cluster_id, backup_id):
        """
        method to begin an export
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param backup_id:
        :return: response object
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/backups/{}/export" \
            .format(self.internal_url, tenant_id, project_id, cluster_id, backup_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def export_status(self, tenant_id, project_id, cluster_id, bucket_id):
        """
        method to query what exports are queued, executing and finished
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param bucket_id:
        :return: response object
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/{}/exports?page=1&perPage=25" \
            .format(self.internal_url, tenant_id, project_id, cluster_id, bucket_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def generate_export_link(self, tenant_id, project_id, cluster_id, export_id):
        """
        method to generate a pre-signed link for the given export
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param export_id:
        :return: response object
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/exports/{}/link" \
            .format(self.internal_url, tenant_id, project_id, cluster_id, export_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def invite_new_user(self, tenant_id, email, password):
        "Invite a new user to the tenant"
        config = {
            "email": email,
            "name": email,
            "password": password,
            "roles": ["organizationOwner"]
        }
        url = "{}/v2/organizations/{}/users" \
            .format(self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def invite_new_user_with_config(self, tenant_id, config):
        "Invite a new user to the tenant, with the config already provided"
        url = "{}/v2/organizations/{}/users" \
            .format(self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def fetch_all_invitations(self):
        """
        Fetches all the invitations for a user
        :return: list of invitations
        """
        url = "{}/invitations".format(self.internal_url)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def manage_invitation(self, invitation_id, action):
        """
        Method to accept or reject an invitation
        :param invitation_id: Id of the invitation that needs to be
        accepted or rejected.
        :param action: accept/decline
        :return:
        """
        url = "{}/invitations/{}".format(self.internal_url, invitation_id)
        resp = self.do_internal_request(url, method="PUT",
                                        params=json.dumps({"action": action}))
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

    def remove_user(self, tenant_id, user_id):
        """
        Remove a user from the tenant
        """
        url = "{}/v2/organizations/{}/users/{}".format(self.internal_url, tenant_id, user_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def create_xdcr_replication(self, tenant_id, project_id, cluster_id, payload):
        """
        Create a new XDCR replication

        Sample payload:
        {
            "direction": "one-way",
            "sourceBucket": "YnVja2V0LTE=",
            "target": {
                "cluster": "21a51ea3-4fc6-42ee-90f3-d26334fc3ace",
                "bucket":"YnVja2V0LTE=",
                "scopes": [
                    {
                        "source": "scope-1",
                        "target": "target-scope-1",
                        "collections": [
                            {
                                "source": "coll-1",
                                "target": "target-coll-1"
                            }
                        ]
                    }
                ]
            },
            "settings": {
                "filterExpression": "REGEXP_CONTAINS(country, \"France\")",
                "priority": "medium",
                "networkUsageLimit": 500
            }
        }
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr"\
              .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(payload))
        return resp

    def list_cluster_replications(self, tenant_id, project_id, cluster_id):
        """
        Get all XDCR replications for a cluster
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr"\
              .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_replication(self, tenant_id, project_id, cluster_id, replication_id):
        """
        Get a specific XDCR replication for a cluster
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr/{}"\
              .format(self.internal_url, tenant_id, project_id, cluster_id, replication_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_replication(self, tenant_id, project_id, cluster_id, replication_id):
        """
        Delete an XDCR replication
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr/{}"\
              .format(self.internal_url, tenant_id, project_id, cluster_id, replication_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def pause_replication(self, tenant_id, project_id, cluster_id, replication_id):
        """
        Pause an XDCR replication
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr/{}/pause"\
              .format(self.internal_url, tenant_id, project_id, cluster_id, replication_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def start_replication(self, tenant_id, project_id, cluster_id, replication_id):
        """
        Start an XDCR replication
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr/{}/start"\
              .format(self.internal_url, tenant_id, project_id, cluster_id, replication_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def create_sgw_backend(self, tenant_id, config):
        """
        Create a SyncGateway backend (app services) for a cluster

        Sample config:
        {
            "clusterId": "a2b3dfbb-6e88-4309-a4c1-ea3184d95321",
            "name": "my-sync-gateway-backend",
            "description": "sgw backend that drives my amazing app",
            "SyncGatewaySpecs": {
                "desired_capacity": 1,
                "compute": {
                    "type": "c5.large",
                    "cpu": 2
                    "memoryInGb": 4
                }
            }
        }
        """
        url = '{}/v2/organizations/{}/backends'.format(self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def get_sgw_backend(self, tenant_id, project_id, cluster_id, backend_id):
        """
        Get details about a SyncGateway backend for a cluster
        """
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_sgw_backend(self, tenant_id, project_id, cluster_id, backend_id):
        """
        Delete a SyncGateway backend
        """
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def create_sgw_database(self, tenant_id, project_id, cluster_id, backend_id, config):
        """
        Create a SyncGateway database (app endpoint)

        Sample config:
        {
            "name": "sgw-1",
            "sync": "",
            "bucket": "bucket-1",
            "delta_sync": false,
            "import_filter": ""
        }
        """
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def get_sgw_databases(self, tenant_id, project_id, cluster_id, backend_id):
        "Get a list of all available sgw databases (app endpoints)"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases?page=1&perPage=250' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def update_sgw_database(self, tenant_id, project_id, cluster_id, backend_id, db_name, config):
        "Update the sgw database (app endpoint)"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="PUT",
                                        params=json.dumps(config))
        return resp

    def resume_sgw_database(self, tenant_id, project_id, cluster_id, backend_id, db_name):
        "Resume the sgw database (app endpoint)"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/online' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def pause_sgw_database(self, tenant_id, project_id, cluster_id, backend_id, db_name):
        "Resume the sgw database (app endpoint)"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/offline' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def allow_my_ip_sgw(self, tenant_id, project_id, cluster_id, backend_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/allowip'\
            .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self._urllib_request("https://ifconfig.me", method="GET")
        if resp.status_code != 200:
            raise Exception("Fetch public IP failed!")
        body = {"cidr": "{}/32".format(resp.content.decode()), "comment": ""}
        resp = self.do_internal_request(url, method="POST",
                                    params=json.dumps(body))
        return resp

    def add_allowed_ip_sgw(self, tenant_id, project_id, cluster_id, backend_id, ip):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/allowip'\
            .format(self.internal_url, tenant_id, project_id, backend_id, cluster_id)
        body = {"cidr": "{}/32".format(ip), "comment": ""}
        resp = self.do_internal_request(url, method="POST",
                                    params=json.dumps(body))
        return resp

    def update_sync_function_sgw(self, tenant_id, project_id, cluster_id, backend_id, db_name, config):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/sync' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def add_app_role_sgw(self, tenant_id, project_id, cluster_id, backend_id, db_name, config):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/roles' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def add_user_sgw(self, tenant_id, project_id, cluster_id, backend_id, db_name, config):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/users' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def add_admin_user_sgw(self, tenant_id, project_id, cluster_id, backend_id, config):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/adminusers' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def get_sgw_links(self, tenant_id, project_id, cluster_id, backend_id, db_name):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/connect' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_sgw_info(self, tenant_id, project_id, cluster_id, backend_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_sgw_certificate(self, tenant_id, project_id, cluster_id, backend_id, db_name):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/publiccert' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_sgw_logstreaming_config(self, tenant_id, project_id, cluster_id, backend_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/logstreaming' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def enable_sgw_logstreaming(self, tenant_id, project_id, cluster_id, backend_id):
        "Enable log streaming for the sgw"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/logstreaming/enable' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def disable_sgw_logstreaming(self, tenant_id, project_id, cluster_id, backend_id):
        "Disable log streaming for the sgw"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/logstreaming/disable' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def create_or_override_log_streaming_config(self, tenant_id, project_id, cluster_id, backend_id, config):
        "Create or override log streaming config"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/logstreaming/config' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="PUT",
                                        params=json.dumps(config))
        return resp

    def delete_log_streaming_config(self, tenant_id, project_id, cluster_id, backend_id):
        "Delete log streaming config"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/logstreaming/config' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def get_sgw_logstreaming_collector_options(self, tenant_id, project_id, cluster_id, backend_id):
        "Get log streaming bit collector configuration"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/logstreaming/collector-options' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_sgw_logstreaming_collector_option_selected(self, tenant_id, project_id, cluster_id, backend_id):
        "Get log streaming bit collector option selected"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/logstreaming/collector-option-selected' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_logging_options(self, tenant_id, project_id, cluster_id, backend_id):
        "Get allowed logging options and selections"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/logging-options' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_logging_config(self, tenant_id, project_id, cluster_id, backend_id, db_name):
        "Get current logging options for the app endpoint"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/logging' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def update_logging_config(self, tenant_id, project_id, cluster_id, backend_id, db_name, config):
        "Update current logging options for the app endpoint"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/logging' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def sgw_enable_audit_logging(self, tenant_id, project_id, cluster_id, backend_id):
        "Enable audit logging for the sgw"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/audit-logging/enable' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def sgw_disable_audit_logging(self, tenant_id, project_id, cluster_id, backend_id):
        "Disable audit logging for the sgw"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/audit-logging/disable' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def sgw_get_audit_logging_state(self, tenant_id, project_id, cluster_id, backend_id):
        "Get audit logging state"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/audit-logging' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def sgw_set_audit_logging_config(self, tenant_id, project_id, cluster_id, backend_id, db_name, config):
        "Set audit logging config"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/audit-logging/{}/config' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="PUT",
                                        params=json.dumps(config))
        return resp

    def sgw_update_audit_logging_config(self, tenant_id, project_id, cluster_id, backend_id, db_name, config):
        "Update audit logging config"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/audit-logging/{}/config' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def sgw_get_audit_logging_config(self, tenant_id, project_id, cluster_id, backend_id, db_name):
        "Get audit logging config"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/audit-logging/{}/config' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, backend_id, db_name)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_node_metrics(self, tenant_id, project_id, cluster_id, metrics, step, start, end):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/metrics/{}/query_range' \
              .format(self.internal_url, tenant_id, project_id, cluster_id, metrics)
        payload = {'step':step, 'start':start, 'end':end}
        resp = self.do_internal_request(url, method="GET", params=payload)
        return resp

    def create_project(self, tenant_id, name):
        project_details = {"name": name, "tenantId": tenant_id}

        url = '{}/v2/organizations/{}/projects'.format(self.internal_url, tenant_id)
        api_response = self.do_internal_request(url, method="POST",
                                                        params=json.dumps(project_details))
        return api_response

    def delete_project(self, tenant_id, project_id):
        url = '{}/v2/organizations/{}/projects/{}'.format(self.internal_url, tenant_id,
                                                          project_id)
        api_response = self.do_internal_request(url, method="DELETE",
                                                        params='')
        return api_response

    def turn_off_cluster(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/off' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST", params='')
        return resp

    def turn_on_cluster(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/on' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        payload = {"turnOnAppService" : True}
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def enable_private_endpoint(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/privateendpoint'\
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST", params='')
        return resp

    def get_private_endpoint_status(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/privateendpoint' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def delete_private_endpoint(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/privateendpoint' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="DELETE", params='')
        return resp

    def get_gcp_private_endpoint_connection_link(self, tenant_id, project_id, cluster_id, body):
        """
            body =
            {
                "vpcId": "{customers-VPC}",
                "subnetIds": "{customers-subnet}"
            }
        """
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/privateendpoint/linkcommand' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(body))
        return resp

    def accept_gcp_private_endpoint_connection(self, tenant_id, project_id, cluster_id, body):
        """
            body =
            {
                "endpointId": "{customers-GCP-Project-Id}"
            }
        """
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/privateendpoint/connection' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(body))
        return resp

    def list_private_endpoint_connections(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/privateendpoint/connection' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def reject_private_endpoint_connection(self, tenant_id, project_id, cluster_id,
                                              gcp_project_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/privateendpoint/connection/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id, gcp_project_id)
        resp = self.do_internal_request(url, method="DELETE", params='')
        return resp

    def update_cluster_sepcs(self, tenant_id, project_id, cluster_id, specs):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/specs' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(specs))
        return resp

    def get_root_ca(self, cluster_id):
        url = '{}/v2/databases/{}/proxy/pools/default/trustedCAs' \
            .format(self.internal_url, cluster_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def toggle_cluster_deletion_protection(self, tenant_id, project_id,
                                           cluster_id, deletion_protection):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        payload = {"deletionProtection": deletion_protection}
        resp = self.do_internal_request(url, method="PATCH",
                                        params=json.dumps(payload))
        return resp

    def deploy_v2_cluster(self, tenant_id, payload):
        url = '{}/v2/organizations/{}/clusters/v2'.format(self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def list_global_feature_flags(self):
        url = '{}/v2/features/flags'.format(self.internal_url)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def list_global_feature_flags_specific(self, flag_name):
        url = '{}/v2/features/flags?flags={}'.format(self.internal_url, flag_name)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def list_tenant_feature_flags(self, tenant_id):
        url = '{}/v2/features/{}/flags'.format(self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def list_tenant_feature_flags_specific(self, tenant_id, flag_name):
        url = '{}/v2/features/{}/flags?flags={}'.format(self.internal_url, tenant_id, flag_name)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def list_global_feature_flags_internal(self):
        url = "{}/internal/support/features/flags".format(self.internal_url)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def list_global_feature_flags_internal_specific(self, flag_name):
        url = "{}/internal/support/features/flags?flags={}".format(self.internal_url, flag_name)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def create_global_feature_flag(self, flag_name, payload):
        url = "{}/internal/support/features/flags/{}".format(self.internal_url, flag_name)
        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(payload),
                                    headers=self.cbc_api_request_headers)
        return resp

    def update_global_feature_flag(self, flag_name, payload):
        url = "{}/internal/support/features/flags/{}".format(self.internal_url, flag_name)
        resp = self._urllib_request(url, method="PUT",
                                    params=json.dumps(payload),
                                    headers=self.cbc_api_request_headers)
        return resp

    def delete_global_feature_flag(self, flag_name):
        url = "{}/internal/support/features/flags/{}".format(self.internal_url, flag_name)
        resp = self._urllib_request(url, method="DELETE",
                                    headers=self.cbc_api_request_headers)
        return resp

    def list_tenant_feature_flags_internal(self, tenant_id):
        url = "{}/internal/support/features/{}/flags".format(self.internal_url, tenant_id)
        resp = self._urllib_request(url, method="GET",
                                    headers=self.cbc_api_request_headers)
        return resp

    def list_tenant_feature_flags_internal_specific(self, tenant_id, flag_name):
        url = "{}/internal/support/features/{}/flags?flags={}".format(self.internal_url, tenant_id, flag_name)
        resp = self._urllib_request(url, method="GET",
                                    headers=self.cbc_api_request_headers)
        return resp

    def create_tenant_feature_flag(self, tenant_id, flag_name, payload):
        url = "{}/internal/support/features/{}/flags/{}".format(self.internal_url, tenant_id, flag_name)
        resp = self._urllib_request(url, method="POST",
                                    params=json.dumps(payload),
                                    headers=self.cbc_api_request_headers)
        return resp

    def update_tenant_feature_flag(self, tenant_id, flag_name, payload):
        url = "{}/internal/support/features/{}/flags/{}".format(self.internal_url, tenant_id, flag_name)
        resp = self._urllib_request(url, method="PUT",
                                    params=json.dumps(payload),
                                    headers=self.cbc_api_request_headers)
        return resp

    def delete_tenant_feature_flag(self, tenant_id, flag_name):
        url = "{}/internal/support/features/{}/flags/{}".format(self.internal_url, tenant_id, flag_name)
        resp = self._urllib_request(url, method="DELETE",
                                    headers=self.cbc_api_request_headers)
        return resp

    def initialize_feature_flags_from_launchdarkly(self):
        url = "{}/internal/support/features/flags/initialize".format(self.internal_url)
        resp = self._urllib_request(url, method="POST",
                                    headers=self.cbc_api_request_headers)
        return resp

    def create_autovec_integration(self, tenant_id, payload):
        """
        Create an S3 or OpenAI integration for creating autovec workflow
        Args:
            tenant_id: ID of the organization
            payload:
                S3 integration payload:
                    {
                        "integrationType": "s3",
                        "name": "Key-New-72",
                        "data": {
                            "accessKeyId": "sample_access_key_id",
                            "secretAccessKey": "sample_secret_access_key",
                            "awsRegion": "region",
                            "bucket": "bucket",
                            "folderPath": "path"
                        }
                    }
                OpenAI integration payload:
                    {
                        "integrationType": "openAI",
                        "name": "Key-New-73",
                        "data": {
                            "key": "sample_secret_key"
                        }
                    }
        Returns:
            ID of the integration created
            Example:
            {
                "id": "06416e0e-8bdf-4273-bbf0-9ca71ba00536-Key-New-73"
            }
        """
        url = "{}/v2/organizations/{}/integrations".format(self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def get_autovec_integration(self, tenant_id, integration_id):
        """
        Get details of an autovec integration
        Args:
            tenant_id: ID of the organization
            integration_id: ID of the integration

        Returns:

        """
        url = "{}/v2/organizations/{}/integrations/{}".format(self.internal_url, tenant_id, integration_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def update_autovec_integration(self, tenant_id, integration_id, payload):
        """
        Update an autovec integration
        Args:
            tenant_id: ID of the organization
            integration_id: ID of the integration
            payload:
                S3 integration example:
                    {
                        "integrationType": "s3",
                        "name": "string"
                        "data": {
                            "accessKeyId": "sample_access_key_id_2",
                            "secretAccessKey": "sample_secret_access_key_2"
                            "aws_region": "region_2",
                            "bucket": "bucket_2",
                            "folderPath": "path_2"
                        }
                    }
                OpenAI integration example:
                    {
                       "integrationType": "openAI",
                       "name": "string"
                       "data": {
                           "key": "sample_secret_key_2"
                       }
                    }
        Returns:
            No content
        """
        url = "{}/v2/organizations/{}/integrations/{}".format(self.internal_url, tenant_id, integration_id)
        resp = self.do_internal_request(url, method="PUT", params=json.dumps(payload))
        return resp

    def list_autovec_integrations(self, tenant_id, integration_type=None, page=1, per_page=25):
        """
        Get list of all integrations in the organization
        Args:
            tenant_id: ID of the organization
            integration_type: type of integrations to list (openAI, s3)
            page: page to view
            per_page: results per page

        Returns:
            List of autovec integrations
            Example:
                {
                    "cursor": {
                        "pages": {
                            "page": 1,
                            "last": 1,
                            "perPage": 10,
                            "totalItems": 4
                        },
                        "hrefs": {}
                    },
                    "data": [
                        {
                            "data": {
                                "integrationType": "s3",
                                "id": "06416e0e-8bdf-4273-bbf0-9ca71ba00536-Key-New-59",
                                "tenantId": "06416e0e-8bdf-4273-bbf0-9ca71ba00536",
                                "name": "Key-New-59",
                                "accessKeyId": "****************y_id",
                                "secretAccessKey": "****************y_id",
                                "awsRegion": "region",
                                "bucket": "bucket",
                                "folderPath": "path",
                                "createdByUser": "aniket.kumar",
                                "createdByUserID": "8fbc47a8-8736-492f-a356-3965bd92c219",
                                "upsertedByUserID": "",
                                "createdAt": "2024-10-21T18:00:34.019456588Z",
                                "upsertedAt": "0001-01-01T00:00:00Z",
                                "modifiedByUserID": "8fbc47a8-8736-492f-a356-3965bd92c219",
                                "modifiedAt": "2024-10-21T18:00:34.019456588Z",
                                "version": 1
                            },
                            "permissions": {
                                "create": {
                                    "accessible": true
                                },
                                "read": {
                                    "accessible": true
                                },
                                "update": {
                                    "accessible": true
                                },
                                "delete": {
                                    "accessible": true
                                }
                            }
                        }
                    ]
                }
        """
        if integration_type:
            url = "{}/v2/organizations/{}/integrations?integrationType={}&page={}&perPage={}".format(self.internal_url,
                                                                                                     tenant_id, integration_type,
                                                                                                     page, per_page)
        else:
            url = "{}/v2/organizations/{}/integrations?page={}&perPage={}".format(self.internal_url,
                                                                                  tenant_id, page, per_page)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_autovec_integration(self, tenant_id, integration_id):
        """

        Args:
            tenant_id: ID of the organization
            integration_id: ID of the integration

        Returns:
            No content
        """
        url = "{}/v2/organizations/{}/integrations/{}".format(self.internal_url, tenant_id, integration_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def create_autovec_workflow(self, tenant_id, project_id, cluster_id, payload):
        """
        Create an autovec workflow
        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster
            payload:
                {
                    "dataSource": {
                        "id":"adb4fb4c-1d98-4287-ac33-230742d2cc76-s3-integration-name-25"
                    },
                    "type": "structured",
                    "schemaFields": [
                        "field1",
                        "field2"
                    ],
                    "embeddingModel": {
                        "external": {
                            "name": "open-ai-integration-26",
                            "modelName": "text-embedding-3-small",
                            "provider": "openAI",
                            "apiKey": "asfasd"
                        }
                    },
                    "cbKeyspace": {
                        "bucket": "bucket-1",
                        "scope": "_default",
                        "collection": "_default"
                    },
                    "vectorIndexName": "vector-index-name",
                    "embeddingFieldName": "embedding-field",
                    "name": "flow2"
                }

        Returns:
            ID of the workflow created
            Example:
                {
                    "id": "60621d6c-a92c-4219-95c3-eb213b0745b5"
                }
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/ai/workflows".format(self.internal_url, tenant_id,
                                                                                   project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def get_autovec_workflow(self, tenant_id, project_id, cluster_id, workflow_id):
        """
        Get workflow details
        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster
            workflow_id: ID of the workflow

        Returns:
            Workflow details
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/ai/workflows/{}".format(self.internal_url, tenant_id,
                                                                                      project_id, cluster_id, workflow_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_autovec_workflow(self, tenant_id, project_id, cluster_id, workflow_id):
        """
        Delete autovec workflow
        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster
            workflow_id: ID of the workflow

        Returns:
            No content
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/ai/workflows/{}".format(self.internal_url, tenant_id,
                                                                                      project_id, cluster_id, workflow_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def list_autovec_workflows(self, tenant_id, page=1, per_page=10):
        """
        Get list of autovec workflows
        Args:
            tenant_id: ID of the autovec workflow
            page: page to view
            per_page: results per page

        Returns:
            List of autovec workflows
        """
        url = "{}/v2/organizations/{}/ai/workflows?page={}&perPage={}".format(self.internal_url, tenant_id,
                                                                              page, per_page)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def pause_autovec_workflow(self, tenant_id, project_id, cluster_id, workflow_id):
        """
        Pause an autovec workflow
        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster
            workflow_id: ID of the workflow

        Returns:
            202 accepted on success
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/ai/workflows/{}/pause".format(self.internal_url, tenant_id,
                                                                                      project_id, cluster_id, workflow_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def resume_autovec_workflow(self, tenant_id, project_id, cluster_id, workflow_id):
        """
        Resume an autovec workflow
        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster
            workflow_id: ID of the workflow

        Returns:
            202 accepted on success
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/ai/workflows/{}/resume".format(self.internal_url,
                                                                                            tenant_id,
                                                                                            project_id, cluster_id,
                                                                                            workflow_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def list_health_reports(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/health-advisor'.format(
            self.internal_url, tenant_id, project_id, cluster_id)
        url = url + '?page=1&perPage=10&sortBy=createdAt&sortDirection=desc'
        resp = self.do_internal_request(url, method="GET")
        return resp

    def list_health_reports_check(self, tenant_id, project_id, cluster_id, report_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/health-advisor/{}'.format(
            self.internal_url, tenant_id, project_id, cluster_id, report_id)
        url = url + '?page=1&perPage=10&sortBy=severity&sortDirection=desc&category=data&severity=good'
        resp = self.do_internal_request(url, method="GET")
        return resp

    def generate_health_report(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/health-advisor'.format(
            self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def get_health_report_generation_progress(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/health-advisor/progress'.format(
            self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_health_advisor_settings(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/health-advisor/settings'.format(
            self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_health_report_overall_stats(self, tenant_id, project_id, cluster_id, report_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/health-advisor/{}/stats'.format(
            self.internal_url, tenant_id, project_id, cluster_id, report_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def update_health_advisor_settings(self, tenant_id, project_id, cluster_id, payload=None):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/health-advisor/settings'.format(
            self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="PATCH", params=json.loads(payload))
        return resp

    def get_info_health_report(self, tenant_id, project_id, cluster_id, report_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/health-advisor/{}/info'.format(
                self.internal_url, tenant_id, project_id, cluster_id, report_id)
        url = url + '?category=data'
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_pdf_health_report(self, tenant_id, project_id, cluster_id, report_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/health-advisor/{}/pdf'.format(
                self.internal_url, tenant_id, project_id, cluster_id, report_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def upload_cert_mtls(self, tenant_id, project_id, cluster_id, payload):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/mtls'.format(
            self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def upload_mtls_settings(self, tenant_id, project_id, cluster_id, payload):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/mtls'.format(
            self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="PUT", params=json.dumps(payload))
        return resp

    def get_mtls_details(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/mtls'.format(
            self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def deploy_model(self, tenant_id, payload):

        """
        Deploys a LLM or embedding model
        tenant_id: ID of the organization
        payload:
            Embedding:
            {
              "name": "my-embedding-model",
              "modelCatalogId": "29455162-6925-4b55-a726-9b7cc12c9f4a",
              "config": {
                "provider": "hostedAWS",
                "region": "us-east-1",
                "multiAZ": true,
                "compute": {
                  "instanceType": "g6.xlarge",
                  "instanceCount": 2
                }
              },
              "parameters": {
                "tuning": {
                  "quantization": "full-precision",
                  "optimization": "throughput",
                  "dimensions": 4096
                }
              }
            }
            LLM:
            {
              "name": "my-text-generation-model",
              "modelCatalogId": "5676ca67-c6d8-4db4-9064-66cede4c2f8b",
              "config": {
                "provider": "hostedAWS",
                "region": "us-east-1",
                "multiAZ": true,
                "compute": {
                  "instanceType": "g6.xlarge",
                  "instanceCount": 2
                }
              },
              "parameters": {
                "tuning": {
                  "quantization": "full-precision",
                  "optimization": "throughput",
                  "dimensions": 4096
                }
              }
            }

        Returns:
            ID of the model deployed
            Example:
                {
                    "id": "60621d6c-a92c-4219-95c3-eb213b0745b5"
                }
        """
        url = "{}/v2/organizations/{}/languagemodels".format(self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def delete_model(self, tenant_id, model_id):
        """
        Deletes a model
        Args:
            tenant_id: ID of the organization
            model_id: ID of the model

        Returns:
            202 Language model was successfully queued for deletion
        """
        url = "{}/v2/organizations/{}/languagemodels/{}".format(self.internal_url, tenant_id,
                                                                                        model_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def get_model_details(self, tenant_id, model_id):
        """
        Get details of a model
        Args:
            tenant_id: ID of the organization
            model_id: ID of the model

        Returns:
            200 on success and model details:
        """
        url = "{}/v2/organizations/{}/languagemodels/{}".format(self.internal_url, tenant_id,
                                                                                        model_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def create_model_api_key(self, tenant_id, model_id, payload):
        """
        Create an API key for a deployed model
        Args:
            tenant_id: ID of the organization
            model_id: ID of the model
            payload: {
                        "name": "TestAPIKey",
                        "description": "Test API Key",
                        "expiryDuration": 180,
                        "createdByUserID": "8fbc47a8-8736-492f-a356-3965bd92c219",
                        "accessPolicy": {
                          "allowedModels": [
                            "5ca127fe-49da-4a6a-aef9-08393b97643f"
                          ],
                          "allowedIPs": [
                            "0.0.0.0/0"
                          ]
                        }
                      }

        Returns:
            200 on success and API key details:
            {
                "id": "api-key-id",
                "name": "my-model-api-key",
                "apiKey": "api-key-value",
                "description": "Test API Key",
                "expiryDuration": 180,
                "expiry": "2024-10-21T18:00:34.019456588Z",
                "accessPolicy": {
                    # TODO
                }
            }
        """
        url = "{}/v2/organizations/{}/languageModelAPIKeys".format(self.internal_url, tenant_id, model_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def delete_model_api_key(self, tenant_id, api_key_id):
        """
        Delete an API key for a deployed model
        Args:
            tenant_id: ID of the organization
            api_key_id: ID of the
        Returns:
            202 on successful delete
        """
        url = "{}/v2/organizations/{}/languageModelAPIKeys/{}".format(self.internal_url, tenant_id,
                                                                                       api_key_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def update_model_api_key(self, tenant_id, api_key_id, payload):
        url = "{}/v2/organizations/{}/languageModelAPIKeys/{}".format(
            self.internal_url, tenant_id, api_key_id
        )
        resp = self.do_internal_request(url, method="PUT", params=json.dumps(payload))
        return resp

    def list_models(self, tenant_id, page=1, per_page=10):
        """
        List all the deployed models in an organization
        Args:
            tenant_id: ID of the organization
            page: page to view
            per_page: results per page

        Returns:
            200 on success
            Lists all models deployed
        """
        url = "{}/v2/organizations/{}/languagemodels?page={}&perPage={}".format(self.internal_url, tenant_id,
                                                                                page, per_page)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def list_activity_log_events(self, tenant_id, project_id, cluster_id, start, end):
        url = "{}/v2/organizations/{}/events?page=1&perPage=25&project={}".format(self.internal_url, tenant_id, project_id)
        url = "{}&severity=critical,warning&tag=alert&start={}&end={}&cluster={}&sortBy=severity&sortDirection=asc".format(
            url, start, end, cluster_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_index_status(self, cluster_id):
        url = "{}/v2/databases/{}/proxy/indexStatus".format(self.internal_url, cluster_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def list_indexes(self, tenant_id, project_id, cluster_id, **kwargs):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/ui_monitoring/index_table".format(
            self.internal_url, tenant_id, project_id, cluster_id)
        query_params = "&".join("{}={}".format(k, v) for k, v in kwargs.items())
        url = "{}?{}".format(url, query_params)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_query_workload_stats(self, tenant_id, project_id, cluster_id, payload):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/query-workload-stats".format(
            self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def get_query_workload_filters(self, tenant_id, project_id, cluster_id, **kwargs):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/query-workload-filters".format(
            self.internal_url, tenant_id, project_id, cluster_id)
        query_params = "&".join("{}={}".format(k, v) for k, v in kwargs.items())
        url = "{}?{}".format(url, query_params)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_fts_index_status(self, cluster_id):
        url = "{}/v2/databases/{}/proxy/fts/api/indexStatus".format(self.internal_url, cluster_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_tenant_info(self, tenant_id):
        url = "{}/v2/organizations/{}".format(self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def enable_fusion(self, cluster_id, sync_threshold = 102400):
        url = "{}/internal/support/clusters/{}/fusion/enable".format(self.internal_url, cluster_id)
        data = {
            "logStoreURI": "s3://cbc-storage-{}".format(cluster_id[-6:]),
            "enableSyncThresholdMB": sync_threshold
        }
        resp = self._urllib_request(url, method="POST", params=json.dumps(data), headers=self.cbc_api_request_headers)
        return resp

    def disable_fusion(self, cluster_id):
        url = "{}/internal/support/clusters/{}/fusion/disable".format(self.internal_url, cluster_id)
        resp = self._urllib_request(url, method="POST", headers=self.cbc_api_request_headers)
        return resp

    def get_fusion_status(self, cluster_id):
        url = "{}/internal/support/clusters/{}/fusion/status".format(self.internal_url, cluster_id)
        resp = self._urllib_request(url, method="GET", headers=self.cbc_api_request_headers)
        return resp

    def get_mtls_configuration(self, tenant_id, project_id, cluster_id):
        """
        Get the mTLS configuration for the cluster.

        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster

        Returns:
            200: Successfully retrieved mTLS configuration for the cluster.
            Example:
            {
                "state": "enable",
                "prefixes": [
                    {
                    "path": "subject.cn",
                    "prefix": "www.",
                    "delimiter": "."
                    }
                ]
            }
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/mtls/config".format(
            self.internal_url, tenant_id, project_id, cluster_id
        )
        resp = self.do_internal_request(url, method="GET")
        return resp

    def update_mtls_configuration(self, tenant_id, project_id, cluster_id, mTLS_config):
        """
        Update the mTLS configuration on the cluster.

        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster
            mTLS_config: The mTLS configuration data to update
                Example:
                {
                    "state": "enable",
                    "prefixes": [
                        {
                        "path": "subject.cn",
                        "prefix": "www.",
                        "delimiter": "."
                        }
                    ]
                }

        Returns:
            204: Successfully updated the mTLS configuration for the cluster
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/mtls/config".format(
            self.internal_url, tenant_id, project_id, cluster_id
        )
        resp = self.do_internal_request(url, method="PUT", params=json.dumps(mTLS_config))
        return resp

    def add_mtls_certificate(self, tenant_id, project_id, cluster_id, certificate_data):
        """
        Add a new mTLS certificate to the cluster.

        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster
            certificate_data: The certificate data to add
                Example:
                {
                    "name": "MyCertificate",
                    "certificate": "***",
                    "intermediates": "***"
                }

        Returns:
            201: Successfully added a new certificate to the cluster
            Example:
            {
                "id": "ffffffff-aaaa-1414-eeee-000000000000"
            }
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/mtls/certificates".format(
            self.internal_url, tenant_id, project_id, cluster_id
        )
        resp = self.do_internal_request(url, method="POST", params=json.dumps(certificate_data))
        return resp

    def list_mtls_certificates(self, tenant_id, project_id, cluster_id, page=None, per_page=None,
                              sort_by=None, sort_direction=None):
        """
        List the current mTLS certificates on the cluster.

        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster
            page: Page number for pagination
            per_page: Number of results per page
            sort_by: Field to sort by
            sort_direction: Sort direction (asc/desc)

        Returns:
            200: Successfully listed mTLS certificates
            Example:
            {
                "data": [
                    {
                    "id": "ffffffff-aaaa-1414-eeee-000000000000",
                    "status": "pending",
                    "certificateData": {
                        "name": "my-cert",
                        "certificate": "***",
                        "intermediates": "***"
                    },
                    "intendedState": {
                        "name": "my-cert",
                        "certificate": "***",
                        "intermediates": "***"
                    },
                    "audit": {
                        "createdBy": "ffffffff-aaaa-1414-eeee-000000000000",
                        "createdAt": "2021-09-01T12:34:56Z",
                        "modifiedBy": "ffffffff-aaaa-1414-eeee-000000000000",
                        "modifiedAt": "2021-09-01T12:34:56Z",
                        "version": 1
                    }
                    }
                ],
                "cursor": {
                    "pages": {
                        "page": 2,
                        "next": 3,
                        "previous": 1,
                        "last": 10,
                        "perPage": 10,
                        "totalItems": 10
                    },
                    "hrefs": {
                        "first": "https://cloud.couchbase.com/v4/users?page=1&perPage=10",
                        "last": "https://cloud.couchbase.com/v4/users?page=1&perPage=10",
                        "previous": "https://cloud.couchbase.com/v4/users?page=1&perPage=10",
                        "next": "https://cloud.couchbase.com/v4/users?page=1&perPage=10"
                    }
                }
            }
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/mtls/certificates".format(
            self.internal_url, tenant_id, project_id, cluster_id
        )

        # Build query parameters
        params = {}
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['perPage'] = per_page
        if sort_by is not None:
            params['sortBy'] = sort_by
        if sort_direction is not None:
            params['sortDirection'] = sort_direction

        if params:
            query_string = '&'.join(["{0}={1}".format(k, v) for k, v in params.items()])
            url = "{0}?{1}".format(url, query_string)

        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_mtls_certificate(self, tenant_id, project_id, cluster_id, cert_id):
        """
        Get a specific mTLS certificate by ID.

        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster
            cert_id: ID of the certificate to retrieve

        Returns:
            200: Successfully returned a self-signed certificate
            Example:
            {
                "id": "ffffffff-aaaa-1414-eeee-000000000000",
                "status": "pending",
                "certificateData": {
                    "name": "my-cert",
                    "certificate": "***",
                    "intermediates": "***"
                },
                "intendedState": {
                    "name": "my-cert",
                    "certificate": "***",
                    "intermediates": "***"
                },
                "audit": {
                    "createdBy": "ffffffff-aaaa-1414-eeee-000000000000",
                    "createdAt": "2021-09-01T12:34:56Z",
                    "modifiedBy": "ffffffff-aaaa-1414-eeee-000000000000",
                    "modifiedAt": "2021-09-01T12:34:56Z",
                    "version": 1
                }
            }
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/mtls/certificates/{}".format(
            self.internal_url, tenant_id, project_id, cluster_id, cert_id
        )
        resp = self.do_internal_request(url, method="GET")
        return resp

    def update_mtls_certificate(self, tenant_id, project_id, cluster_id, cert_id, certificate_data):
        """
        Update an existing mTLS certificate.

        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster
            cert_id: ID of the certificate to update
            certificate_data: The updated certificate data
                Example:
                {
                    "name": "my-cert",
                    "certificate": "***",
                    "intermediates": "***"
                }

        Returns:
            202: Successfully submitted request to update the certificate
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/mtls/certificates/{}".format(
            self.internal_url, tenant_id, project_id, cluster_id, cert_id
        )
        resp = self.do_internal_request(url, method="PUT", params=json.dumps(certificate_data))
        return resp

    def delete_mtls_certificate(self, tenant_id, project_id, cluster_id, cert_id):
        """
        Delete an mTLS certificate from the cluster.

        Args:
            tenant_id: ID of the organization
            project_id: ID of the project
            cluster_id: ID of the cluster
            cert_id: ID of the certificate to delete

        Returns:
            202: Successfully submitted request to delete the certificate
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/mtls/certificates/{}".format(
            self.internal_url, tenant_id, project_id, cluster_id, cert_id
        )
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def start_ondemand_cluster_backup(self, tenant_id, project_id, cluster_id, retention_hours):
        """Start a new backup snapshot."""
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/cloudsnapshotbackups".format(
            self.internal_url,
            tenant_id,
            project_id,
            cluster_id,
        )
        payload = {"retention": retention_hours}
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def restore_cluster_backup(self, tenant_id, project_id, cluster_id, backup_id):
        """Restore the cluster using an existing backup snapshot."""
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/cloudsnapshotbackups/{}/restore".format(
            self.internal_url, tenant_id, project_id, cluster_id, backup_id
        )
        resp = self.do_internal_request(url, method="POST")
        return resp

    def list_cluster_backups(self, tenant_id, project_id, cluster_id, page, per_page):
        """List all cluster level backups on the specified cluster."""
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/cloudsnapshotbackups?page={}&perPage={}".format(
            self.internal_url, tenant_id, project_id, cluster_id, page, per_page
        )
        resp = self.do_internal_request(url, method="GET")
        return resp

    def list_cluster_restores(self, tenant_id, project_id, cluster_id, page, per_page):
        """List all cluster level restores that have taken place on a specified cluster."""
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/cloudsnapshotbackups/restores?page={}&perPage={}".format(
            self.internal_url, tenant_id, project_id, cluster_id, page, per_page
        )
        resp = self.do_internal_request(url, method="GET")
        return resp
