import json

from ..common.CapellaAPI import CommonCapellaAPI


class CapellaAPI(CommonCapellaAPI):
    """
        Class to support Capella Columnar endpoints and operations.

        Parameters:
            url (str): The base URL of the Columnar API.
            secret (str): The secret key for authentication.
            access (str): The access key for authentication.
            user (str): The username for authentication.
            pwd (str): The password for authentication.
            TOKEN_FOR_INTERNAL_SUPPORT (str, optional): An optional token
            for internal support.
    """

    def set_trigger_time_for_onoff(self, time, instance_ids):
        """
        Use to trigger schedule on/off by providing instance a false time to compare to
        Parameters:
            time (str): Time in UTC
            instance_ids (list): List to instance ids of the instances
        """
        url = "{}/internal/support/onoff/queue-schedule-operations/columnar".format(
            self.internal_url
        )
        body = {
            "scheduledTimeInUTC": time,
            "clusters": instance_ids
        }
        resp = self._urllib_request(url, "POST", params=json.dumps(body),
                                    headers=self.cbc_api_request_headers)
        return resp

    def set_trigger_time_for_scheduled_backup(self, time, instances, all_instances=False):
        """
        Use to set a false time to the instance to start schdeuled backup
        Parameters:
            time (str): Time in UTC
            instances (list) : All the instance to relay false time to
            all_instances (bool): To enable false time for all the instances in an environment
        """
        body = {
            "time": time,
            "instances": instances,
            "all_instances": all_instances
        }
        url = "{}/internal/support/columnar/recovery/scheduling".format(self.internal_url)
        resp = self._urllib_request(url, "POST", params=json.dumps(body),
                                    headers=self.cbc_api_request_headers)
        return resp

    def set_trigger_time_for_backup_retention(self, time, instances, all_instances=False):
        """
        Provide false time to check for retention deletion
        Parameters:
            time (str): Time in UTC
            instances (list): Instance ids of all the instance to apply to
            all_instances (bool): To enable false time for all the instances in an environment
        """
        body = {
            "retentionTimeInUTC": time,
            "instanceIds": instances,
            "allInstances": all_instances
        }
        url = "{}/internal/support/columnar/recovery/retention".format(self.internal_url)
        resp = self._urllib_request(url, "POST", params=json.dumps(body),
                                    headers=self.cbc_api_request_headers)
        return resp

    def get_columnar_services(self):
        """
            Retrieve a list of all Columnar services.
        """
        url = "{}/internal/support/serverlessanalytics/service".format(
            self.internal_url)
        resp = self.do_internal_request(url, "GET")
        return resp

    def get_specific_columnar_service(self, serviceId):
        """
            Retrieve a specific Columnar service.

            Parameters:
                serviceId : ID of the service whose service needs to be retrieved
        """
        url = '{}/internal/support/serverlessanalytics/service/{}'.format(
            self.internal_url, serviceId)
        resp = self.do_internal_request(url, "GET")
        return resp

    def get_deployment_options(self, tenant_id, provider="aws", region=None):
        """
        Get deployment options for a Columnar instance.

        Returns valid options for deployment parameters, including but not
        limited to suggested CIDR, instance types, support packages and node
        count.

        Required Parameters:
            `tenant_id` (str): The ID of the tenant to get options for.
        Optional Parameters:
            `provider` (str): The provider or cloud platform (e.g., AWS, GCP) to get options for.
            `region` (str): The region or location to get options for (provider is required if this
                          is specified).
        """
        url = "{}/v2/organizations/{}/instance/deployment-options/v2".format(
            self.internal_url, tenant_id
        )
        if provider:
            url += "?provider={}".format(provider)
            if region:
                url += "&region={}".format(region)
        resp = self.do_internal_request(url, "GET")
        return resp

    def create_columnar_instance(self, tenant_id, project_id, config):
        """
            Create a new Columnar instance within a specified project.

            Parameters:
                tenant_id (str): The ID of the tenant under which the instance will be created.
                project_id (str): The ID of the project where the instance will be added.
                config (dict): This contains the deployment parameters needed. Sample Below:
                {'availabilityZone': 'single',
                 'description': 'Have fun with Columnar',
                 'instanceTypes': {'memory': '16GB', 'vcpus': '4vCPUs'},
                 'name': 'do-not-delete_Columnar ;-)',
                 'nodes': 2,
                 'overRide': {'image': 'Choose your own',
                              'token': 'secret'},
                 'provider': 'aws',
                 'region': 'us-east-1',
                 'package': {'key': 'Developer Pro', 'timezone': 'PT'}}
        """
        url = "{}/v2/organizations/{}/projects/{}/instance".format(
            self.internal_url, tenant_id, project_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def get_columnar_instances(self, tenant_id, project_id, page=1,
                               perPage=100):
        """
            Retrieve a list of Columnar instances within a specified project.

            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project for which instances will be retrieved.
                page (int): The page number to retrieve. Default is 1.
                perPage (int): Number of results to return per page. Default is 100.

        """
        url = "{}/v2/organizations/{}/projects/{}/instance?page={}&perPage=" \
              "{}".format(
            self.internal_url, tenant_id, project_id, page, perPage)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_specific_columnar_instance(self, tenant_id, project_id, instance_id):
        """
            Retrieve information about a specific Columnar instance within a project.

            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance to retrieve information for.
        """
        url = "{}/v2/organizations/{}/projects/{}/instance/{}".format(
            self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_columnar_nodes(self, instance_id):
        """
            Retrieve information about the nodes of a specific Columnar instance.

            Parameters:
                instance_id (str): The ID of the Columnar instance to delete.
        """
        url = "{}/internal/support/instances/{}/nodes".format(self.internal_url, instance_id)
        resp = self._urllib_request(url, "GET", headers=self.cbc_api_request_headers)
        return resp

    def delete_columnar_instance(self, tenant_id, project_id, instance_id):
        """
            Delete a specific Columnar instance within a project.

            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance to delete.
        """
        url = "{}/v2/organizations/{}/projects/{}/instance/{}".format(
            self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def update_columnar_instance(self, tenant_id, project_id, instance_id, name, description, nodes, **kwargs):
        """
            Modify a specific Columnar instance within a project.

            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance to delete.
                name (str): The name of the Columnar instance.
                description (str): A description for the Columnar instance.
                nodes (int): The number of nodes to allocate for the instance.
                **kwargs: Additional keyword arguments to pass to the API request.
        """
        url = "{}/v2/organizations/{}/projects/{}/instance/{}".format(
            self.internal_url, tenant_id, project_id, instance_id)
        body = {
            "name": name,
            "description": description,
            "nodes": nodes
        }
        for key, value in kwargs.items():
            body[key] = value

        resp = self.do_internal_request(url, method="PATCH", params=json.dumps(body))
        return resp

    def create_columnar_role(self, tenant_id, project_id, instance_id,
                             payload):
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/roles".format(
            self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(payload))
        return resp

    def delete_columnar_role(self, tenant_id, project_id, instance_id,
                             role_id):
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/roles/{}".format(
            self.internal_url, tenant_id, project_id, instance_id, role_id)
        resp = self.do_internal_request(
            url, method="DELETE")
        return resp

    def create_api_keys(self, tenant_id, project_id, instance_id,
                        payload=None):
        """
            Create a Columnar apikey

            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance to create keys for.
        """
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/apikeys".format(
            self.internal_url, tenant_id, project_id, instance_id)
        if payload:
            resp = self.do_internal_request(url, method="POST",
                                            params=json.dumps(payload))
        else:
            resp = self.do_internal_request(url, method="POST")
        return resp

    def get_api_keys(self, tenant_id, project_id, instance_id, page=1,
                     perPage=100):
        """
            Create a Columnar apikey

            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance to get keys for.
        """
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/apikeys?" \
              "page={}&perPage={}".format(
            self.internal_url, tenant_id, project_id, instance_id,
            page, perPage)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_api_keys(self, tenant_id, project_id, instance_id, api_key):
        """
            Revoke a Columnar apikey
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance to create keys for.
                api_key (str): api key id.
        """
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/apikeys/{}".format(
            self.internal_url, tenant_id, project_id, instance_id, api_key)
        resp = self.do_internal_request(
            url, method="DELETE")
        return resp

    def update_api_key(self, tenant_id, project_id, instance_id, api_key_id, payload=None):
        """
            Update a Columnar apikey
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance to create keys for.
                api_key_id (str): api key id.
                payload: The roles and privileges to be assigned
        """
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/apikeys/{}".format(
            self.internal_url, tenant_id, project_id, instance_id, api_key_id)
        resp = self.do_internal_request(url, method="PATCH",
                                        params=json.dumps(payload))
        return resp

    def allow_ip(self, tenant_id, project_id, instance_id, cidr, comment="", **kwargs):
        """
            Add a CIDR to the columnar CIDR allowed list.
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
                cidr (str): The CIDR that is to be added to the allowed CIDR list
                comment (str): Comment for the CIDR that is to be added
                **kwargs: Additional keyword arguments to pass to the API request.

        """
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/allowlists".format(
            self.internal_url, tenant_id, project_id, instance_id)
        body = {"cidr": cidr, "comment": comment}
        for key, value in kwargs.items():
            body[key] = value

        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(body))
        return resp

    def turn_off_instance(self, tenant_id, project_id, instance_id):
        """
            Turn off a columnar instance
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance to create keys for.
        """
        url = '{}/v2/organizations/{}/projects/{}/instance/{}/off' \
            .format(self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="POST", params='')
        return resp

    def turn_on_instance(self, tenant_id, project_id, instance_id):
        """
            Turn on a columnar instance
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
        """
        url = '{}/v2/organizations/{}/projects/{}/instance/{}/on' \
            .format(self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="POST", params='')
        return resp

    def execute_statement(self, tenant_id, project_id, instance_id, statement,
                          client_context_id=None, analytics_timeout=120,
                          time_out_unit="s"):

        url = "{}/v2/organizations/{}/projects/{}/instance/{}/proxy/query/service".format(
            self.internal_url, tenant_id, project_id, instance_id)

        params = {'statement': statement, 'client_context_id': client_context_id,
                  'timeout': str(analytics_timeout) + time_out_unit}

        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(params))
        return resp

    def schedule_on_off(self, tenant_id, project_id, instance_id, days, timezone="UTC", **kwargs):
        """
            Schedules the columnar instance on and off
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
                timezone (str): The timezone to follow for schedule times
                days (list of dict): Contains states, day and time for on off
        """
        body = {
            "timezone": timezone,
            "days": days,
        }
        for k, v in kwargs.items():
            body[k] = v
        url = '{}/v2/organizations/{}/projects/{}/instance/{}/schedules/onoff' \
            .format(self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="PUT", params=json.dumps(body))
        return resp

    def create_backup(self, tenant_id, project_id, instance_id, retention=None):
        """
            Creates backup for columnar instance
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
                retention(int): Optional, Backup retention time in hours from 24-to-720
        """
        payload = {}
        if retention:
            payload = {"retention": retention}
        url = '{}/v2/organizations/{}/projects/{}/instance/{}/snapshotbackups'.format(
            self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def list_backups(self, tenant_id, project_id, instance_id, page=1, perPage=100):
        """
            List all backups for a columnar instance
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
                page (int): The page number.
                perPage (int): Item per page.
        """
        url = '{}/v2/organizations/{}/projects/{}/instance/{}/snapshotbackups?page={}&perPage={}' \
            .format(self.internal_url, tenant_id, project_id, instance_id, page, perPage)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_backup(self, tenant_id, project_id, instance_id, backup_id):
        """
            Delete a backup belonging to the columnar instance
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
                backup_id (str): The ID of the backup that is to be deleted
        """
        url = '{}/v2/organizations/{}/projects/{}/instance/{}/snapshotbackups/{}' \
            .format(self.internal_url, tenant_id, project_id, instance_id, backup_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def edit_backup_retention(self, tenant_id, project_id, instance_id, backup_id, retention):
        """
            Edit a backup retention
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
                backup_id (str): The ID of the backup that is to be deleted
                retention (int): Backup retention time in hours from 24-to-720
        """
        payload = {"retention": retention}
        url = '{}/v2/organizations/{}/projects/{}/instance/{}/snapshotbackups/{}' \
            .format(self.internal_url, tenant_id, project_id, instance_id, backup_id)
        resp = self.do_internal_request(url, method="PUT", params=json.dumps(payload))
        return resp

    def backup_restore_billing_rate(self, tenant_id, project_id, instance_id):
        """
            Get billing rate for backup and restore
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
        """
        url = '{}/v2/organizations/{}/projects/{}/instance/{}/snapshotbackups/cost' \
            .format(self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def create_restore(self, tenant_id, project_id, instance_id, backup_id):
        """
            Create restore of a backup
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
                backup_id (str): The ID of the backup that is to be restored
        """
        url = '{}/v2/organizations/{}/projects/{}/instance/{}/snapshotbackups/{}/restore' \
            .format(self.internal_url, tenant_id, project_id, instance_id, backup_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def list_restores(self, tenant_id, project_id, instance_id, page=1, perPage=100):
        """
            List all restores for a columnar instance
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
        """
        url = (
            "{}/v2/organizations/{}/projects/{}/instance/{}/"
            "snapshotbackups/restores?page={}&perPage={}"
        ).format(self.internal_url, tenant_id, project_id, instance_id, page, perPage)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_restore_progress(self, tenant_id, project_id, instance_id, restore_id):
        """
            Get the progress of a restore on a columnar instance
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
                restore_id (str): The ID of the restore
        """
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/snapshotbackups/restores/{}/progress" \
            .format(self.internal_url, tenant_id, project_id, instance_id, restore_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def schedule_backup_create_update(self, tenant_id, project_id, instance_id, interval, retention, start_time):
        """
            Create/update (upsert) backup schedule of a columnar instance
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
                interval (int): hours
                retention (int): hours from 24-to-720
                start_time (timestamp-in-RFC3339): Optional, Time to start backup
        """
        payload = {
            "interval": interval,
            "retention": retention,
        }
        if start_time:
            payload["startTime"] = start_time

        url = '{}/v2/organizations/{}/projects/{}/instance/{}/snapshotbackupschedule' \
            .format(self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="PUT", params=json.dumps(payload))
        return resp

    def get_backup_schedules(self, tenant_id, project_id, instance_id):
        """
            Get all schedules available for the columnar instance
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
        """
        url = '{}/v2/organizations/{}/projects/{}/instance/{}/snapshotbackupschedule' \
            .format(self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_schedule_backup(self, tenant_id, project_id, instance_id):
        """
            Delete all schedule backups for the columnar instance
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
        """
        url = '{}/v2/organizations/{}/projects/{}/instance/{}/snapshotbackupschedule' \
            .format(self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def create_link(self, tenant_id, project_id, instance_id, link_name, cluster_id):
        """
            Create a remote link to a Capella Provisioned cluster.
            Parameters:
                tenant_id (str): The ID of the tenant associated with the project.
                project_id (str): The ID of the project where the instance is located.
                instance_id (str): The ID of the Columnar instance.
                link_name (str): The name for the link.
                cluster_id (str): The ID of the Capella Provisioned cluster to link to.

            Note: This creates a background job to create the link, as link creation involves
            multiple steps including setting up VPC peering between the two Capella clusters.
        """
        payload = {
            "linkName": link_name,
            "provisionedCluster": {"clusterId": cluster_id},
        }
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/links".format(
            self.internal_url, tenant_id, project_id, instance_id)
        resp = self.do_internal_request(url, method="POST", params=json.dumps(payload))
        return resp

    def create_analytics_admin_user(self, instance_id):
        """
        Note - This will not work on production environment.
        Will create couchbase-cloud-qe with analytics_admin permission.
        Parameters:
            instance_id (str): Columnar instance ID
        """
        url = "{0}/internal/support/instances/{1}/qe-account".format(
            self.internal_url, instance_id
        )
        resp = self._urllib_request(url, "POST",
                                    headers=self.cbc_api_request_headers)
        return resp

    def delete_analytics_admin_user(self, instance_id):
        """
        Note - This will not work on production environment.
        Will delete couchbase-cloud-qe with analytics_admin permission.
        Parameters:
            instance_id (str): Columnar instance ID
        """
        url = "{0}/internal/support/instances/{1}/qe-account".format(
            self.internal_url, instance_id
        )
        resp = self._urllib_request(url, "DELETE",
                                    headers=self.cbc_api_request_headers)
        return resp

    def list_all_roles(self, tenant_id, project_id, instance_id, page=1, perPage=100):
        """
        List all the rbac roles in the columnar instance
        Parameters:
            tenant_id (str): The ID of the tenant associated with the project.
            project_id (str): The ID of the project where the instance is located.
            instance_id (str): The ID of the Columnar instance.
            page (int): The page number.
            perPage (int): Item per page.

        """
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/roles?page={}&perPage=" \
              "{}".format(
            self.internal_url, tenant_id, project_id, instance_id, page, perPage)
        resp = self.do_internal_request(url, method="GET")
        return resp

    """
    Method fetches all the maintenance jobs for a columnar cluster.
    :param page <int> Page number to be fetched.
    :param per_page <int> Number of jobs per page.
    """
    def get_maintenance_jobs(self, tenant_id, project_id, instance_id,
                             page=1, per_page=100):
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/maintenances".format(
            self.internal_url, tenant_id, project_id, instance_id)
        payload = {
            "page": page,
            "perPage": per_page
        }
        resp = self.do_internal_request(
            url, method="GET", params=json.dumps(payload))
        return resp

    """
    Method fetches info for a maintenance job for a columnar cluster.
    :param job_id <int> Id of the maintenance job.
    """
    def get_maintenance_job_status(self, tenant_id, project_id, instance_id, job_id):
        url = "{}/v2/organizations/{}/projects/{}/instance/{}/maintenances/" \
              "{}".format(
            self.internal_url, tenant_id, project_id, instance_id, job_id)
        resp = self.do_internal_request(url, method="GET")
        return resp
