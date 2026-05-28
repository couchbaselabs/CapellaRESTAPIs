# -*- coding: utf-8 -*-
# Generic/Built-in

import logging
from ..lib.APIRequests import APIRequests


class ColumnarAPIs(APIRequests):

    def __init__(self, url, secret, access, bearer_token):
        super(ColumnarAPIs, self).__init__(url, secret, access, bearer_token)
        self.columnar_ops_API_log = logging.getLogger(__name__)
        self.analytics_clusters_endpoint = "/v4/organizations/{}/projects/{}/analyticsClusters"
        self.org_level_analytics_clusters_endpoint = "/v4/organizations/{}/analyticsClusters"
        self.on_off_endpoint = self.analytics_clusters_endpoint + "/{}/activationState"
        self.schedule_on_off_endpoint = self.analytics_clusters_endpoint + "/{}/onOffSchedule"
        self.cloud_snapshot_backups_endpoint = self.analytics_clusters_endpoint + "/{}/cloudSnapshotBackups"
        self.cloud_snapshot_backup_schedule_endpoint = self.analytics_clusters_endpoint + "/{}/cloudSnapshotBackupSchedule"

    def turn_analytics_cluster_off(
            self,
            organizationId,
            projectId,
            instanceId,
            headers=None,
            **kwargs):
        """
        Switches the columnar instance state to OFF.

        Args:
            organizationId: The tenantID in which the instance is present. (UUID)
            projectId: The ID of the Project in which the instance is present. (UUID)
            instanceId: The ID of the Instance. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Turning off the columnar instance {}, inside project {}, inside "
            "tenant {}".format(instanceId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del(self.on_off_endpoint.format(
            organizationId, projectId, instanceId), params, headers)
        return resp

    def turn_analytics_cluster_on(
            self,
            organizationId,
            projectId,
            instanceId,
            headers=None,
            **kwargs):
        """
        Switches the columnar instance state to ON.

        Args:
            organizationId: The tenantID in which the instance is present. (UUID)
            projectId: The ID of the Project in which the instance is present. (UUID)
            instanceId: The ID of the Instance. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Turning on the columnar instance {}, inside project {}, inside "
            "tenant {}".format(instanceId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_post(self.on_off_endpoint.format(
            organizationId, projectId, instanceId), params, headers)
        return resp

    def create_analytics_cluster(
            self,
            organizationId,
            projectId,
            name,
            cloudProvider,
            compute,
            region,
            nodes,
            support,
            availability,
            description="",
            headers=None,
            **kwargs):
        """
        Creates a columnar instance inside a Project

        Args:
            organizationId: The tenantID in which the instance is present. (UUID)
            projectId: The ID of the Project in which the instance is present. (UUID)
            name: Name of the instance. (str)
            cloudProvider: Keyword. (str)
            compute: The computational params of the instance. (obj)
                cpu: Number vCPUs allocated to the instance. (int)
                ram: RAM (in GBs) allocated to the instance. (int)
            region: keyword, based on cloudProvider. (str)
            nodes: Number of nodes to be allotted to the instance. (int)
            support: The Plan and Timezone details for the instance. (dict)
                plan: Developer / Enterprise (string)
                timezone: one of the AWS timezones (string)
            availability: The availability zone configuration. Must be one of 'single' or 'multi. (str)
            description: Description of the columnar instance. (str)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Creating an columnar instance inside project {}, inside tenant "
            "{}.".format(projectId, organizationId))

        params = {
            "name": name,
            "cloudProvider": cloudProvider,
            "compute": compute,
            "region": region,
            "nodes": nodes,
            "support": support,
            "availability": availability
        }
        if description is not None:
            params["description"] = description
        for k, v in kwargs:
            params[k] = v

        resp = self.api_post(self.analytics_clusters_endpoint.format(
            organizationId, projectId), params, headers)
        return resp

    def delete_analytics_cluster(
            self,
            organizationId,
            projectId,
            instanceId,
            headers=None,
            **kwargs):
        """
        Deletes the instance by the given ID.

        Args:
            organizationId: The tenantID in which the instance is present. (UUID)
            projectId: The ID of the Project in which the instance is present. (UUID)
            instanceId: The ID of the Instance. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Deleting the columnar instance {}, inside project {}, inside "
            "tenant {}.".format(instanceId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del("{}/{}".format(
            self.analytics_clusters_endpoint.format(organizationId, projectId),
            instanceId), params, headers)
        return resp

    def fetch_analytics_cluster_info(
            self,
            organizationId,
            projectId,
            instanceId,
            headers=None,
            **kwargs):
        """
        Fetches configuration / info of the instance given its ID.

        Args:
            organizationId: The tenantID in which the instance is present. (UUID)
            projectId: The ID of the Project in which the instance is present. (UUID)
            instanceId: The ID of the Instance. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code, dict
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Fetching the info for columnar instance {}, inside project {}, "
            "inside tenant {}.".format(instanceId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get("{}/{}".format(
            self.analytics_clusters_endpoint.format(organizationId, projectId),
            instanceId), params, headers)
        return resp

    def list_organization_level_analytics_clusters(
            self,
            organizationId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        """
        Lists all the columnar instances inside the specified tenant.

        Args:
            organizationId: The tenantID in which the instances are present. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)
            page: Sets what page you would like to view. (int)
            perPage: Sets how many results you would like to have on each page. (int)
            sortBy: Sets order of how you would like to sort results and also the key you would like to order by ([string])
                Example: sortBy=name
            sortDirection: The order on which the items will be sorted. (str)
                Accepted Values - asc / desc

        Returns:
            Success : Status Code, (list)
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Listing all columnar instances inside tenant {}"
            .format(organizationId))

        params = {}
        if page:
            params["page"] = page
        if perPage:
            params["perPage"] = perPage
        if perPage:
            params["sortBy"] = sortBy
        if perPage:
            params["sortDirection"] = sortDirection
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_get(self.org_level_analytics_clusters_endpoint.format(
            organizationId), params, headers)
        return resp

    def list_project_level_analytics_clusters(
            self,
            organizationId,
            projectId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        """
        Lists all the columnar instances inside a specified project under a tenant
        Args:
            organizationId: The tenantID in which the project is present. (UUID)
            projectId: The ID of the Project in which the instances are present. (UUID)
            page: Sets what page you would like to view. (int)
            perPage: Sets how many results you would like to have on each page. (int)
            sortBy: Sets order of how you would like to sort results and also the key you would like to order by ([string])
                Example: sortBy=name
            sortDirection: The order on which the items will be sorted. (str)
                Accepted Values - asc / desc
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code, (list)
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Listing all columnar instances inside project {}, "
            "inside tenant {}.".format(projectId, organizationId))

        params = {}
        if page:
            params["page"] = page
        if perPage:
            params["perPage"] = perPage
        if perPage:
            params["sortBy"] = sortBy
        if perPage:
            params["sortDirection"] = sortDirection
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_get(
            self.analytics_clusters_endpoint.format(organizationId, projectId),
            params, headers)
        return resp

    def update_analytics_cluster(
            self,
            organizationId,
            projectId,
            instanceId,
            name,
            nodes,
            support,
            description=None,
            headers=None,
            **kwargs):
        """
        Updates the specifications of a columnar instance based on Payload Params.

        Args:
            organizationId: The tenantID in which the instance is present. (UUID)
            projectId: The ID of the Project in which the instance is present. (UUID)
            instanceId: The ID of the Instance. (UUID)
            name: New name of the instance
            nodes: New number of nodes to be allotted to the instance. (int)
            support: The Plan and Timezone details for the instance. (dict)
                plan: Developer / Enterprise (string)
                timezone: one of the AWS timezones (string)
            description: New description of the columnar instance. (str)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Updating the columnar instance {}, inside project {}, inside "
            "tenant {}".format(instanceId, projectId, organizationId))

        params = {
            "name": name,
            "nodes": nodes,
            "support": support
        }
        if description is not None:
            params["description"] = description
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put("{}/{}".format(
            self.analytics_clusters_endpoint.format(organizationId, projectId),
            instanceId), params, headers)
        return resp

    def create_on_off_schedule(
            self,
            organizationId,
            projectId,
            instanceId,
            timezone,
            days,
            headers=None,
            **kwargs):
        """
        Creates a schedule for switching the columnar instance on off on weekly basis

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project. (UUID)
            instanceId: The ID of the instance which has to be scheduled on/off. (UUID)
            timezone: The local time-zone that the scheduled days shall fall into (str)
            days: List of each day having its schedule params (list)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Creating on off schedule for the instance {}, inside project {}, "
            "inside tenant {}.".format(instanceId, projectId, organizationId))

        params = {
            "timezone": timezone,
            "days": days
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.schedule_on_off_endpoint.format(
            organizationId, projectId, instanceId), params, headers)
        return resp

    def delete_on_off_schedule(
            self,
            organizationId,
            projectId,
            instanceId,
            headers=None,
            **kwargs):
        """
        Deletes the on/off schedule (if present) for the specified instance,

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project. (UUID)
            instanceId: The ID of the instance for which the scheduled has to be cleared. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Deleting on/off schedule for instance {}, inside project {}, "
            "inside tenant {}.".format(instanceId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del(self.schedule_on_off_endpoint.format(
            organizationId, projectId, instanceId), params, headers)
        return resp

    def fetch_on_off_schedule_info(
            self,
            organizationId,
            projectId,
            instanceId,
            headers=None,
            **kwargs):
        """
        Gets the details for the on/off schedule of the given instance.

        Args:
            organizationId: ID of the tenant. (UUID)
            projectId: ID of the Project. (UUID)
            instanceId: ID of the instance for which the on/off details have to be fetched. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Fetching on/off schedule details for the instance {}, inside "
            "project {}, inside tenant {}".format(instanceId, projectId,
                                                  organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.schedule_on_off_endpoint.format(
            organizationId, projectId, instanceId), params, headers)
        return resp

    def update_on_off_schedule(
            self,
            organizationId,
            projectId,
            instanceId,
            timezone,
            days,
            headers=None,
            **kwargs):
        """
        Change the on/off schedule for a specific instance.

        Args:
            organizationId: ID of the tenant. (UUID)
            projectId: ID of the Project. (UUID)
            instanceId: ID of the instance for which the on/off details have to be changed. (UUID)
            timezone: The local time-zone that the scheduled days shall fall into (str)
            days: List of each day having its schedule params (list)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Changing on/off schedule for instance {}, inside project {}, "
            "inside tenant {}".format(instanceId, projectId, instanceId))

        params = {
            "timezone": timezone,
            "days": days
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(self.schedule_on_off_endpoint.format(
            organizationId, projectId, instanceId), params, headers)
        return resp

    def create_cloud_snapshot_backup(
            self,
            organizationId,
            projectId,
            instanceId,
            retention=None,
            headers=None,
            **kwargs):
        """
        Creates a cloud snapshot backup for a Columnar analytics cluster.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project. (UUID)
            instanceId: The ID of the analytics cluster. (UUID)
            retention: Retention period in hours. (int, optional)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code 202, backup ID
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Creating cloud snapshot backup for instance {}, project {}, "
            "tenant {}.".format(instanceId, projectId, organizationId))

        params = {}
        if retention is not None:
            params["retention"] = retention
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(
            self.cloud_snapshot_backups_endpoint.format(
                organizationId, projectId, instanceId),
            params if params else None,
            headers)
        return resp

    def list_cloud_snapshot_backups(
            self,
            organizationId,
            projectId,
            instanceId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        """
        Lists cloud snapshot backups for a Columnar analytics cluster.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project. (UUID)
            instanceId: The ID of the analytics cluster. (UUID)
            page: Page number for pagination. (int)
            perPage: Results per page. (int)
            sortBy: Field to sort by. (str)
            sortDirection: Sort direction, 'asc' or 'desc'. (str)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code 200, list of backups
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Listing cloud snapshot backups for instance {}, project {}, "
            "tenant {}.".format(instanceId, projectId, organizationId))

        params = {}
        if page is not None:
            params["page"] = page
        if perPage is not None:
            params["perPage"] = perPage
        if sortBy is not None:
            params["sortBy"] = sortBy
        if sortDirection is not None:
            params["sortDirection"] = sortDirection
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_get(
            self.cloud_snapshot_backups_endpoint.format(
                organizationId, projectId, instanceId),
            params if params else None,
            headers)
        return resp

    def update_cloud_snapshot_backup_retention(
            self,
            organizationId,
            projectId,
            instanceId,
            backupId,
            retention,
            headers=None,
            **kwargs):
        """
        Updates the retention period for a cloud snapshot backup.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project. (UUID)
            instanceId: The ID of the analytics cluster. (UUID)
            backupId: The ID of the backup. (UUID)
            retention: New retention period in hours. (int)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code 204
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Updating retention for backup {}, instance {}, project {}, "
            "tenant {}.".format(backupId, instanceId, projectId, organizationId))

        params = {"retention": retention}
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(
            "{}/{}".format(
                self.cloud_snapshot_backups_endpoint.format(
                    organizationId, projectId, instanceId),
                backupId),
            params,
            headers)
        return resp

    def delete_cloud_snapshot_backup(
            self,
            organizationId,
            projectId,
            instanceId,
            backupId,
            headers=None,
            **kwargs):
        """
        Deletes a cloud snapshot backup.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project. (UUID)
            instanceId: The ID of the analytics cluster. (UUID)
            backupId: The ID of the backup to delete. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code 202
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Deleting cloud snapshot backup {}, instance {}, project {}, "
            "tenant {}.".format(backupId, instanceId, projectId, organizationId))

        params = {}
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_del(
            "{}/{}".format(
                self.cloud_snapshot_backups_endpoint.format(
                    organizationId, projectId, instanceId),
                backupId),
            params if params else None,
            headers)
        return resp

    def restore_cloud_snapshot_backup(
            self,
            organizationId,
            projectId,
            instanceId,
            backupId,
            headers=None,
            **kwargs):
        """
        Initiates a restore from a cloud snapshot backup.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project. (UUID)
            instanceId: The ID of the analytics cluster. (UUID)
            backupId: The ID of the backup to restore from. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code 202, restore ID
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Restoring cloud snapshot backup {}, instance {}, project {}, "
            "tenant {}.".format(backupId, instanceId, projectId, organizationId))

        params = {}
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(
            "{}/{}/restore".format(
                self.cloud_snapshot_backups_endpoint.format(
                    organizationId, projectId, instanceId),
                backupId),
            params if params else None,
            headers)
        return resp

    def list_cloud_snapshot_restores(
            self,
            organizationId,
            projectId,
            instanceId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        """
        Lists cloud snapshot restore operations for a Columnar analytics cluster.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project. (UUID)
            instanceId: The ID of the analytics cluster. (UUID)
            page: Page number for pagination. (int)
            perPage: Results per page. (int)
            sortBy: Field to sort by. (str)
            sortDirection: Sort direction, 'asc' or 'desc'. (str)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code 200, list of restores
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Listing cloud snapshot restores for instance {}, project {}, "
            "tenant {}.".format(instanceId, projectId, organizationId))

        params = {}
        if page is not None:
            params["page"] = page
        if perPage is not None:
            params["perPage"] = perPage
        if sortBy is not None:
            params["sortBy"] = sortBy
        if sortDirection is not None:
            params["sortDirection"] = sortDirection
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_get(
            "{}/restores".format(
                self.cloud_snapshot_backups_endpoint.format(
                    organizationId, projectId, instanceId)),
            params if params else None,
            headers)
        return resp

    def upsert_cloud_snapshot_backup_schedule(
            self,
            organizationId,
            projectId,
            instanceId,
            interval,
            retention,
            start_time,
            headers=None,
            **kwargs):
        """
        Creates or updates a cloud snapshot backup schedule for a Columnar analytics cluster.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project. (UUID)
            instanceId: The ID of the analytics cluster. (UUID)
            interval: Backup frequency in hours. (int)
            retention: Retention period in hours. (int)
            start_time: Start time in ISO 8601 format. (str)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code 204
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Upserting cloud snapshot backup schedule for instance {}, "
            "project {}, tenant {}.".format(instanceId, projectId, organizationId))

        params = {
            "interval": interval,
            "retention": retention,
            "startTime": start_time,
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(
            self.cloud_snapshot_backup_schedule_endpoint.format(
                organizationId, projectId, instanceId),
            params,
            headers)
        return resp

    def get_cloud_snapshot_backup_schedule(
            self,
            organizationId,
            projectId,
            instanceId,
            headers=None,
            **kwargs):
        """
        Retrieves the cloud snapshot backup schedule for a Columnar analytics cluster.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project. (UUID)
            instanceId: The ID of the analytics cluster. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code 200 (schedule exists) or 204 (no schedule)
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Getting cloud snapshot backup schedule for instance {}, "
            "project {}, tenant {}.".format(instanceId, projectId, organizationId))

        params = {}
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_get(
            self.cloud_snapshot_backup_schedule_endpoint.format(
                organizationId, projectId, instanceId),
            params if params else None,
            headers)
        return resp

    def delete_cloud_snapshot_backup_schedule(
            self,
            organizationId,
            projectId,
            instanceId,
            headers=None,
            **kwargs):
        """
        Deletes the cloud snapshot backup schedule for a Columnar analytics cluster.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project. (UUID)
            instanceId: The ID of the analytics cluster. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code 204
            Error : message, hint, code, HttpStatusCode
        """
        self.columnar_ops_API_log.info(
            "Deleting cloud snapshot backup schedule for instance {}, "
            "project {}, tenant {}.".format(instanceId, projectId, organizationId))

        params = {}
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_del(
            self.cloud_snapshot_backup_schedule_endpoint.format(
                organizationId, projectId, instanceId),
            params if params else None,
            headers)
        return resp
