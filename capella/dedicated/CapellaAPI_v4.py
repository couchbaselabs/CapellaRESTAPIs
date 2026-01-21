# -*- coding: utf-8 -*-
# Generic/Built-in
import base64
import logging

import json

from ..lib.APIRequests import APIRequests
from ..common.CapellaAPI_v4 import CommonCapellaAPI


class ClusterOperationsAPIs(APIRequests):

    def __init__(self, url, secret, access, bearer_token):
        super(ClusterOperationsAPIs, self).__init__(
            url, secret, access, bearer_token)
        self.cluster_ops_API_log = logging.getLogger(__name__)
        organization_endpoint = "/v4/organizations"
        self.cluster_endpoint = organization_endpoint + "/{}/projects/{}/clusters"
        self.allowedCIDR_endpoint = organization_endpoint + "/{}/projects/{}/clusters/{}/allowedcidrs"
        self.db_user_endpoint = organization_endpoint + "/{}/projects/{}/clusters/{}/users"
        self.bucket_endpoint = organization_endpoint + "/{}/projects/{}/clusters/{}/buckets"
        self.scope_endpoint = organization_endpoint + "/{}/projects/{}/clusters/{}/buckets/{}/scopes"
        self.collection_endpoint = organization_endpoint + "/{}/projects/{}/clusters/{}/buckets/{}/scopes/{}/collections"
        self.backups_endpoint = organization_endpoint + "/{}/projects/{}/clusters/{}/backups"
        self.backup_schedule_endpoint = organization_endpoint + "/{}/projects/{}/clusters/{}/buckets/{}/backup/schedules"
        self.sample_bucket_endpoint = organization_endpoint + "/{}/projects/{}/clusters/{}/sampleBuckets"
        self.org_appservice_api = organization_endpoint + "/{}/appservices"
        self.cluster_appservice_api = self.cluster_endpoint + "/{}/appservices"
        self.cluster_on_off_schedule_endpoint = self.cluster_endpoint + "/{}/onOffSchedule"
        self.cluster_on_off_endpoint = self.cluster_endpoint + "/{}/activationState"
        self.appservice_on_off_endpoint = self.cluster_appservice_api + "/{}/activationState"

        self.alerts_endpoint = organization_endpoint + "/{}/projects/{}/alertIntegrations"
        self.test_alert_endpoint = self.alerts_endpoint[:-1] + "Test"

        self.audit_log_exports_endpoint = self.cluster_endpoint + "/{}/auditLogExports"
        self.audit_log_endpoint = self.cluster_endpoint + "/{}/auditLog"
        self.audit_log_events_endpoint = self.cluster_endpoint + "/{}/auditLogEvents"

        self.flush_buckets_endpoint = self.bucket_endpoint + "/{}/flush"
        self.bucket_migration_endpoint = self.cluster_endpoint + "/{}/bucketStorageMigration"
        self.vpc_endpoint = self.cluster_endpoint + "/{}/networkPeers"
        self.vnet_peering_cmd_endpoint = self.vpc_endpoint + "/networkPeerCommand"

        self.private_network_service_endpoint = self.cluster_endpoint + "/{}/privateEndpointService"
        self.list_private_networks_endpoint = self.private_network_service_endpoint + "/endpoints"
        self.private_network_command_endpoint = self.list_private_networks_endpoint[:-1] + "Command"
        self.associate_private_network_endpoint = self.list_private_networks_endpoint + "/{}/associate"
        self.unassociate_private_network_endpoint = self.list_private_networks_endpoint + "/{}/unassociate"

        self.tenant_events_endpoint = organization_endpoint + "/{}/events"
        self.project_events_endpoint = organization_endpoint + "/{}/projects/{}/events"

        self.app_svc_audit_log_endpoint = self.cluster_appservice_api + "/{}/auditLog"
        self.app_svc_audit_log_exports_endpoint = self.app_svc_audit_log_endpoint + "Exports"
        self.app_svc_audit_log_streaming_endpoint = self.app_svc_audit_log_endpoint + "Streaming"
        self.app_svc_audit_log_config_endpoint = self.cluster_appservice_api + "/{}/appEndpoints/{}/auditLog"
        self.app_svc_audit_log_events_endpoint = self.app_svc_audit_log_config_endpoint + "Events"

        self.index_endpoint = self.cluster_endpoint + "/{}/queryService/indexes"
        self.index_build_status_endpoint = self.cluster_endpoint + "/{}/queryService/indexBuildStatus"
        self.bulk_index_check_endpoint = self.cluster_endpoint + "/{}/queryService/bulkIndexCheck"

        self.app_endpoints_endpoint = self.cluster_appservice_api + "/{}/appEndpoints"
        self.app_endpoint_on_off_endpoint = self.app_endpoints_endpoint + "/{}/activationStatus"
        self.app_endpoint_resync_endpoint = self.app_endpoints_endpoint + "/{}/resync"
        self.import_filter_endpoint = self.app_endpoints_endpoint + "/{}/importFilter"
        self.access_control_function_endpoint = self.app_endpoints_endpoint + "/{}/accessControlFunction"
        self.app_endpoint_collections_endpoint = self.app_endpoints_endpoint + "/{}/collections"

        self.app_endpoint_OIDC_provider = self.app_endpoints_endpoint + "/{}/oidcProviders"
        self.app_service_admin_users = self.cluster_appservice_api + "/{}/adminUsers"
        self.app_endpoint_admin_users = self.app_endpoints_endpoint + "/{}/adminUsers"
        self.cors_endpoint = self.app_endpoints_endpoint + "/{}/cors"

        self.free_tier_cluster_endpoint = self.cluster_endpoint + "/freeTier"
        self.free_tier_cluster_activation_state_endpoint = self.free_tier_cluster_endpoint + "/{}/activationState"
        self.free_tier_bucket_endpoint = self.cluster_endpoint + "/{}/buckets/freeTier"
        self.free_tier_app_svc_endpoint = self.cluster_endpoint + "/{}/appservices/freeTier"

        self.user_endpoint = organization_endpoint + "/{}/users"

        # fusion 2
        self.express_scaling_endpoint = self.cluster_endpoint + "/{}/expressScaling"

        # appService Log Streaming
        self.app_svc_log_streaming_endpoint = self.cluster_appservice_api + "logStreaming"
        self.app_endpoint_log_streaming_endpoint = self.app_endpoints_endpoint + "logStreaming"
        self.app_svc_log_streaming_pause_resume_endpoint = self.app_svc_log_streaming_endpoint + "/activationState"
    
    def create_user(
            self,
            organizationId,
            resources,
            email,
            name,
            organizationRoles,
            headers=None,
            **kwargs):
        """
        Invites a new user under the organization.

        Args:
            organizationId: The ID of the tenant in which the user is created. (UUID)
            resources: The resources the user has access to. (list)
            email: The email of the user to be created. (string)
            name: The name of the user to be created. (string)
            organizationRole: The role of the user in the organization. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode.
        """
        self.cluster_ops_API_log.info(
            "Creating user: {}, inside organization: {}".format(email, organizationId))
        params = {
            "resources": resources,
            "email": email,
            "name": name,
            "organizationRoles": organizationRoles
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.user_endpoint.format(organizationId),
                             params, headers)
        return resp

    def fetch_user_info(
            self,
            organizationId,
            userId,
            headers=None,
            **kwargs):
        """
        Fetches the details of a user.

        Args:
            organizationId: The ID of the tenant in which the user is present. (UUID)
            userId: The ID of the user to fetch the details of. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)
        
        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode.
        """
        self.cluster_ops_API_log.info(
            "Fetching details for user: {}, inside organization: {}".format(userId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get("{}/{}".format(self.user_endpoint.format(organizationId), userId), params, headers)
        return resp
    
    def update_user(
            self,
            organizationId,
            userId,
            body,
            headers=None,
            **kwargs):
        """
        Updates organizationRole and resources of the user.

        Args:
            organizationId: The ID of the tenant in which the user is present. (UUID)
            userId: The ID of the user to update the details of. (UUID)
            body: The body having new roles for the user. (dict)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)
        
        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode.
        """
        self.cluster_ops_API_log.info(
            "Updating user: {}, inside organization: {}".format(userId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_put("{}/{}".format(self.user_endpoint.format(organizationId), userId), body, headers)
        return resp

    def delete_user(
            self,
            organizationId,
            userId,
            headers=None,
            **kwargs):
        """
        Removes user from the organization.

        Args:
            organizationId: The ID of the tenant in which the user is present. (UUID)
            userId: The ID of the user to delete. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)
        
        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode.
        """
        self.cluster_ops_API_log.info(
            "Deleting user: {}, inside organization: {}".format(userId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del("{}/{}".format(self.user_endpoint.format(organizationId), userId), params, headers)
        return resp
    
    def list_users(
            self,
            organizationId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            projectId=None,
            headers=None,
            **kwargs):
        """
        Lists all the users in the organization and filter on the basis of projectId.

        Args:
            organizationId: The ID of the tenant in which the users are present. (UUID)
            page: The page number to fetch the users from. (int)[optional]
            perPage: The number of users to fetch per page. (int)[optional]
            sortBy: The field to sort the users by. (string)[optional]
            sortDirection: The direction to sort the users by. (string)[optional]
            projectId: The ID of the project to filter the users by. (UUID)[optional]
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)
        
        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode.
        """
        self.cluster_ops_API_log.info(
            "Listing users inside organization: {}".format(organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        if page:
            params["page"] = page
        if perPage:
            params["perPage"] = perPage
        if sortBy:
            params["sortBy"] = sortBy
        if sortDirection:
            params["sortDirection"] = sortDirection
        if projectId:
            params["projectId"] = projectId

        resp = self.api_get(self.user_endpoint.format(organizationId), params, headers)
        return resp
    
    def fetch_free_tier_cluster_info(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        """
        Get details of the free tier cluster.
        While only cluster name, description, CSP, region and CIDR are configurable, other read only fields are retrieved.

        Args:
            organizationId: The ID of the tenant in which the cluster is present. (UUID)
            projectId: ID of the project in which the cluster is present. (UUID)
            clusterId: ID of the free-tier cluster to fetch the details. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching details for free-tier cluster: {}, inside project: {}, "
            "inside tenant: {}".format(organizationId, projectId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get("{}/{}".format(
            self.free_tier_cluster_endpoint.format(organizationId, projectId),
            clusterId), params, headers)
        return resp

    def create_free_tier_cluster(
            self,
            organizationId,
            projectId,
            name,
            cloudProvider,
            description="",
            headers=None,
            **kwargs):
        """
        Creates a free tier cluster. This is a 1 node cluster than only runs data, query, index and search services.
        You can have at most 1 free tier cluster per tenant.

        Args:
            organizationId: The ID of the tenant in which the cluster is created. (UUID)
            projectId: ID of the project in which the cluster is created. (UUID)
            name: Name of the cluster to be created. (string)
            cloudProvider: The cloud provider related details for the cluster to be created. (JSON)
            description: Description of the cluster to be created. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Creating cluster inside project: {}, inside tenant: {}".format(
                projectId, organizationId))
        params = {
            "name": name,
            "cloudProvider": cloudProvider,
            "description": description
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.free_tier_cluster_endpoint.format(
            organizationId, projectId), params, headers)
        return resp

    def delete_free_tier_cluster(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        """
        Retrieves the free tier cluster in the project, if any.

        Args:
            organizationId: The ID of the tenant in which the cluster is present. (UUID)
            projectId: ID of the project in which the cluster is present. (UUID)
            clusterId: ID of the cluster to be deleted. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Deleting free-tier cluster: {}, in project: {}, in tenant: {}"
            .format(clusterId, projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del("{}/{}".format(self.free_tier_cluster_endpoint
                                           .format(organizationId, projectId),
                                           clusterId), params, headers)
        return resp

    def update_free_tier_cluster(
            self,
            organizationId,
            projectId,
            clusterId,
            name,
            description="",
            headers=None,
            **kwargs):
        """
        Updates an existing free tier cluster. Only name and description are configurable.

        Args:
            organizationId: The ID of the tenant in which the cluster is created. (UUID)
            projectId: ID of the project in which the cluster is created. (UUID)
            clusterId: ID of the cluster to be updated. (UUID)
            name: Name of the cluster to be created. (string)
            description: Description of the cluster to be created. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Creating cluster inside project: {}, inside tenant: {}".format(
                projectId, organizationId))
        params = {
            "name": name,
            "description": description
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put("{}/{}".format(
            self.free_tier_cluster_endpoint.format(
                organizationId, projectId), clusterId),
            params, headers)
        return resp

    def turn_free_tier_cluster_on(
            self,
            organizationId,
            projectId,
            clusterId,
            turnOnLinkedAppService,
            headers=None,
            **kwargs):
        """
        Turn free tier cluster on.

        Args:
            organizationId: The ID of the tenant in which the cluster is present. (UUID)
            projectId: ID of the project in which the cluster is present. (UUID)
            clusterId: ID of the free-tier cluster inside which the app service is. (UUID)
            turnOnLinkedAppService: If the linked app service shall be turned on after the cluster is turned on as well. (bool)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Turning on Free Tier Cluster: {}, inside Project: {}, inside Org:"
            " {}".format(clusterId, projectId, organizationId))

        params = {
            "turnOnLinkedAppService": turnOnLinkedAppService
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(
            self.free_tier_cluster_activation_state_endpoint.format(
                organizationId, projectId, clusterId), params, headers)
        return resp

    def turn_free_tier_cluster_off(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        """
        Turn free tier cluster off.

        Args:
            organizationId: The ID of the tenant in which the cluster is present. (UUID)
            projectId: ID of the project in which the cluster is present. (UUID)
            clusterId: ID of the free-tier cluster inside which the app service is. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Turning on Free Tier Cluster: {}, inside Project: {}, inside Org:"
            " {}".format(clusterId, projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del(
            self.free_tier_cluster_activation_state_endpoint.format(
                organizationId, projectId, clusterId), params, headers)
        return resp

    def create_free_tier_app_service(
            self,
            organizationId,
            projectId,
            clusterId,
            name,
            description="",
            headers=None,
            **kwargs):
        """
        Creates a free tier app service. Free tier app service can only be turned off/on when the linked free tier cluster is turned off/on.

        Args:
            organizationId: The ID of the tenant in which the cluster is present. (UUID)
            projectId: ID of the project in which the cluster is present. (UUID)
            clusterId: ID of the free-tier cluster inside which the app service is to be created. (UUID)
            name: The name of the app service to be created. (string)
            description: Describe the app service in any way. (string)[optional]
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Creating a free tier app service inside cluster: {}, inside "
            "project: {}, inside org: {}".format(clusterId, projectId,
                                                 organizationId))
        params = {
            "name": name,
            "description": description
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.free_tier_app_svc_endpoint.format(
            organizationId, projectId, clusterId),
            params, headers)
        return resp

    def update_free_tier_app_service(
            self,
            organizationId,
            projectId,
            clusterId,
            appId,
            name,
            description="",
            headers=None,
            **kwargs):
        """
        Updates an existing free tier app service. Only name and description are configurable.

        Args:
            organizationId: The ID of the tenant in which the cluster is present. (UUID)
            projectId: ID of the project in which the cluster is present. (UUID)
            clusterId: ID of the free-tier cluster inside which the app service is. (UUID)
            appId: ID of the app service to be updated. (UUID)
            name: The updated name of the app service. (string)
            description: Describe the app service in any way. (string)[optional]
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Updating app service: {}, linked to cluster: {}, inside project: "
            "{}, inside Org: {}".format(appId, clusterId, projectId,
                                        organizationId))
        params = {
            "name": name,
            "description": description
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put("{}/{}".format(self.free_tier_app_svc_endpoint
                                           .format(organizationId, projectId,
                                                   clusterId),
                                           appId), params, headers)
        return resp

    def fetch_free_tier_app_service_info(
            self,
            organizationId,
            projectId,
            clusterId,
            appId,
            headers=None,
            **kwargs):
        """
        Fetches the details of the free tier app service.
        While only name and description are configurable, other read only fields will be displayed.

        Args:
            organizationId: The ID of the tenant in which the cluster is present. (UUID)
            projectId: ID of the project in which the cluster is present. (UUID)
            clusterId: ID of the free-tier cluster inside which the app service is. (UUID)
            appId: ID of the app service to be updated. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching info for app service: {}, linked to cluster: {}, inside "
            "project: {}, inside Org: {}".format(appId, clusterId,
                                                 projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get("{}/{}".format(self.free_tier_app_svc_endpoint
                                           .format(organizationId, projectId,
                                                   clusterId),
                                           appId), params, headers)
        return resp

    def delete_free_tier_app_service(
            self,
            organizationId,
            projectId,
            clusterId,
            appId,
            headers=None,
            **kwargs):
        """
        Deletes an existing free tier app service.

        Args:
            organizationId: The ID of the tenant in which the cluster is present. (UUID)
            projectId: ID of the project in which the cluster is present. (UUID)
            clusterId: ID of the free-tier cluster inside which the app service is. (UUID)
            appId: ID of the free-tier app service to be deleted. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Deleting the AppSvc: {}, inside cluster: {}, inside project: {}, "
            "inside Org: {}".format(appId, clusterId, projectId,
                                    organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del("{}/{}".format(self.free_tier_app_svc_endpoint
                            .format(organizationId, projectId, clusterId),
                                appId), params, headers)
        return resp

    def create_free_tier_bucket(
            self,
            organizationId,
            projectId,
            clusterId,
            name,
            memoryAllocationInMb,
            headers=None,
            ** kwargs):
        """
        Creates a new free tier bucket. This is a Couchbase bucket where only the name a memory quota is configurable. Other bucket properties use default values.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the free tier cluster to create bucket inside it. (UUID)
            name: Name of the bucket to be created, (string)
            memoryAllocationInMb: Memory to be allocated to the bucket. (int)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Creating a bucket inside free tier cluster: {}, inside "
            "project: {}, inside tenant: {}".format(clusterId, projectId,
                                                    organizationId))
        params = {
            "name": name,
            "memoryAllocationInMb": memoryAllocationInMb,
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.free_tier_bucket_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def delete_free_tier_bucket(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            headers=None,
            **kwargs):
        """
        Deletes an existing free tier bucket.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the free tier cluster to delete bucket inside it. (UUID)
            bucketId: ID of the free tier bucket to be deleted. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Deleting bucket: {}, inside cluster: {}, inside project: {}, "
            "inside tenant: {}".format(bucketId, clusterId, projectId,
                                       organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del("{}/{}".format(self.free_tier_bucket_endpoint
                            .format(organizationId, projectId, clusterId),
                                    bucketId), params, headers)
        return resp

    def fetch_free_tier_bucket_info(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            headers=None,
            **kwargs):
        """
        Get bucket. While only name and memory quota are configurable for free tier buckets, the response will show additional read only bucket properties such as replicas, etc.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the free tier cluster to delete bucket inside it. (UUID)
            bucketId: ID of the free tier bucket to be fetched. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching bucket: {}, inside cluster: {}, inside project: {}, "
            "inside tenant: {}".format(bucketId, clusterId, projectId,
                                       organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get("{}/{}".format(self.free_tier_bucket_endpoint
                            .format(organizationId, projectId, clusterId),
                                    bucketId), params, headers)
        return resp

    def update_free_tier_bucket(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            memoryAllocationInMb,
            headers=None,
            **kwargs):
        """
        Updates an existing free tier bucket. Only bucket memory quota is configurable. Once created bucket name cannot be changed.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the free tier cluster to delete bucket inside it. (UUID)
            bucketId: ID of the free tier bucket to be fetched. (string)
            memoryAllocationInMb: The new configured memory for the bucket. (int)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching bucket: {}, inside cluster: {}, inside project: {}, "
            "inside tenant: {}".format(bucketId, clusterId, projectId,
                                       organizationId))
        params = {
            "memoryAllocationInMb": memoryAllocationInMb
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put("{}/{}".format(self.free_tier_bucket_endpoint
                            .format(organizationId, projectId, clusterId),
                                    bucketId), params, headers)
        return resp

    def list_free_tier_bucket(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        """
        Lists all buckets in the free tier cluster. While only name and memory quota are configurable for free tier buckets, the response will show additional read only bucket properties such as replicas, etc.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the free tier cluster to create bucket inside it. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Creating a bucket inside free tier cluster: {}, inside "
            "project: {}, inside tenant: {}".format(clusterId, projectId,
                                                    organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.free_tier_bucket_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def create_app_endpoint(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            name,
            deltaSyncEnabled,
            bucket,
            scopes,
            xattr,
            cors,
            headers=None,
            **kwargs):
        """
        Creates an App Endpoint.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the App Service to create an Endpoint inside. (UUID)
            name: Of the App Endpoint to be created. (string)
            deltaSyncEnabled: (bool)
            bucket: Name of the bucket to link the App Endpoint with. (string)
            scopes: Scopes to be associated inside the given  bucket. (obj)
            xattr: userXattrKey for configuring the App Endpoint. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Creating an App endpoint inside the App Service: {}, inside the "
            "Cluster: {}, inside the Project: {}, inside the tenant: {}"
            .format(appServiceId, clusterId, projectId, organizationId))
        params = {
            "name": name,
            "deltaSyncEnabled": deltaSyncEnabled,
            "bucket": bucket,
            "scopes": scopes,
            "userXattrKey": xattr,
            "cors":cors
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.app_endpoints_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            params, headers)
        return resp

    def fetch_app_endpoint_info(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """
        Fetches the details of the given App Endpoint.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the App Service to create an Endpoint inside. (UUID)
            appEndpointName: Name of the App Endpoint to fetch details. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching details for app Endpoint: {}, linked to App Svc: {}, "
            "inside Cluster: {}, inside Project: {}, inside tenant: {}".format(
                appEndpointName, appServiceId, clusterId, projectId,
                organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get("{}/{}".format(self.app_endpoints_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            appEndpointName), params, headers)
        return resp

    def delete_app_endpoint(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """
        Deletes a given App Endpoint.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the App Service to create an Endpoint inside. (UUID)
            appEndpointName: Name of the App Endpoint to be deleted. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code (ONLY).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Deleting  app Endpoint: {}, linked to App Svc: {}, inside "
            "Cluster: {}, inside Project: {}, inside tenant: {}".format(
                appEndpointName, appServiceId, clusterId, projectId,
                organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del("{}/{}".format(self.app_endpoints_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            appEndpointName), params, headers)
        return resp

    def list_app_endpoints(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        """
        Successfully lists all the App Endpoints under a specific App Service.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            appServiceId: ID of the app service for which app endpoint are to be listed. (UUID)
            page: Sets what page you would like to view. (int)
            perPage: Sets how many results you would like to have on each page. (int)
            sortBy: Sets order of how you would like to sort results and also the key you would like to order by ([string])
                Example: sortBy=name
            sortDirection: The order on which the items will be sorted. (str)
                Accepted Values - asc / desc
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and Response Body
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Listing App Endpoints in App Service: {}, inside cluster: {}, "
            "inside project: {}, inside tenant: {}".format(
                appServiceId, clusterId, projectId, organizationId))
        params = {}
        if page:
            params["page"] = page
        if perPage:
            params["perPage"] = perPage
        if sortBy:
            params["sortBy"] = sortBy
        if sortDirection:
            params["sortDirection"] = sortDirection
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_get(self.app_endpoints_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            params, headers)
        return resp

    def list_app_endpoint_collections(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            page=None,
            perPage=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        """
               Lists all the collections under a specific App Endpoint along with their associated configurations such as Access Control function, Import Filter or user defined xattr key.

               Args:
                   organizationId: The ID of the tenant. (UUID)
                   projectId: ID of the project inside the tenant. (UUID)
                   clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
                   appServiceId: ID of the app service for which app endpoint are to be listed. (UUID)
                   AppEndpointName: the name of the appservice we are getting the collections from.
                   page: Sets what page you would like to view. (int)
                   perPage: Sets how many results you would like to have on each page. (int)
                   sortDirection: The order on which the items will be sorted. (str)
                       Accepted Values - asc / desc
                   headers: Headers to be sent with the API call. (dict)
                   **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

               Returns:
                   Success : Status Code and Response Body
                   Error : message, hint, code, HttpStatusCode
               """
        self.cluster_ops_API_log.info(
            "Listing Collections in App Endpoints {} in App Service: {}, "
            "inside "
            "cluster: {}, "
            "inside project: {}, inside tenant: {}".format(
                appEndpointName, appServiceId, clusterId, projectId,
                organizationId))
        params = {}
        if page:
            params["page"] = page
        if perPage:
            params["perPage"] = perPage
        if sortDirection:
            params["sortDirection"] = sortDirection
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_get(self.app_endpoint_collections_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName),
            params, headers)
        return resp


    def update_app_endpoint(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            name,
            deltaSyncEnabled,
            bucket,
            scopes,
            xattr,
            cors,
            headers=None,
            **kwargs):
        """
        Updates a specified App Endpoint’s configurations such as Access Control function, Import Filter, Delta Sync, or user defined xattr key.
        All fields are required, the App Endpoint and bucket names cannot be changed.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            appServiceId: ID of the app service for which app endpoint are to be listed. (UUID)
            appEndpointName: Name of the App Endpoint to be updated. (string)
            name: Updated name of the App Endpoint. (string)
            deltaSyncEnabled: To have the delta sync enabled or disabled for the endpoint. (bool)
            bucket: Name of the bucket linked to the app endpoint. (string)
            scopes: Scopes to be included in the app endpoint config inside the bucket. (list)
            xattr: User X-Attributes Key to be used with the endpoint. (string)
            cors: User's cors data. (dict)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code (ONLY).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Updating App Endpoint: {}, linked to App Service: {}, inside "
            "cluster: {}, inside project: {}, inside tenant: {}"
            .format(appEndpointName, appServiceId, clusterId, projectId,
                    organizationId))
        params = {
            "name": name,
            "deltaSyncEnabled": deltaSyncEnabled,
            "bucket": bucket,
            "scopes": scopes,
            "userXattrKey": xattr,
            "cors": cors
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put("{}/{}".format(self.app_endpoints_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            appEndpointName), params, headers)
        return resp

    def resume_app_endpoint(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """
        Brings an App Endpoint online to close and reopen the connection to the backing Cluster bucket, re-establish access from the Public REST API and accept all incoming Admin API requests.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            appServiceId: ID of the app service for which app endpoint are to be listed. (UUID)
            appEndpointName: Name of the App Endpoint to be resumed. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code (ONLY).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Turning on appEndpoint: {}, linked to appService: {}, inside "
            "cluster: {}, inside project: {}, inside tenant: {}".format(
                appEndpointName, appServiceId, clusterId, projectId,
                organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_post(self.app_endpoint_on_off_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName), params, headers)
        return resp

    def pause_app_endpoint(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """
        Take the database offline to run resync or to make changes without disrupting current App Endpoint operations.
        Clients currently connected to the App Endpoint will not be able to sync data with the Cluster while the App Endpoint is paused.
        This will not take the backing Cluster bucket offline.
        Pausing an App Endpoint that is in the progress of coming online will pause the App Endpoint after it comes online.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            appServiceId: ID of the app service for which app endpoint are to be listed. (UUID)
            appEndpointName: Name of the App Endpoint to be paused. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Turning off appEndpoint: {}, linked to appService: {}, inside "
            "cluster: {}, inside project: {}, inside tenant: {}".format(
                appEndpointName, appServiceId, clusterId, projectId,
                organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(self.app_endpoint_on_off_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName), params, headers)
        return resp

    def delete_access_function(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointKeyspace,
            headers=None,
            **kwargs):
        """
        Deletes the Access Control and Validation function for the given keyspace.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the app service linked to the cluster. (UUID)
            appEndpointKeyspace: The name of the App Endpoint and the scope and collection separated by period (.) .
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Deleting the accessFunction in appEndpointKeyspa {} in "
            "appService {} in cluster {} in project {} in organization {}".format(
                appEndpointKeyspace, appServiceId, clusterId, projectId,
                organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del(self.access_control_function_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointKeyspace), params, headers)
        return resp

    def fetch_app_endpoint_c_o_r_s_info(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """
        Fetch the App Endpoint Cross-Origin Resource Sharing (CORS) Configuration.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the App Service to create an Endpoint inside. (UUID)
            appEndpointName: Name of the App Endpoint to fetch details. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching details for app Endpoint CORS : {}, linked to App Svc: {}, "
            "inside Cluster: {}, inside Project: {}, inside tenant: {}".format(
                appEndpointName, appServiceId, clusterId, projectId,
                organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.cors_endpoint.format(organizationId, projectId, clusterId, appServiceId,
            appEndpointName), params, headers)
        return resp

    def update_cors(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            cors,
            headers=None,
            **kwargs):
        """
        Upsert the App Endpoint Cross-Origin Resource Sharing (CORS) Configuration

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            appServiceId: ID of the app service for which app endpoint are to be listed. (UUID)
            appEndpointName: Name of the App Endpoint to be updated. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code (ONLY).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Updating cors for  App Endpoint: {}, linked to App Service: {}, inside "
            "cluster: {}, inside project: {}, inside tenant: {}"
            .format(appEndpointName, appServiceId, clusterId, projectId,
                    organizationId))
        params = {
            "origin": [
                "http://example.com",
                "http://staging.example.com"
            ],
            "loginOrigin": [
                "http://example.com"
            ],
            "headers": [
                "Content-Type"
            ],
            "maxAge": 600,
            "disabled": False
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(self.cors_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName), params, headers)
        return resp

    def update_access_control_function(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointKeyspace,
            payload,
            headers=None,
            **kwargs):
        """
        Used to upsert a custom Access Control and Validation function for the given keyspace.
        This is a Javascript function specified at a keyspace, where a user’s read/write access is defined for documents in that particular keyspace.
        Every document mutation is processed by this function.
        If an Access Control function is not explicitly defined, a default is applied.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the app service linked to the cluster. (UUID)
            appEndpointKeyspace: The name of the App Endpoint and the scope and collection separated by period (.) .
            payload: The new import filter function to be added in the request. (string)
            payload: Payload string coming into `params`. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Updating the access control function in appEndpointKeyspace {} "
            "in appService: {} in cluster: {} in project: {} in "
            "organization: {}".format(
                appEndpointKeyspace, appServiceId, clusterId, projectId,
                organizationId))
        params = payload
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(self.access_control_function_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointKeyspace), None, headers, params)
        return resp

    def fetch_access_function_info(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointKeyspace,
            headers=None,
            **kwargs):
        """
        Retrieves the Access Control and Validation function for the given keyspace.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the app service linked to the cluster. (UUID)
            appEndpointKeyspace: The name of the App Endpoint and the scope and collection separated by period (.) .
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching access control function info for appEndpointKeyspace: {}"
            " in appService: {} in cluster {} in project {} in organization {}"
            .format(appEndpointKeyspace, appServiceId, clusterId, projectId,
                    organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.access_control_function_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointKeyspace), params, headers)
        return resp

    def fetch_app_endpoint_resync_info(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """
        Fetches the Resync status of the given App Endpoint.
        If no resync operation was triggered, the response will say the status is completed with 0 values for other properties.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            appServiceId: ID of the app service for which app endpoint are to be listed. (UUID)
            appEndpointName: Name of the App Endpoint to be paused. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching resync status for appEndpoint: {}, inside appService: "
            "{}, linked to cluster: {}, inside project: {}, inside tenant: {}"
            .format(appEndpointName, appServiceId, clusterId, projectId,
                    organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.app_endpoint_resync_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName), params, headers)
        return resp

    def start_resync(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            scopes,
            headers=None,
            **kwargs):
        """
        Initialises the Resync operation for the given collections.
        By default, all collections that require resync will be resynced unless they are specified in the scopes property, in which case only the specified collections that require resync will be resynced.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            appServiceId: ID of the app service for which app endpoint are to be listed. (UUID)
            appEndpointName: Name of the App Endpoint to be paused. (string)
            scopes: The scopes that need to be included in the resync operation. (obj: map[string]{}interface)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Starting resync for appEndpoint: {}, inside appService: {}, "
            "linked to cluster: {}, inside project: {}, inside tenant: {}"
            .format(appEndpointName, appServiceId, clusterId, projectId,
                    organizationId))
        params = {
            "scopes": scopes,
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.app_endpoint_resync_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName), params, headers)
        return resp

    def stop_resync(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """
        Stops the Resync operation. When stopping resync, it will be stopped for all collections being processed.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            appServiceId: ID of the app service for which app endpoint are to be listed. (UUID)
            appEndpointName: Name of the App Endpoint to be paused. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Stopping resync for appEndpoint: {}, inside appService: {}, "
            "linked to cluster: {}, inside project: {}, inside tenant: {}"
            .format(appEndpointName, appServiceId, clusterId, projectId,
                    organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del(self.app_endpoint_resync_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName), params, headers)
        return resp

    def fetch_import_filter_info(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointKeyspace,
            headers=None,
            **kwargs):
        """
        Retrieves the Import Filter for the given keyspace.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the app service linked to the cluster. (UUID)
            appEndpointKeyspace:
            headers:
            **kwargs:

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching the importFilter info in appEndpointKeyspace: {} in "
            "appService: {} in cluster: {} in project: {} in tenant: {}"
            .format(appEndpointKeyspace, appServiceId, clusterId, projectId,
                    organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.import_filter_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointKeyspace), params, headers)
        return resp

    def delete_import_filter(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointKeyspace,
            headers=None,
            **kwargs):
        """
        Retrieves the Import Filter for the given keyspace.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the app service linked to the cluster. (UUID)
            appEndpointKeyspace:
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """

        self.cluster_ops_API_log.info(
            "Deleting the importFilter for appEndpointKeyspace: {} in "
            "appService: {} in cluster:{} in project: {} in tenant: {}"
            .format(appEndpointKeyspace, appServiceId, clusterId, projectId,
                    organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del(self.import_filter_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointKeyspace), params, headers)
        return resp

    def update_import_filter(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointKeyspace,
            payload,
            headers=None,
            **kwargs):
        """
        Updates the Import Filter for the given keyspace.
        By default, there is no import filter and all documents are imported.
        Import Filters identify the subset of documents eligible to be replicated by App services based on user-defined requirements.
        This subset is applied to all future mutations.
        Once the document has been imported and processed by the App Endpoint, changing the Import Filter will not remove it, even if the updated import filters would prevent newer mutations or iterations of the document from getting imported.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the app service linked to the cluster. (UUID)
            appEndpointKeyspace: The name of the App Endpoint and the scope and collection separated by period (.) .
            payload: The new import filter function to be added in the request. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Updating the importFilter in appEndpointKeyspace: {} in "
            "appService: {} in cluster: {} in project: {} in tenant: {}"
            .format(appEndpointKeyspace, appServiceId, clusterId, projectId,
                    organizationId))

        params = payload
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(self.import_filter_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointKeyspace), None, headers, params)
        return resp

    def create_app_endpoint_o_i_d_c_provider(self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """
        Creates an OIDC provider for the specified App Endpoint. The
        OIDC provider is used for OIDC authentication. After you enable OIDC,
        all client requests will use the default OIDC provider,
        unless the OIDC provider for the request is explicitly specified on authentication

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the App Service to create an Endpoint inside. (UUID)
            appEndpointName: the name of the app endpoint. (string)

            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Creating an OIDC Provider for the App endpoint: {},in the "
            "appservice: {}, inside the cluster: {}, for the Project: {} and "
            "Organization: {}".format(appEndpointName, appServiceId,
                                      clusterId, projectId,
                                      organizationId))
        params ={
            "clientId": "foo_client",
            "discoveryUrl": "https://accounts.google.com/.well-known/openid-configuration",
            "issuer": "https://accounts.google.com",
            "register": True,
            "rolesClaim": "roles",
            "userPrefix": "fooOIDC",
            "usernameClaim": "fooAlt"
        }
        for k, v in kwargs.items():
            if k in params:
                params[k] = v

        resp = self.api_post(self.app_endpoint_OIDC_provider.format(
            organizationId, projectId, clusterId, appServiceId, appEndpointName),
            params, headers)
        return resp

    def list_app_endpoint_o_i_d_c_providers(self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """gets the OIDC providers for a particular app endpoint"""
        self.cluster_ops_API_log.info(
            "getting the users for the App endpoint: {},in the "
            "AppService: {}, inside the cluster: {}, for the Project: {} and "
            "Organization: {}".format(appEndpointName, appServiceId,
                                      clusterId, projectId,
                                      organizationId))

        resp = self.api_get(self.app_endpoint_OIDC_provider.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName),headers)
        return resp

    def fetch_oidc_provider_info(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            OIDCProviderID,
            headers=None,
            **kwargs):
        """
        Fetches the details of the given oidc provider

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the App Service to create an Endpoint inside. (UUID)
            appEndpointName: Name of the App Endpoint to fetch details. (string)
            OIDCProviderID: Id of the oidc provider (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching details for the OIDC Provider {} for app Endpoint: {}, "
            "linked to App Svc: {}, inside Cluster: {}, inside Project: {}, inside tenant: {}".format(
                appEndpointName, appServiceId, clusterId, projectId,
                organizationId, OIDCProviderID))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get("{}/{}".format(
            self.app_endpoint_OIDC_provider.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName), OIDCProviderID), params, headers)
        return resp

    def update_app_endpoint_o_i_d_c_provider(self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            oidcProviderId,
            headers=None,
            **kwargs):
        """
        Updates the OIDC provider for the specified App Endpoint.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant app service inside
            it. (UUID)
            appServiceId: ID of the App Service to create an Endpoint inside. (UUID)
            appEndpointName: the name of the app endpoint. (string)

            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Updates the OIDC Provider for the App endpoint: {},in the "
            "appservice: {}, inside the cluster: {}, for the Project: {} and "
            "Organization: {}".format(appEndpointName, appServiceId,
                                      clusterId, projectId,
                                      organizationId))
        params = {
            "clientId": "bar_client",
            "discoveryUrl": "https://accounts.google.com/.well-known/openid-configuration",
            "isDefault": False,
            "issuer": "https://accounts.google.com",
            "providerId": "ffffffff-aaaa-1414-eeee-000000000000",
            "register": True,
            "rolesClaim": "roles",
            "userPrefix": "barOIDC",
            "usernameClaim": "barAlt"
        }
        for k, v in kwargs.items():
            if k in params:
                params[k] = v

        resp = self.api_put("{}/{}".format(
            self.app_endpoint_OIDC_provider.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName),oidcProviderId),params, headers)
        return resp

    def update_app_endpoint_o_i_d_c_default_provider(self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """
        Updates the default OIDC provider for the specified App Endpoint.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant app service inside
            it. (UUID)
            appServiceId: ID of the App Service to create an Endpoint inside. (UUID)
            appEndpointName: the name of the app endpoint. (string)
            providerId: The id of the default provider. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "updates the default OIDC Provider for the App endpoint: {},in the "
            "appservice: {}, inside the cluster: {}, for the Project: {} and "
            "Organization: {}".format(appEndpointName, appServiceId,
                                      clusterId, projectId,
                                      organizationId))
        params = {}
        params["providerId"] = kwargs.get("providerId",
                                          "ffffffff-aaaa-1414-eeee-000000000000")
        if kwargs.get("param"):
            params["param"] = kwargs.get("param")

        resp = self.api_put(self.app_endpoint_OIDC_provider.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName)+"/defaultProvider",
            params, headers)
        return resp

    def delete_app_endpoint_o_i_d_c_provider(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            oidcProviderId,
            headers=None,
            **kwargs):
        """
        Deletes a given Oidc provider for the specified App Endpoint.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the App Service to create an Endpoint inside. (UUID)
            appEndpointName: Name of the App Endpoint to be deleted. (string)
            oidcProviderId: ID of the oidc Provider. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code (ONLY).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Deleting Oidc Provider for app Endpoint: {}, linked to App Svc: "
            "{}, inside Cluster: {}, inside Project: {}, inside tenant: {}".format(
                appEndpointName, appServiceId, clusterId, projectId,
                organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del("{}/{}".format(self.app_endpoint_OIDC_provider.format(
            organizationId, projectId, clusterId, appServiceId,appEndpointName),
            oidcProviderId), params, headers)
        return resp

    def bulk_index_check(
            self,
            organizationId,
            projectId,
            clusterId,
            state,
            indexes,
            headers=None,
            **kwargs):
        """
        Monitor the build status of a list of indexes. It returns the number of indexes in the desired state.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            state: The desired state which the  indexes are expected to be in. (string)
            indexes: The list of indexes to be matched against that state. (list)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching bulk index status for indices: {}, in the cluster: {}, "
            "in the project: {}, in the tenant: {}"
            .format(indexes, clusterId, projectId, organizationId))

        params = {
            "state": state,
            "indexes": indexes
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.bulk_index_check_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def fetch_index_props(
            self,
            organizationId,
            projectId,
            clusterId,
            indexName,
            headers=None,
            **kwargs):
        """
        Get the index properties of a specified index in a keyspace.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            indexName: The name of the index for which the definition has to be fetched. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY.
            Error : message, hint, code, HttpStatusCode
        """
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get("{}/{}".format(
            self.index_endpoint.format(
                organizationId, projectId, clusterId), indexName),
            params, headers)
        return resp

    def index_build_status(
            self,
            organizationId,
            projectId,
            clusterId,
            indexName,
            headers=None,
            **kwargs):
        """
        Monitor the build status of an index.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            indexName: The name of the index for which the definition has to be fetched. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY.
            Error : message, hint, code, HttpStatusCode
        """
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get("{}/{}".format(
            self.index_build_status_endpoint.format(
                organizationId, projectId, clusterId), indexName),
            params, headers)
        return resp

    def list_index_definitions(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        """
        Get definitions for all indices in a keyspace.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY.
            Error : message, hint, code, HttpStatusCode
        """
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.index_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def manage_query_indices(
            self,
            organizationId,
            projectId,
            clusterId,
            definition,
            headers=None,
            **kwargs):
        """
        CREATE/DROP/ALTER/BUILD primary and secondary indexes.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            definition: The query statement for the index to be defined with. (DDL)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY.
            Error : message, hint, code, HttpStatusCode
        """
        params = {
            "definition": definition,
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.index_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def update_app_svc_audit_log_state(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            auditEnabled,
            headers=None,
            **kwargs):
        """
        Enable or disable Audit Logging for an App Service.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the app service linked to the cluster. (UUID)
            auditEnabled: Stop or start audit logging for the app service. (bool)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY.
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Updating audit logging state of app service: {}, linked to the "
            "cluster: {}, inside project: {}, inside tenant: {}"
            .format(appServiceId, clusterId, projectId, organizationId))
        params = {
            "auditEnabled": auditEnabled
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(self.app_svc_audit_log_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            params, headers)
        return resp

    def fetch_app_svc_audit_log_state_info(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            headers=None,
            **kwargs):
        """
        Retrieves the audit logging state for a specific App Service.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the app service linked to the cluster. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching audit logging state of app service: {}, linked to the "
            "cluster: {}, inside project: {}, inside tenant: {}"
            .format(appServiceId, clusterId, projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.app_svc_audit_log_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            params, headers)
        return resp

    def list_app_svc_audit_log_events(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """
        Retrieves all audit log event ids, their descriptions and enabled status for an App Endpoint. The list of filterable event IDs can be specified while configuring audit logging for the App Service.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the app service linked to the cluster. (UUID)
            appEndpointName: name of the endpoint inside the app service. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response (JSON).
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Listing Audit Log Events for the App Endpoint: {}, inside the "
            "app Service: {}, linked to the cluster: {}, inside the project: "
            "{}, inside the tenant: {}".format(appEndpointName, appServiceId,
                                               clusterId, projectId,
                                               organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.app_svc_audit_log_events_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName), params, headers)
        return resp

    def update_app_svc_audit_log_config(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            auditEnabled,
            enabledEventIds,
            disabledUsers,
            disabledRoles,
            headers=None,
            **kwargs):
        """
        Updates the audit logging configuration for a specific App Endpoint. Operations performed by disabled users and roles are excluded from audit logs.
        See a list of event IDs by calling /auditLogEvents, add event IDs to the enabledEventIds field to enable audit logging for those events.

        Args:
            organizationId: The tenant ID for the path. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster which has the app service inside it. (UUID)
            appServiceId: ID of the app service linked to the cluster. (UUID)
            appEndpointName: name of the endpoint inside the app service. (string)
            auditEnabled: Whether to enable audit logs or not. (bool)
            enabledEventIds: IDs of the events for which audit logging is to be enabled. (list)
            disabledUsers: Users which are disabled from being logged no matter the audit logging state. (list)
            disabledRoles: Roles that are excluded from being logged no matter the audit logging config. (list)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Updating audit logging config for app endpoint: {}, inside app "
            "service: {}, linked to the cluster: {}, inside the project: {}, "
            "inside the tenant: {}"
            .format(appEndpointName, appServiceId, clusterId, projectId,
                    organizationId))
        params = {
            "auditEnabled": auditEnabled,
            "enabledEventIds": enabledEventIds,
            "disabledUsers": disabledUsers,
            "disabledRoles": disabledRoles
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(self.app_svc_audit_log_config_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName), params, headers)
        return resp

    def fetch_app_endpoint_audit_log_config_info(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            appEndpointName,
            headers=None,
            **kwargs):
        """
        Retrieves the audit logging configuration for a specific App Endpoint.

        Args:
            organizationId: The tenant in which app service is present. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster having the app service. (UUID)
            appServiceId: ID of the app service for which app service which has the relative app endpoint. (UUID)
            appEndpointName: The name of the App Endpoint for which the config is to be fetched for. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response Body (json)
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching audit log config for app endpoint: {}, inside the app "
            "service: {}, linked to cluster: {}, inside the project: {}, "
            "inside the tenant: {}"
            .format(appEndpointName, appServiceId, clusterId, projectId,
                    organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.app_svc_audit_log_config_endpoint.format(
            organizationId, projectId, clusterId, appServiceId,
            appEndpointName), params, headers)
        return resp

    def patch_app_service_audit_log_streaming(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            op,
            path,
            value,
            headers=None,
            **kwargs):
        """
        Used to pause or resume streaming.
        If log streaming is paused we will retain the collector credentials.

        Args:
            organizationId: The tenant in which app service is present. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster having the app service. (UUID)
            appServiceId: ID of the app service for which app service is being tuned. (UUID)
            op: The operation to be run on the streaming. (string)
            path: The path of the app service streaming. (string)
            value: The value to set for the app service streaming. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Changing streaming config for appService: {}, in the cluster: {},"
            " inside the project: {}, inside the tenant: {}".format(
                appServiceId, clusterId, projectId, organizationId))
        params = {
            "op": op,
            "path": path,
            "value": value
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_patch(self.app_svc_audit_log_streaming_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            params, headers)
        return resp

    def update_app_service_audit_log_streaming(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            streamingEnabled,
            disabledAppEndpoints,
            outputType,
            credentials,
            headers=None,
            **kwargs):
        """
        Sets up audit log streaming for a specific App Service with filters. If streamingEnabled is true log streaming will begin.
        Ensure you have provided collector credentials if you wish to begin streaming; log streaming cannot be enabled without credentials. Refer to schema below to see required fields for your log collection provider. Providers include Datadog, Sumo Logic, and generic HTTP.
        To remove the credentials, disable log streaming by setting streamingEnabled to false and overwrite the credentials with an empty secrets field.
        To start or resume streaming, set streamingEnabled to true. To pause log streaming, set streamingEnabled to false.

        Args:
            organizationId: ID of the tenant. (UUID)
            projectId: ID of the project which contains the cluster. (UUID)
            clusterId: ID of the cluster which has the linked App Service. (UUID)
            appServiceId: ID of the App Service for which streaming has to be configured. (UUID)
            streamingEnabled: Param to stop / start the streaming. (bool)
            disabledAppEndpoints: The App Endpoints inside the App Service which have to be ignored while streaming logs. (list (of strings))
            outputType: The expected audit log output config.
            credentials: The required creds related to the service provider
            to which the Audit Logs are being streamed to. (obj)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Updating audit logs streaming config for App Service: {}, linked "
            "to the cluster: {}, inside the project: {}, inside the tenant: {}"
            .format(appServiceId, clusterId, projectId, organizationId))
        params = {
            "streamingEnabled": streamingEnabled,
            "disabledAppEndpoints": disabledAppEndpoints,
            "outputType": outputType,
            "credentials": credentials
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(self.app_svc_audit_log_streaming_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            params, headers)
        return resp

    def fetch_app_service_audit_log_streaming_info(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            headers=None,
            **kwargs):
        """
        Retrieves the current state of audit log streaming for a specific App Service, as well as the output type and enabled App endpoints.

        Args:
            organizationId: ID of the tenant. (UUID)
            projectId: ID of the project which contains the cluster. (UUID)
            clusterId: ID of the cluster which has the linked App Service. (UUID)
            appServiceId: ID of the App Service for which streaming state has to be fetched. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response Body (json)
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching audit log streaming state for app service: {}, linked to"
            " cluster: {}, inside project: {}, inside tenant: {}".format(
                appServiceId, clusterId, projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.app_svc_audit_log_streaming_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            params, headers)
        return resp

    def create_app_svc_audit_log_export(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            start,
            end,
            headers=None,
            **kwargs):
        """
        For creation of export logs for a specific App Service inside a Cluster.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            appServiceId: ID of the app service for which export logs are to be generated. (UUID)
            start: The start time for the audit logs exports. (%Y-%m-%dT%H:%M:%S)
            end: The end time for the audit logs exports. (%Y-%m-%dT%H:%M:%S)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Creating export logs for App Service: {}, inside the Cluster: {},"
            " inside the Project: {}, inside the Tenant: {}".format(
                appServiceId, clusterId, projectId, organizationId))
        params = {
            "start": start,
            "end": end,
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.app_svc_audit_log_exports_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            params, headers)
        return resp

    def list_app_svc_audit_log_exports(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        """
        For listing export logs for a specific App Service inside a Cluster.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            appServiceId: ID of the app service for which export logs are to be generated. (UUID)
            page: Sets what page you would like to view. (int)
            perPage: Sets how many results you would like to have on each page. (int)
            sortBy: Sets order of how you would like to sort results and also the key you would like to order by ([string])
                Example: sortBy=name
            sortDirection: The order on which the items will be sorted. (str)
                Accepted Values - asc / desc
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and Response Body
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Listing audit log exports for App Service: {}, inside the "
            "Cluster: {}, inside the Project: {}, in the Tenant: {}".format(
                appServiceId, clusterId, projectId, organizationId))
        params = {}
        if page:
            params["page"] = page
        if perPage:
            params["perPage"] = perPage
        if sortBy:
            params["sortBy"] = sortBy
        if sortDirection:
            params["sortDirection"] = sortDirection
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_get(self.app_svc_audit_log_exports_endpoint.format(
            organizationId, projectId, clusterId, appServiceId),
            params, headers)
        return resp

    def fetch_app_svc_audit_log_export_info(
            self,
            organizationId,
            projectId,
            clusterId,
            appServiceId,
            auditLogExportId,
            headers=None,
            **kwargs):
        """
        Fetches the audit log export information for a specific scheduled export based on the exportID linked to the audit log.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the app service is present. (UUID)
            appServiceId: ID of the app service for which export logs are to be generated. (UUID)
            auditLogExportId: The ID of the specific audit log export for which the specifications have to be fetched. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and response
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching specification for the audit log export: {}, linked to "
            "the app service: {}, inside the cluster: {}, inside the "
            "project: {}, inside the tenant: {}".format(
                auditLogExportId, appServiceId, clusterId, projectId,
                organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get("{}/{}".format(
            self.app_svc_audit_log_exports_endpoint.format(
                organizationId, projectId, clusterId, appServiceId),
            auditLogExportId), params, headers)
        return resp

    def flush_bucket(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            headers=None,
            **kwargs):
        """
        A post endpoint used to flush the bucket based on the ID passed,
        PREREQUISITE :- The flush setting on the bucket should be enabled.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: ID of the project inside the tenant. (UUID)
            clusterId: ID of the cluster inside the project in which the bucket is present. (UUID)
            bucketId: ID of the bucket to be flushed. (bucket ID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and Response Body
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Flushing bucket: {}, inside the cluster: {}, "
            "inside the project: {}, inside the tenant: {}"
            .format(bucketId, clusterId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_put(self.flush_buckets_endpoint.format(
            organizationId, projectId, clusterId, bucketId), params, headers)
        return resp

    def list_tenant_events(
            self,
            organizationId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        """
        Returns the List containing all the events happened so far inside a specific tenant.

        Args:
            organizationId: The ID of the tenant to list the events for. (UUID)
            page: Sets what page you would like to view. (int)
            perPage: Sets how many results you would like to have on each page. (int)
            sortBy: Sets order of how you would like to sort results and also the key you would like to order by ([string])
                Example: sortBy=name
            sortDirection: The order on which the items will be sorted. (str)
                Accepted Values - asc / desc
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and Response Body
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Listing events inside the tenant {}".format(organizationId))

        params = {}
        if page:
            params["page"] = page
        if perPage:
            params["perPage"] = perPage
        if sortBy:
            params["sortBy"] = sortBy
        if sortDirection:
            params["sortDirection"] = sortDirection
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_get(self.tenant_events_endpoint.format(
            organizationId), params, headers)
        return resp

    def fetch_tenant_event_info(
            self,
            organizationId,
            eventId,
            headers=None,
            **kwargs):
        """
        Fetches a specific event inside the specified tenant, based on the ID.

        Args:
            organizationId: The ID of the tenant to list the events for. (UUID)
            eventId: The ID of the event to be fetched the info for. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and Response Body
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching information for event {} inside tenant {}".format(
                eventId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get("{}/{}".format(self.tenant_events_endpoint.format(
            organizationId), eventId), params, headers)
        return resp

    def list_project_events(
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
        Lists all the events happened so far inside a specific project in a tenant.

        Args:
            organizationId: The ID of the tenant inside which the project is present. (UUID)
            projectId: The ID of project for which all the events have to be listed. (UUID)
            page: Sets what page you would like to view. (int)
            perPage: Sets how many results you would like to have on each page. (int)
            sortBy: Sets order of how you would like to sort results and also the key you would like to order by ([string])
                Example: sortBy=name
            sortDirection: The order on which the items will be sorted. (str)
                Accepted Values - asc / desc
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and Response Body
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Listing the events inside the project {}, inside the tenant {}"
            .format(projectId, organizationId))

        params = {}
        if page:
            params["page"] = page
        if perPage:
            params["perPage"] = perPage
        if sortBy:
            params["sortBy"] = sortBy
        if sortDirection:
            params["sortDirection"] = sortDirection
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_get(self.project_events_endpoint.format(
            organizationId, projectId), params, headers)
        return resp

    def fetch_project_event_info(
            self,
            organizationId,
            projectId,
            eventId,
            headers=None,
            **kwargs):
        """
        Fetches the information for a specific event inside a project based on the eventID and projectID

        Args:
            organizationId: The tenantID inside which the project is present. (UUID)
            projectId: The projectID for which the tenant has to be fetched. (UUID)
            eventId: The ID of the event to be fetched. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and Response Body
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching info for event {}, inside the project {}, "
            "inside the tenant {}".format(eventId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get("{}/{}".format(self.project_events_endpoint.format(
            organizationId, projectId), eventId), params, headers)
        return resp

    def fetch_network_peer_record_info(
            self,
            organizationId,
            projectId,
            clusterId,
            vpcID,
            headers=None,
            **kwargs):
        """
        Gets the details related to the network peering connection between a capella cluster and the Virtual Private Cloud (within a cloud Provider) that it is peered with.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project having the cluster. (UUID)
            clusterId: The ID of the cluster which has been peered. (UUID)
            vpcID: The ID of the Virtual Private Cloud. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code and Response Body
            Error : message, hint, code, HttpStatusCode
        """
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get("{}/{}".format(self.vpc_endpoint.format(
            organizationId, projectId, clusterId), vpcID), params, headers)
        return resp

    def create_network_peer(
            self,
            organizationId,
            projectId,
            clusterId,
            name,
            pConf,
            pType,
            headers=None,
            **kwargs):
        """
        Creates a peering connection between the capella cluster and the VPC on the cloud provider.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project having the cluster. (UUID)
            clusterId: The ID of the cluster which to be peered. (UUID)
            name: Name of the VPC Peer connection
            pConf: Provider configuration. (object)
                AWSConfig: Configuration of the cloud being peered with capella cluster. The inner params are based on the key of this object, ie, the cloud provider specifically. (obj)
                    "accountId": User Account related to the cloud Provider. (string)
                    "cidr": Network IP / Subnet IP. (IP)
                    region: Keyword. (string)
                    vpcId: (string)
                providerId: ID of the connection establishment fetched from the Provider (string)
            pType: Provider type. (string) [gcp, aws, azure]
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        params = {
            "name": name,
            "providerType": pType,
            "providerConfig": pConf
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.vpc_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def delete_network_peer(
            self,
            organizationId,
            projectId,
            clusterId,
            vpcID,
            headers=None,
            **kwargs):
        """
        Deletes the peering connection between the capella cluster and the VPC on the cloud provider.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project having the cluster. (UUID)
            clusterId: The ID of the cluster which has been peered. (UUID)
            vpcID: The ID of the Virtual Private Cloud. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del("{}/{}".format(self.vpc_endpoint.format(
            organizationId, projectId, clusterId), vpcID), params, headers)
        return resp

    def list_network_peer_records(
            self,
            organizationId,
            projectId,
            clusterId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        """
        Lists all the peering connections between the capella cluster and any of the multiple VPCs on same/multiple cloud providers.

        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project having the cluster. (UUID)
            clusterId: The ID of the cluster which has-been/has-to-be peered. (UUID)
            page: Sets what page you would like to view. (int)
            perPage: Sets how many results you would like to have on each page. (int)
            sortBy: Sets order of how you would like to sort results and also the key you would like to order by ([string])
                Example: sortBy=name
            sortDirection: The order on which the items will be sorted. (str)
                Accepted Values - asc / desc
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code, dict
            Error : message, hint, code, HttpStatusCode
        """
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

        resp = self.api_get(self.vpc_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def get_azure_vnet_peering_command(
            self,
            organizationId,
            projectId,
            clusterId,
            tenantId,
            subscriptionId,
            resourceGroup,
            vnetId,
            vnetPeeringServicePrincipal,
            headers=None,
            **kwargs):
        """
        Retrieves the role assignment command or script to be executed in the Azure CLI to assign a new network contributor role.
        It scopes only to the specified subscription and the virtual network within that subscription
        Args:
            organizationId: The ID of the tenant. (UUID)
            projectId: The ID of the project having the cluster. (UUID)
            clusterId: The ID of the Azure cluster for which to get the peering command. (UUID)
            tenantId: The ID of the Azure tenant. (UUID)
            subscriptionId: The ID of the Azure subscription. (UUID)
            resourceGroup: Name of the resource group where the VPC is created. (string)
            vnetId: The vnet ID for which to generate peering command. (string)
            vnetPeeringServicePrincipal: The ID of the vnet service principal created when peering access is allowed through the UI. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)
        Returns:
            Success : Status Code, dict
            Error : message, hint, code, HttpStatusCode
        """

        params = {
            "tenantId": tenantId,
            "subscriptionId": subscriptionId,
            "resourceGroup": resourceGroup,
            "vnetId": vnetId,
            "vnetPeeringServicePrincipal": vnetPeeringServicePrincipal
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.vnet_peering_cmd_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def accept_private_endpoint(
            self,
            organizationId,
            projectId,
            clusterId,
            endpointId,
            headers=None,
            **kwargs):
        """
        Accepts a new private endpoint connection request so that it is associated with the endpoint service. This means the private endpoint is available for use.

        Args:
            organizationId: ID of the tenant. (UUID)
            projectId: ID of the project. (UUID)
            clusterId: ID of the capella cluster to be peered. (UUID)
            endpointId: ID of the peering endpoint. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Accepting private endpoint request for {}, inside cluster {}, "
            "inside project {}, inside tenant {}.".format(
                endpointId, clusterId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_post(self.associate_private_network_endpoint.format(
            organizationId, projectId, clusterId, endpointId), params, headers)
        return resp

    def delete_private_endpoint(
            self,
            organizationId,
            projectId,
            clusterId,
            endpointId,
            headers=None,
            **kwargs):
        """
        Removes the private endpoint associated with the endpoint service. This means the private endpoint is no longer able to connect to the private endpoint service.

        Args:
            organizationId: ID of the tenant. (UUID)
            projectId: ID of the project. (UUID)
            clusterId: ID of the capella cluster. (UUID)
            endpointId: endpoint for which the Service has to be removed. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Removing the private endpoint for {}, inside cluster {}, "
            "inside project {}, inside tenant".format(
                endpointId, clusterId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_post(self.unassociate_private_network_endpoint.format(
            organizationId, projectId, clusterId, endpointId), params, headers)
        return resp

    def disable_private_endpoint_service(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        """
        Disables the Private Endpoint service for a capella cluster.

        Args:
            organizationId: ID of the tenant. (UUID)
            projectId: ID of the project. (UUID)
            clusterId: ID of the capella cluster for which private endpoints have to be disabled. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Disabling Private Endpoint Service for cluster {}, in project {},"
            " in tenant {}.".format(clusterId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del(self.private_network_service_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def enable_private_endpoint_service(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        """
        Enables the Private Endpoint Service for a Capella Cluster.

        Args:
            organizationId: ID of the tenant. (UUID)
            projectId: ID of the project. (UUID)
            clusterId: ID of the capella cluster for which private endpoints have to be disabled. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
         """
        self.cluster_ops_API_log.info(
            "Enabling Private endpoint service on cluster {}, in project {}, "
            "in tenant {}".format(clusterId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = {}

        resp = self.api_post(self.private_network_service_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def fetch_private_endpoint_service_status_info(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        """
        Determines if the endpoint service is enabled or disabled on your cluster.

        Args:
            organizationId: ID of the tenant. (UUID)
            projectId: ID of the project. (UUID)
            clusterId: ID of the tenant. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code ONLY
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Fetching Private Endpoint info of cluster {}, in project {}, "
            "in tenant {}".format(clusterId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(self.private_network_service_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def list_private_endpoint(
            self,
            organizationId,
            projectId,
            clusterId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        """
        Returns a list of private endpoints associated with the endpoint service for your Capella cluster, along with the endpoint state. Each private endpoint connects a private network to the Capella cluster.

        Args:
            organizationId: ID of the tenant. (UUID)
            projectId: ID of the project. (UUID)
            clusterId: ID of the capella cluster which has the endpoint service and m multiple private endpoints associated with it. (UUID)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)
            page: Sets what page you would like to view. (int)
            perPage: Sets how many results you would like to have on each page. (int)
            sortBy: Sets order of how you would like to sort results and also the key you would like to order by ([string])
                Example: sortBy=name
            sortDirection: The order on which the items will be sorted. (str)
                Accepted Values - asc / desc
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code, dict
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "Listing all the private endpoints linked to the endpoint "
            "service for cluster {}, in project {}, in tenant {}".format(
                clusterId, projectId, organizationId))

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

        resp = self.api_get(self.list_private_networks_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    def post_private_endpoint_command(
            self,
            organizationId,
            projectId,
            clusterId,
            payload,
            headers=None,
            **kwargs):
        """
        Retrieves the command or script to be executed in order to create the private endpoint which will provides a private connection between the specified VPC and the specified Capella private endpoint service.

        Args:
            organizationId: ID of the tenant. (UUID)
            projectId: ID of the project. (UUID)
            clusterId: ID of the capella cluster having private endpoint service. (UUID)
            payload: Private Network command payload, specific to the CSP. (string)
            headers: Headers to be sent with the API call. (dict)
            **kwargs: Do not use this under normal circumstances. This is only to test negative scenarios. (dict)

        Returns:
            Success : Status Code, (list)
            Error : message, hint, code, HttpStatusCode
        """
        self.cluster_ops_API_log.info(
            "getting command for the subnets inside vpc for cluster {}, "
            "inside project {}, inside tenant {}".format(
                clusterId, projectId, organizationId))

        params = payload
        for k, v in kwargs:
            params[k] = v

        resp = self.api_post(self.private_network_command_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Method to restore the backup with backupId under cluster, project and organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    - Project Manager
    - Project Viewer
    - Database Data Reader/Writer
    - Database Data Reader
    :param organizationId (str) Organization ID under which the backup has to be created.
    :param projectId (str) Project ID under which the backup has to be created.
    :param targetClusterID (str) The ID of the target cluster to restore to.
    :param sourceClusterID (str) The ID of the source cluster the restore is based on.
    :param backupID (str) The backup record ID that contains the backup to restore from.
    :param services (str) Items Enum: "data" "query"
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def restore_backup(
            self,
            organizationId,
            projectId,
            targetClusterID,
            sourceClusterID,
            backupID,
            services,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Restore Backup in project {} in organization {}".format(
                projectId, organizationId))
        params = {
            "targetClusterID": targetClusterID,
            "sourceClusterID": sourceClusterID,
            "backupID": backupID,
            "services": services,
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(
            self.backups_endpoint.format(
                organizationId, projectId,
                sourceClusterID) + '/' + backupID + '/restore', params,
            headers)
        return resp

    """
    Method to delete the backup with backupId under cluster, project and organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    :param organizationId (str) Organization ID under which the backup has to be created.
    :param projectId (str) Project ID under which the backup has to be created.
    :param clusterId (str) Cluster ID under which the backup has to be created.
    :param backupId (str) Backup ID which the backup has to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_backup(
            self,
            organizationId,
            projectId,
            clusterId,
            backupId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Delete Backup in project {} in organization {}".format(
                projectId, organizationId))
        params = {}
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_del(
            self.backups_endpoint.format(
                organizationId, projectId, clusterId) + '/' + backupId, params,
            headers)
        return resp

    """
    Method to get the backup under cluster, project and organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    :param organizationId (str) Organization ID under which the backup has to be created.
    :param projectId (str) Project ID under which the backup has to be created.
    :param clusterId (str) Cluster ID under which the backup has to be created.
    :param backupId (str) Backup ID which the backup has to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def get_backup(
            self,
            organizationId,
            projectId,
            clusterId,
            backupId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Get Backup in project {} in organization {}".format(
                projectId, organizationId))
        params = {}
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_get(
            self.backups_endpoint.format(
                organizationId, projectId, clusterId) + '/' + backupId, params,
            headers)
        return resp

    """
    Method to get list all the backups under cluster, project and organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    :param organizationId (str) Organization ID under which the backup has to be created.
    :param projectId (str) Project ID under which the backup has to be created.
    :param clusterId (str) Cluster ID under which the backup has to be created.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_backups(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "List Backup in project {} in organization {}".format(
                projectId, organizationId))
        params = {}
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_get(
            self.backups_endpoint.format(
                organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Method creates a backup under bucket, cluster, project and organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    :param organizationId (str) Organization ID under which the backup has to be created.
    :param projectId (str) Project ID under which the backup has to be created.
    :param clusterId (str) Cluster ID under which the backup has to be created.
    :param bucketId (str) Bucket ID under which the backup has to be created.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_backup(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Creating Backup in project {} in organization {}".format(
                projectId, organizationId))
        params = {}
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            self.backups_endpoint.format(
                organizationId, projectId,
                "{}/buckets/{}".format(clusterId, bucketId)), params, headers)
        return resp

    """
    Method creates a cluster under project and organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    - Project Manager
    :param organizationId (str) Organization ID under which the cluster has to be created.
    :param projectId (str) Project ID under which the cluster has to be created.
    :param name (str) Name of the cluster to be created. Max length 256 characters.
    :param description (str) Description of the cluster. Optional. Max length 1024 characters.
    :param cloudProvider (object) The cloud provider where the cluster will be hosted.
    {
        :param type (str) Cloud provider type, either 'aws', 'gcp', or 'azure'.
        :param region (str) Cloud provider region
        :param cidr (str) CIDR block for Cloud Provider.
    }
    :param couchbaseServer (object)
    {
        :param version(str) Version of the Couchbase Server to be installed in the cluster, should be greater than 7.1.
    }
    :param serviceGroups ([object])
    [{
        :param node (object)
        {
            :param compute (object)
            {
                :param cpu (int) CPU units (cores).
                :param ram (int) RAM units (GB).
            }
            :param disk (object)
            {
                :param storage (int) >=50. Storage in GB.
                :param type (str) Type of disk
                    AWS - "gp3", "io2"
                    GCP - "pd-ssd"
                    azure - "p6" "p10" "p15" "p20" "p30" "p40" "p50" "p60" "ultra"
                :param iops (int) For AWS and Azure only.
                :param autoExpansion (bool) Auto-expansion option. Only supported for AWS and GCP.
            }
        }
        :param numOfNodes (int) Number of nodes. Min value - 3 Max Value - 27
        :param services ([object])
        [{
            :param type (str) Enum: "query" "index" "data" "search" "analytics" "eventing"
        }]
    }]
    :param availability (object)
    {
        :param type (str) Availability zone type, either 'single' or 'multi'.
    }
    :param trial (bool) Specify if the cluster is for a trial or not. True for trial cluster.
    :param support (object)
    {
        :param plan (str) Plan type, either "basic" "developer pro" "enterprise"
        :param timezone (str) The standard timezone for the cluster. Should be the TZ identifier.
        Enum: "ET" "GMT" "IST" "PT"
    }
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_cluster(
            self,
            organizationId,
            projectId,
            name,
            cloudProvider,
            couchbaseServer=None,
            serviceGroups=None,
            availability=None,
            support=None,
            description="",
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Creating Cluster {} in project {} in organization {}".format(
                name, projectId, organizationId))
        params = {
            "name": name,
            "cloudProvider": cloudProvider
        }
        if couchbaseServer:
            params["couchbaseServer"] = couchbaseServer
        if serviceGroups:
            params["serviceGroups"] = serviceGroups
        if availability:
            params["availability"] = availability
        if support:
            params["support"] = support
        if description:
            params["description"] = description

        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            self.cluster_endpoint.format(
                organizationId, projectId), params, headers)
        return resp

    """
    Method fetches all the clusters under a project.
    Returned set of clusters is reduced to what the caller has access to view.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
        Database Data Reader/Writer
        Database Data Reader
    :param organizationId (str) Organization ID for which the cluster have to be listed.
    :param projectId (str) Project ID for which the cluster has to be listed.
    :param page (int) Sets what page you would like to view
    :param perPage (int) Sets how many results you would like to have on each page
    :param sortBy ([string]) Sets order of how you would like to sort results and also the key you would like to order by
                             Example: sortBy=name
    :param sortDirection (str) The order on which the items will be sorted. Accepted Values - asc / desc
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_clusters(
            self,
            organizationId,
            projectId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "List all the cluster for project {} in organization {}".format(
                projectId, organizationId))
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
            self.cluster_endpoint.format(
                organizationId, projectId), params, headers)
        return resp

    """
    Method fetches info of the required cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
        Database Data Reader/Writer
        Database Data Reader
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster whose info has to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_cluster_info(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Fetching cluster info for {} in project {} in organization {}".format(
                clusterId, projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            "{}/{}".format(
                self.cluster_endpoint.format(
                    organizationId,
                    projectId),
                clusterId),
            params,
            headers)
        return resp

    """
    Method to update cluster config.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster whose config has to be updated.
    :param name (str) Name of the cluster to be created. Max length 256 characters.
    :param description (str) Description of the cluster. Optional. Max length 1024 characters.
    :param support (object)
    {
        :param plan (str) Plan type, either "basic" "developer pro" "enterprise"
        :param timezone (str) The standard timezone for the cluster. Should be the TZ identifier.
        Enum: "ET" "GMT" "IST" "PT"
    }
    :param serviceGroups ([object])
    [{
        :param node (object)
        {
            :param compute (object)
            {
                :param cpu (int) CPU units (cores).
                :param ram (int) RAM units (GB).
            }
            :param disk (object)
            {
                :param storage (int) >=50. Storage in GB.
                :param type (str) Type of disk
                    AWS - "gp3", "io2"
                    GCP - "pd-ssd"
                    azure - "p6" "p10" "p15" "p20" "p30" "p40" "p50" "p60" "ultra"
                :param iops (int) For AWS and Azure only.
                :param autoExpansion (bool) Auto-expansion option. Only supported for AWS and GCP.
            }
        }
        :param numOfNodes (int) Number of nodes. Min value - 3 Max Value - 27
        :param services ([object])
        [{
            :param type (str) Enum: "query" "index" "data" "search" "analytics" "eventing"
        }]
    }]
    :param ifmatch (bool) Is set to true then it uses a precondition header that specifies the entity tag of a resource.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def update_cluster(
            self,
            organizationId,
            projectId,
            clusterId,
            name,
            description,
            support,
            serviceGroups,
            ifmatch,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Updating cluster {} in project {} in organization {}".format(
                clusterId, projectId, organizationId))
        params = {
            "name": name,
            "description": description,
            "support": support,
            "serviceGroups": serviceGroups
        }
        if ifmatch:
            if not headers:
                headers = {}
            result = self.fetch_cluster_info(
                organizationId, projectId, clusterId)
            version_id = result.json()["audit"]["version"]
            headers["If-Match"] = "Version: {}".format(version_id)

        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(
            "{}/{}".format(
                self.cluster_endpoint.format(
                    organizationId,
                    projectId),
                clusterId),
            params,
            headers)
        return resp

    """
    Method deletes the required cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster which has to be deleted.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_cluster(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Deleting cluster {} in project {} in organization {}".format(
                clusterId, projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            "{}/{}".format(
                self.cluster_endpoint.format(
                    organizationId,
                    projectId),
                clusterId),
            params,
            headers)
        return resp

    """
    Switches on the cluster.

    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster which has to be switched on.
    :param turnOnLinkedAppService (bool) To turn on the related App Services inside the cluster as well or not
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def switch_cluster_on(self, organizationId, projectId, clusterId,
                          turnOnLinkedAppService, headers=None, **kwargs):
        self.cluster_ops_API_log.info(
            "Switching on Cluster {} in project {} in organization {}".format(
                clusterId, projectId, organizationId))

        params = {
            "turnOnLinkedAppService": turnOnLinkedAppService,
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            self.cluster_on_off_endpoint.format(
                organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Switches off the cluster.
    Turning off your database turns off the compute for your cluster but the storage remains.
    All of the data, schema (buckets, scopes, and collections), and indexes remain, as well as cluster configuration, including users and allow lists.

    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster which has to be switched off.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def switch_cluster_off(self, organizationId, projectId, clusterId,
                           headers=None, **kwargs):
        self.cluster_ops_API_log.info(
            "Switching off Cluster {} in project {} in organization {}".format(
                clusterId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            self.cluster_on_off_endpoint.format(
                organizationId, projectId, clusterId), params, headers)
        return resp

    """
    This provides the means to add a new cluster On/Off schedule. Based on this the cluster is turned on or off for the whole week based on the specified day

    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager

    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) ID of the cluster which has to be scheduled.
    :param timezone (str) Timezone for the schedule
    :param days (list) [
        :object {
            :param state (str) The scheduled state for the cluster
            :param day (str) The scheduled day for that state
            :param from (object) {
                :param hour (int)
                :param minute (int)
            }
            :param to (object) {
                :param hour (int)
                :param minute (int)
            }
        }
    ]
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_cluster_on_off_schedule(
            self,
            organizationId,
            projectId,
            clusterId,
            timezone,
            days,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info("Adding on/off schedule in cluster {} "
                                      .format(clusterId))
        params = {
            "timezone": timezone,
            "days": days,
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            self.cluster_on_off_schedule_endpoint.format(
                organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Fetches the details of the On/Off schedule for the given cluster.

    In order to access this endpoint, the provided API key must have at least one of the following roles:
        Organization Owner
        Project Owner
        Project Manager

    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) ID of the cluster which has to be scheduled.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_cluster_on_off_schedule(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info("Fetching on/off schedule in cluster {}"
                                      .format(clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            self.cluster_on_off_schedule_endpoint.format(
                organizationId, projectId, clusterId), params, headers)
        return resp

    """
    This provides the means to update an existing cluster On/Off schedule.

    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager

    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) ID of the cluster which has to be scheduled.
    :param timezone (str) Timezone for the schedule
    :param days (list) [
        :object {
            :param state (str) The scheduled state for the cluster
            :param day (str) The scheduled day for that state
            :param from (object) {
                :param hour (int)
                :param minute (int)
            }
            :param to (object) {
                :param hour (int)
                :param minute (int)
            }
        }
    ]
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def update_cluster_on_off_schedule(
            self,
            organizationId,
            projectId,
            clusterId,
            timezone,
            days,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info("Updating on/off schedule in cluster {}"
                                      .format(clusterId))
        params = {
            "timezone": timezone,
            "days": days,
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(
            self.cluster_on_off_schedule_endpoint.format(
                organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Fetches the details of the On/Off schedule for the given cluster.

    In order to access this endpoint, the provided API key must have at least one of the following roles:
        Organization Owner
        Project Owner
        Project Manager

    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) ID of the cluster which has to be scheduled.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_cluster_on_off_schedule(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info("Deleting on/off schedule in cluster {}"
                                      .format(clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            self.cluster_on_off_schedule_endpoint.format(
                organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Method migrates the specified buckets from couchstore -> magma over Capella.
    :param organizationId (str) Organization ID under which the buckets are present.
    :param projectId (str) Project ID under which the buckets are present.
    :param clusterId (str) Cluster ID under which the buckets are present.
    :param buckets (list)
        :param (str) Bucket name
    :param headers (dict) Headers to be sent with the API call. (NOTE THAT THIS PARAM IS DIFFERENT TO THE HEADER PARAM BEING SENT IN THE BODY OF THE ALERT IN THE CONFIG OBJECT)
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def update_bucket_storage_migration(
            self,
            organizationId,
            projectId,
            clusterId,
            buckets=[],
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Migrating buckets `{}` in cluster {} in project {} in organization {}.".format(
                buckets, clusterId, projectId, organizationId))
        params = {
            "buckets": buckets,
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_put(
            self.bucket_migration_endpoint.format(organizationId, projectId,
                                                  clusterId), params, headers)
        return resp

    """
    Method creates an alert inside a project.
    :param organizationId (str) Organization ID under which the alert is present.
    :param projectId (str) Project ID under which the alert is present.
    :param kind (str) Type of alert integration, currently only supports the type "webhook".
    :param name (str) Name to be added by user about the alert integration. [optional]
    :param config (obj) Configuration details of the alert integration, currently only contains the object webhook.
        :param method (str) Type of Rest API to be send to the user for the alert notification. (POST or PUT)
        :param url ($url) The URL of the customer to which the alert notification API call must be sent.
        :param headers (obj) HTTP headers to be present in the alert API call to the customer. [optional]
            :param headerValue (str) key value pair of the headers to be present in the API call
        :param webhook (obj)
            :param token (str) Authorisation header token to be used in the POST/PUT API alert send to the customer though the webhook integration.
            :param basicAuth (obj) Authorisation header username and password to be used in the POST/PUT API alert send to the customer though the webhook integration.
                :param userId (str)
                :param password (str)
            :param exclude (obj) Contains 2 arrays named appServices and clusters to list what appServices and clusters to not send alerts about. [Optional]
                :param appServices (list) The appServices that the alert shall ignore
                    :param appServiceId (UUID) All the IDs to be excluded by the alert
                :param clusters (list) The clusters that the alert shall ignore
                    :param clusterID (UUID) All the IDs to be excluded by the alert
    :param headers (dict) Headers to be sent with the API call. (NOTE THAT THIS PARAM IS DIFFERENT TO THE HEADER PARAM BEING SENT IN THE BODY OF THE ALERT IN THE CONFIG OBJECT)
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.

    NOTES:
    Either token or basicAuth is required. * Not both! *
    Headers are optional HTTP headers that can be added (support for up to 20).
    The method can be one of POST or PUT
    The url must be HTTPS
    """

    def create_alert(
            self,
            organizationId,
            projectId,
            kind,
            config,
            name=None,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Creating an alert inside the project {} inside the organization {}.".format(
                projectId, organizationId))

        params = {
            "kind": kind,
            "config": config,
        }
        if name:
            params["name"] = name
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(self.alerts_endpoint.format(
            organizationId, projectId),
            params, headers)
        return resp

    """
    Method fetches an alert's information, configuration and state.
    :param organizationId (str) Organization ID under which the alert is present.
    :param projectId (str) Project ID under which the alert is present.
    :param alertId (str) ID of the alert to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_alert_info(
            self,
            organizationId,
            projectId,
            alertId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Fetching the alert {} inside the project {} inside the organization {}.".format(
                alertId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get("{}/{}".format(self.alerts_endpoint.format(
            organizationId, projectId), alertId),
            params, headers)
        return resp

    """
    Method lists all alerts inside an organization.
    :param organizationId (str) Organization ID under which the alert is present.
    :param projectId (str) Project ID under which the alert is present.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_alerts(
            self,
            organizationId,
            projectId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "List alert inside project {} the organization {}.".format(
                projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(self.alerts_endpoint.format(
            organizationId, projectId),
            params, headers)
        return resp

    """
    Method deletes an alert inside a project.
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the alert is present.
    :param alertId (str) ID of the alert to be deleted.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_alert(
            self,
            organizationId,
            projectId,
            alertId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Deleting an alert inside the project {} inside the organization {}.".format(
                projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del("{}/{}".format(self.alerts_endpoint.format(
            organizationId, projectId), alertId),
            params, headers)
        return resp

    """
    Method updates an alert inside a project.
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param alertId (str) ID of the alert to be updated.
    :param kind (str) Type of alert integration, currently only supports the type "webhook".
    :param name (str) Name to be added by user about the alert integration. [optional]
    :param config (obj) Configuration details of the alert integration, currently only contains the object webhook.
        :param method (str) Type of Rest API to be send to the user for the alert notification. (POST or PUT)
        :param url ($url) The URL of the customer to which the alert notification API call must be sent.
        :param headers (obj) HTTP headers to be present in the alert API call to the customer. [optional]
            :param headerValue (str) key value pair of the headers to be present in the API call
        :param webhook (obj)
            :param token (str) Authorisation header token to be used in the POST/PUT API alert send to the customer though the webhook integration.
            :param basicAuth (obj) Authorisation header username and password to be used in the POST/PUT API alert send to the customer though the webhook integration.
                :param userId (str)
                :param password (str)
            :param exclude (obj) Contains 2 arrays named appServices and clusters to list what appServices and clusters to not send alerts about. [Optional]
                :param appServices (list) The appServices that the alert shall ignore
                    :param appServiceId (UUID) All the IDs to be excluded by the alert
                :param clusters (list) The clusters that the alert shall ignore
                    :param clusterID (UUID) All the IDs to be excluded by the alert
    :param headers (dict) Headers to be sent with the API call. (NOTE THAT THIS PARAM IS DIFFERENT TO THE HEADER PARAM BEING SENT IN THE BODY OF THE ALERT IN THE CONFIG OBJECT)
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.

    NOTES:
    Either token or basicAuth is required. * Not both! *
    Headers are optional HTTP headers that can be added (support for up to 20).
    The method can be one of POST or PUT
    The url must be HTTPS
    """

    def update_alert(
            self,
            organizationId,
            projectId,
            alert_id,
            kind,
            config,
            name=None,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Updating the alert {} inside the project {} inside the organization {}.".format(
                alert_id, projectId, organizationId))

        params = {
            "kind": kind,
            "config": config,
        }
        if name:
            params["name"] = name
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_put("{}/{}".format(self.alerts_endpoint.format(
            organizationId, projectId), alert_id),
            params, headers)
        return resp

    """
    Method tests all alerts inside an organization.
    :param organizationId (str) Organization ID under which the alert is present.
    :param projectId (str) Project ID under which the alert is present.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def test_alert(
            self,
            organizationId,
            projectId,
            config,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Test alert inside project {} the organization {}.".format(
                projectId, organizationId))

        params = {
            "config": config,
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(self.test_alert_endpoint.format(
            organizationId, projectId),
            params, headers)
        return resp

    """
    Updates the audit log configuration for the cluster.
    In order to access this endpoint, the provided API key must have at least one of the following roles:
        Organization Owner
        Project Owner
        Project Manager

    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID for which the audit log is being created.
    :param auditEnabled (bool)
    :param disabledUsers (list)
        :param (obj)
            :param domain (str)
            :param name (str)
    :param enabledEventIDs (list)
        :param eventId (int)
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def update_audit_log(
            self,
            organizationId,
            projectId,
            clusterId,
            auditEnabled,
            disabledUsers,
            enabledEventIDs,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Creating Audit Log inside cluster {} inside project {} inside organization {}".format(
                clusterId, projectId, organizationId))

        params = {
            "auditEnabled": auditEnabled,
            "disabledUsers": disabledUsers,
            "enabledEventIDs": enabledEventIDs
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_put(self.audit_log_endpoint.format(
            organizationId, projectId, clusterId),
            params, headers)
        return resp

    """
    Fetches information on whether audit logging is enabled, and which event IDs are enabled.
    To learn more about cluster audit logs, please refer to audit management.
    In order to access this endpoint, the provided API key must have at least one of the following roles :
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
        Database Data Reader/Writer
        Database Data Reader

    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID for which the audit log is requested.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_audit_log_info(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Fetching Audit Logging inside cluster {} inside project {} inside organization {}".format(
                clusterId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(self.audit_log_endpoint.format(
            organizationId, projectId, clusterId),
            params, headers)
        return resp

    """
    Retrieves a list of audit event IDs. The list of filterable event IDs can be specified while configuring audit log for cluster.
    In order to access this endpoint, the provided API key must have at least one of the following roles :
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
        Database Data Reader/Writer
        Database Data Reader

    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID for which the audit log events are to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_audit_log_event_info(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Fetching Audit Log Events info inside cluster {} inside project {} inside organization {}".format(
                clusterId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(self.audit_log_events_endpoint.format(
            organizationId, projectId, clusterId),
            params, headers)
        return resp

    """
    Creates a new audit log export job.
    Audit Logs for the last 30 days can be requested, otherwise they are purged. A pre-signed URL to a s3 bucket location is returned, which is used to download these audit logs.
    In order to access this endpoint, the provided API key must have at least one of the following roles:
        Organization Owner
        Project Owner
        Project Manager

    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID for which the audit log is being created.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_audit_log_export(
            self,
            organizationId,
            projectId,
            clusterId,
            start,
            end,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Creating Audit Log inside cluster {} inside project {} inside organization {}".format(
                clusterId, projectId, organizationId))

        params = {
            "start": start,
            "end": end
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(self.audit_log_exports_endpoint.format(
            organizationId, projectId, clusterId),
            params, headers)
        return resp

    """
    Fetches the status of a single audit log export job.
    It will show the pre-signed URL if the export was successful, a failure error if it was unsuccessful or a message saying no audit logs available if there were no audit logs found during the given timeframe.
    In order to access this endpoint, the provided API key must have at least one of the following roles:
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
        Database Data Reader/Writer
        Database Data Reader

    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID for which the audit log is requested.
    :param auditLogId (str) The ID of the audit log which is being fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_audit_log_export_info(
            self,
            organizationId,
            projectId,
            clusterId,
            auditLogId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Fetching Audit Log {} inside cluster {} inside project {} inside organization {}".format(
                auditLogId, clusterId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            "{}/{}".format(self.audit_log_exports_endpoint.format(
                organizationId, projectId, clusterId), auditLogId),
            params, headers)
        return resp

    """
    Fetches the status of a all audit log export jobs inside a cluster.
    It will show the pre-signed URL if the export was successful, a failure error if it was unsuccessful or a message saying no audit logs available if there were no audit logs found during the given timeframe.
    In order to access this endpoint, the provided API key must have at least one of the following roles:
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
        Database Data Reader/Writer
        Database Data Reader

    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID for which the audit log is requested.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_audit_log_exports(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Listing Audit Logs inside cluster {} inside project {} inside organization {}".format(
                clusterId, projectId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(self.audit_log_exports_endpoint.format(
            organizationId, projectId, clusterId),
            params, headers)
        return resp

    """
    Method downloads the cluster certificate
    In order to access this endpoint, the provided API key must have at least one of the following
    roles:
         Organization Owner
         Project Owner
    Couchbase Capella supports the use of x.509 certificates, for clients and servers. This
    ensures that only approved users, applications, machines, and endpoints have access to system
    resources.
    Consequently, the mechanism can be used by Couchbase SDK clients to access Couchbase Services,
    and by source clusters that use XDCR to replicate data to target clusters. Clients can verify
    the identity of Couchbase Capella, thereby ensuring that they are not exchanging data with a
    rogue entity.
    Get Certificate
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster which has to be deleted.
    """

    def get_cluster_certificate(self, organization_id, project_id, cluster_id,
                                headers=None,
                                **kwargs):
        self.cluster_ops_API_log.info(
            "Downloading certificate for cluster {} in project {} in organization {}".format(
                cluster_id, project_id, organization_id))
        if kwargs:
            params = kwargs
        else:
            params = None
        api_response = self.api_get('{}/{}/certificates'.format(
            self.cluster_endpoint.format(organization_id, project_id),
            cluster_id),
            params=params, headers=headers)
        return api_response

    """
    Method adds a CIDR to allowed CIDRs list of the specified cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster to which CIDR has to be added.
    :param cidr (str) The trusted CIDR to allow connections from.
    :param comment (str) A short description about the allowed CIDR.
    :param expiresAt (str) An RFC3339 timestamp determining when the allowed CIDR should expire.
    If this field is empty/omitted then the allowed CIDR is permanent and will never automatically expire.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def add_CIDR_to_allowed_CIDRs_list(
            self,
            organizationId,
            projectId,
            clusterId,
            cidr,
            comment="",
            expiresAt="",
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Adding {} CIDR block to {} cluster allowed CIDR list".format(
                cidr, clusterId))
        params = {
            "cidr": cidr
        }
        if comment:
            params["comment"] = comment
        if expiresAt:
            params["expiresAt"] = expiresAt
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(self.allowedCIDR_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Method fetches all the allowed CIDRs for a given cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster for which the allowed CIDRs list is to be fetched.
    :param page (int) Sets what page you would like to view
    :param perPage (int) Sets how many results you would like to have on each page
    :param sortBy ([string]) Sets order of how you would like to sort results and also the key you would like to order by
                             Example: sortBy=name
    :param sortDirection (str) The order on which the items will be sorted. Accepted Values - asc / desc
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_allowed_CIDRs(
            self,
            organizationId,
            projectId,
            clusterId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "List all the allowed CIDRs for cluster {}".format(clusterId))
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

        resp = self.api_get(self.allowedCIDR_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Method fetches info of the required allowed CIDR ID.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the allowed CIDR ID is present.
    :param allowedCidrId (str) The GUID4 ID of the allowed CIDR.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_allowed_CIDR_info(
            self,
            organizationId,
            projectId,
            clusterId,
            allowedCidrId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Fetching allowed CIDR info for {} in cluster {}".format(
                allowedCidrId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            "{}/{}".format(
                self.allowedCIDR_endpoint.format(
                    organizationId,
                    projectId,
                    clusterId),
                allowedCidrId),
            params,
            headers)
        return resp

    """
    Method deletes specified CIDR ID from allowed CIDR list of the cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the allowed CIDR ID is present.
    :param allowedCidrId (str) The GUID4 ID of the allowed CIDR which is to be deleted.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_allowed_CIDR(
            self,
            organizationId,
            projectId,
            clusterId,
            allowedCidrId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Deleting allowed CIDR {} from cluster {}".format(
                allowedCidrId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            "{}/{}".format(
                self.allowedCIDR_endpoint.format(
                    organizationId,
                    projectId,
                    clusterId),
                allowedCidrId),
            params,
            headers)
        return resp

    """
    Method creates a new database user for a cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster for which the database user is to be created.
    :param name (str) Username for the database credential (2-256 characters).
    :param password (str) A password associated with the database credential.
    If this field is left empty, a password will be auto-generated.
    :param access ([object])
    [{
        :param privileges ([str]) The list of privileges granted on the resources. read/write
        :param resources (object) The resources for which access will be granted on.
        {
            :param buckets ([object])
            [{
                :param name (str) The name of the bucket.
                :param scopes ([object])
                [{
                    :param name (str) The name of the scope.
                    :param collections ([str]) The collections under a scope.
                }]
            }]
        }
    }]
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_database_user(
            self,
            organizationId,
            projectId,
            clusterId,
            name,
            access,
            password="",
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Creating Database User {} in cluster {}".format(
                name, clusterId))
        params = {
            "name": name,
            "access": access
        }
        if password:
            params["password"] = password
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(self.db_user_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Method fetches all the database users for a given cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster for which the database users list is to be fetched.
    :param page (int) Sets what page you would like to view
    :param perPage (int) Sets how many results you would like to have on each page
    :param sortBy ([string]) Sets order of how you would like to sort results and also the key you would like to order by
                             Example: sortBy=name
    :param sortDirection (str) The order on which the items will be sorted. Accepted Values - asc / desc
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_database_users(
            self,
            organizationId,
            projectId,
            clusterId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "List all the database users for cluster {}".format(clusterId))
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

        resp = self.api_get(self.db_user_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Method fetches info of the required database user ID.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the database user ID is present.
    :param userId (str) The GUID4 ID of the database user.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_database_user_info(
            self,
            organizationId,
            projectId,
            clusterId,
            userId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Fetching Database user info for {} present in cluster {}".format(
                userId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            "{}/{}".format(
                self.db_user_endpoint.format(
                    organizationId,
                    projectId,
                    clusterId),
                userId),
            params,
            headers)
        return resp

    """
    Method updates the access of database user ID.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the database user ID is present.
    :param userId (str) The GUID4 ID of the database user.
    :param access ([object])
    [{
        :param privileges ([str]) The list of privileges granted on the resources. read/write
        :param resources (object) The resources for which access will be granted on.
        {
            :param buckets ([object])
            [{
                :param name (str) The name of the bucket.
                :param scopes ([object])
                [{
                    :param name (str) The name of the scope.
                    :param collections ([str]) The collections under a scope.
                }]
            }]
        }
    }]
    :param ifmatch (bool) Is set to true then it uses a precondition header that specifies the entity tag of a resource.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def update_database_user(
            self,
            organizationId,
            projectId,
            clusterId,
            userId,
            access,
            ifmatch,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Updating database user {} in cluster {}".format(
                userId, clusterId))
        params = {
            "access": access
        }
        if ifmatch:
            if not headers:
                headers = {}
            result = self.fetch_database_user_info(
                organizationId, projectId, clusterId, userId)
            version_id = result.json()["audit"]["version"]
            headers["If-Match"] = "Version: {}".format(version_id)

        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(
            "{}/{}".format(
                self.db_user_endpoint.format(
                    organizationId,
                    projectId,
                    clusterId),
                userId),
            params,
            headers)
        return resp

    """
    Method deletes specified user ID from the cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the allowed CIDR ID is present.
    :param userId (str) The GUID4 ID of the database user which is to be deleted.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_database_user(
            self,
            organizationId,
            projectId,
            clusterId,
            userId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Deleting database user {} from cluster {}".format(
                userId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            "{}/{}".format(
                self.db_user_endpoint.format(
                    organizationId,
                    projectId,
                    clusterId),
                userId),
            params,
            headers)
        return resp

    """
    Method enables clients to load predefined sample data into a cluster by selecting from three available options:
        - travel-sample
        - gamesim-sample
        - beer-sample
    Upon a successful request, a new bucket will be created within the cluster, and it will be populated with the chosen sample data.

    In order to access this endpoint, the provided API key must have at least one of the following roles:
        - Organization Owner
        - Project Owner
        - Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster which has the sample bucket.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_sample_bucket(
            self,
            organizationId,
            projectId,
            clusterId,
            sampleBucket,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Loading Sample Bucket {} into cluster {} in project {} in "
            "organization {}".format(
                sampleBucket, clusterId, projectId, organizationId))
        params = {
            "name": sampleBucket,
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(self.sample_bucket_endpoint.format(
            organizationId, projectId, clusterId),
            params, headers)
        return resp

    """
    Method Lists configurations of all the sample buckets under a cluster.
    In order to access this endpoint, the provided API key must have at least one of the following roles:
        - Organization Owner
        - Project Owner
        - Project Manager
        - Project Viewer
        - Database Data Reader/Writer
        - Database Data Reader
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster which has the sample bucket.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_sample_buckets(
            self,
            organizationId,
            projectId,
            clusterId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Listing all Sample Buckets in cluster {} in project {} in "
            "organization {}".format(
                clusterId, projectId, organizationId))
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

        resp = self.api_get(self.sample_bucket_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Method Fetches the configuration of the given sample bucket.
    In order to access this endpoint, the provided API key must have at least one of the following roles:
        - Organization Owner
        - Project Owner
        - Project Manager
        - Project Viewer
        - Database Data Reader/Writer
        - Database Data Reader
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster which has the sample bucket.
    :param sampleBucket (str) Name of the Sample Bucket which has to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_sample_bucket(
            self,
            organizationId,
            projectId,
            clusterId,
            sampleBucket,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Fetching sample bucket info for {} present in cluster {}".format(
                sampleBucket, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get("{}/{}".format(
            self.sample_bucket_endpoint.format(
                organizationId, projectId, clusterId), sampleBucket),
            params, headers)
        return resp

    """
    Method Deletes an existing bucket which was loaded with sample data.
    In order to access this endpoint, the provided API key must have at least one of the following roles:
        - Organization Owner
        - Project Owner
        - Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster which has the sample bucket.
    :param sampleBucket (str) Name of the Sample Bucket which has to be deleted.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_sample_bucket(
            self,
            organizationId,
            projectId,
            clusterId,
            sampleBucket,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Deleting Sample Bucket {} from cluster {} in project {} "
            "in organization {}".format(
                sampleBucket, clusterId, projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del("{}/{}".format(
            self.sample_bucket_endpoint.format(
                organizationId, projectId, clusterId), sampleBucket),
            params, headers)
        return resp

    """
    Method creates a new bucket in a cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster in which the bucket is to be created.

    :param name (str) Name of the bucket. This field cannot be changed later.
        The name should be according to the following rules-
        1. Characters used for the name should be in the ranges of A-Z, a-z, and 0-9; plus the underscore,
        period, dash, and percent characters.
        2. The name can be a maximum of 100 characters in length.
        3. The name cannot have 0 characters or empty. Minimum length of name is 1.
        4. The name cannot start with a . (period).

    :param type (str) Type of the bucket. If selected Ephemeral, it is not eligible for imports
    or App Endpoints creation. This field cannot be changed later. The options may also be referred to as
    Memory and Disk (Couchbase), Memory Only (Ephemeral).
        Default: "couchbase"
        Accepted Values: "couchbase" "ephemeral"

    :param storageBackend (str) The storage engine to be assigned to and used by the bucket.
    The minimum memory required for Couchstore is 100 MiB, and the minimum memory required for Magma is 1 GiB.
    This field cannot be changed later.
        Default: "couchstore"
        Accepted Values: "couchstore" "magma"

    :param memoryAllocationInMb (int) The amount of memory to allocate for the bucket memory in MiB.
    The maximum limit is dependent on the allocation of the KV service. Min Value 100.

    :param bucketConflictResolution (str) The means in which conflicts are resolved during replication.
    This field cannot be changed later. This field might be referred to as conflictResolution in some places
    and seqno and lww might be referred as sequence Number and Timestamp respectively.
        Default: "seqno"
        Accepted Values: "seqno" "lww"

    :param durabilityLevel (str) The minimum level at which all writes to the Couchbase bucket must occur.
        Default: "none"
        Accepted Values: "none" "majority" "majorityAndPersistActive" "persistToMajority"

    :param replicas (int) The number of replicas for the bucket.
        Default: 1
        Accepted Values: 1 2 3

    :param flush (bool) Determines whether flushing is enabled on the bucket.
    Enable Flush to delete all items in this bucket at the earliest opportunity.
    Disable Flush to avoid inadvertent data loss.
        Default: false

    :param timeToLiveInSeconds (int) Specify the time to live (TTL) value in seconds. This is the maximum time
    to live for items in the bucket. If specified as 0, TTL is disabled.

    :param evictionPolicy (str) This value should only be used when creating ephemeral buckets. This is also
    known as Ejection Policy at various places. Ejection is the policy which Capella will adopt to prevent
    data loss due to memory exhaustion.
        Accepted Values: "valueOnly" "fullEviction" "noEviction" "nruEviction"

    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_bucket(
            self,
            organizationId,
            projectId,
            clusterId,
            name,
            type,
            storageBackend,
            memoryAllocationInMb,
            bucketConflictResolution,
            durabilityLevel,
            replicas,
            flush,
            timeToLiveInSeconds,
            priority=None,
            evictionPolicy="",
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Creating bucket {} in cluster {}".format(
                name, clusterId))
        params = {
            "name": name,
            "type": type,
            "storageBackend": storageBackend,
            "memoryAllocationInMb": memoryAllocationInMb,
            "bucketConflictResolution": bucketConflictResolution,
            "durabilityLevel": durabilityLevel,
            "replicas": replicas,
            "flush": flush,
            "timeToLiveInSeconds": timeToLiveInSeconds,
        }
        if priority is not None:
            params["priority"] = priority
        if evictionPolicy:
            params["evictionPolicy"] = evictionPolicy
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            self.bucket_endpoint.format(
                organizationId,
                projectId,
                clusterId),
            params,
            headers)
        return resp

    """
    Method fetches all the database users for a given cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
        Database Data Reader/Writer
        Database Data Reader
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster for which the bucket list is to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_buckets(
            self,
            organizationId,
            projectId,
            clusterId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "List all the buckets in the cluster {}".format(clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(self.bucket_endpoint.format(
            organizationId, projectId, clusterId), params, headers)
        return resp

    """
    Method fetches info of the required bucket.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
        Project Viewer
        Database Data Reader/Writer
        Database Data Reader
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_bucket_info(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Fetching bucket info for {} present in cluster {}".format(
                bucketId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get("{}/{}".format(self.bucket_endpoint.format(
            organizationId, projectId, clusterId), bucketId), params, headers)
        return resp

    """
    Method updates the config of an existing bucket.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the database user ID is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.

    :param memoryAllocationInMb (int) The amount of memory to allocate for the bucket memory in MiB.
    The maximum limit is dependent on the allocation of the KV service. Min Value 100.

    :param durabilityLevel (str) The minimum level at which all writes to the Couchbase bucket must occur.
        Default: "none"
        Accepted Values: "none" "majority" "majorityAndPersistActive" "persistToMajority"

    :param replicas (int) The number of replicas for the bucket.
        Default: 1
        Accepted Values: 1 2 3

    :param flush (bool) Determines whether flushing is enabled on the bucket.
    Enable Flush to delete all items in this bucket at the earliest opportunity.
    Disable Flush to avoid inadvertent data loss.
        Default: false

    :param timeToLiveInSeconds (int) Specify the time to live (TTL) value in seconds. This is the maximum time
    to live for items in the bucket. If specified as 0, TTL is disabled.

    :param priority (int) Specifies the ranking of the bucket amongst
    other buckets, ranges from a value between (0, 1000), both inclusive.

    :param ifmatch (bool) Is set to true then it uses a precondition header that specifies the entity tag of a resource.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def update_bucket_config(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            memoryAllocationInMb,
            durabilityLevel,
            replicas,
            flush,
            timeToLiveInSeconds,
            ifmatch,
            priority=None,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Updating bucket {} in cluster {}".format(
                bucketId, clusterId))
        params = {
            "memoryAllocationInMb": memoryAllocationInMb,
            "durabilityLevel": durabilityLevel,
            "replicas": replicas,
            "flush": flush,
            "timeToLiveInSeconds": timeToLiveInSeconds,
            "priority": priority
        }
        if priority:
            params["priority"] = priority

        if ifmatch:
            if not headers:
                headers = {}
            result = self.fetch_bucket_info(
                organizationId, projectId, clusterId, bucketId)
            version_id = result.json()["audit"]["version"]
            headers["If-Match"] = "Version: {}".format(version_id)

        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put("{}/{}".format(self.bucket_endpoint.format(
            organizationId, projectId, clusterId), bucketId), params, headers)
        return resp

    """
    Method deletes specified bucket from the cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_bucket(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Deleting bucket {} in cluster {}".format(
                bucketId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del("{}/{}".format(self.bucket_endpoint.format(
            organizationId, projectId, clusterId), bucketId), params, headers)
        return resp

    """
    Method create's a scope in the specified bucket in the cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param name (str) The name of the scope.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_scope(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            name,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Creating scope {} in bucket {} in cluster {}".format(
                name, bucketId, clusterId))
        params = {
            "name": name
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(self.scope_endpoint.format(
            organizationId, projectId, clusterId, bucketId), params, headers)
        return resp

    """
    Method list's all the scopes in the specified bucket of the cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_scopes(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "List all the scopes for bucket {} in cluster {}".format(
                bucketId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(self.scope_endpoint.format(
            organizationId, projectId, clusterId, bucketId), params, headers)
        return resp

    """
    Method fetches the info of the specified scope of a bucket.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param scopeName (str) The name of the scope whose info is to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_scope_info(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            scopeName,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Fetching scope info for {} in bucket {} in cluster {}".format(
                scopeName, bucketId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            "{}/{}".format(
                self.scope_endpoint.format(
                    organizationId,
                    projectId,
                    clusterId,
                    bucketId),
                scopeName),
            params,
            headers)
        return resp

    """
    Method deletes the specified scope from the bucket.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param scopeName (str) The name of the scope which has to be deleted.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_scope(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            scopeName,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Deleting scope {} in bucket {} in cluster {}".format(
                scopeName, bucketId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            "{}/{}".format(
                self.scope_endpoint.format(
                    organizationId,
                    projectId,
                    clusterId,
                    bucketId),
                scopeName),
            params,
            headers)
        return resp

    """
    Method create's a collection in the specified scope of a bucket in the cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param scopeName (str) The name of the scope under which the collection has to be created.
    :param name (str) The name of the scope.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_collection(self, organizationId, projectId, clusterId, bucketId,
                          scopeName, name, maxTTL=-1, headers=None, **kwargs):
        self.cluster_ops_API_log.info(
            "Creating collection {} in scope {} in bucket {} in cluster {}".format(
                name, scopeName, bucketId, clusterId))
        params = {
            "name": name
        }
        if maxTTL >= 0:
            params["maxTTL"] = maxTTL
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            self.collection_endpoint.format(
                organizationId,
                projectId,
                clusterId,
                bucketId,
                scopeName),
            params,
            headers)
        return resp

    """
    Method list's all the collections in the specified scope in the specified bucket of the cluster.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param scopeName (str) The name of the scope for which the collection has to be listed.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_collections(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            scopeName,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "List all the collections in the scope {} in bucket {} in cluster {}".format(
                scopeName, bucketId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            self.collection_endpoint.format(
                organizationId,
                projectId,
                clusterId,
                bucketId,
                scopeName),
            params,
            headers)
        return resp

    """
    Method fetches the info of the specified collection in the scope of a bucket.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param scopeName (str) The name of the scope under which the collection is present.
    :param collectionName (str) Name of the collection whose info has to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_collection_info(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            scopeName,
            collectionName,
            headers=None,
            **kwargs):
        self.cluster_ops_API_log.info(
            "Fetching info for the collection {} in scope {} in bucket {} in cluster {}".format(
                collectionName, scopeName, bucketId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            "{}/{}".format(
                self.collection_endpoint.format(
                    organizationId,
                    projectId,
                    clusterId,
                    bucketId,
                    scopeName),
                collectionName),
            params,
            headers)
        return resp

    """
    This method is used to change the maxTTL for a collection.
    It requires 'maxTTL' param in its body under the PATCH request since that is the only parameter being mutated.
     - range = (-1 <= maxTTL <= 2147483647) for CB cluster v7.6 or above,
     - else: range = (-0 <= maxTTL <= 2147483647)
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param scopeName (str) The name of the scope under which the collection is present.
    :param collectionName (str) Name of the collection whose info has to be fetched.
    :param maxTTL (int) The time limit for the collection to live.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def update_collection(
            self,
            organizationId,
            projectId,
            clusterId,
            bucketId,
            scopeName,
            collectionName,
            maxTTL,
            headers=None,
            **kwargs):
        params = {
            "maxTTL": maxTTL
        }
        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put("{}/{}".format(
            self.collection_endpoint.format(
                organizationId, projectId, clusterId, bucketId, scopeName),
            collectionName), params, headers)
        return resp

    """
    Method deletes the specified collection in the scope.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param scopeName (str) The name of the scope under which the collection is present.
    :param collectionName (str) Name of the collection which is to be deleted.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_collection(self, organizationId, projectId, clusterId, bucketId,
                          scopeName, collectionName, headers=None, **kwargs):
        self.cluster_ops_API_log.info(
            "Deleting the collection {} in scope {} in bucket {} in cluster {}".format(
                collectionName, scopeName, bucketId, clusterId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            "{}/{}".format(
                self.collection_endpoint.format(
                    organizationId,
                    projectId,
                    clusterId,
                    bucketId,
                    scopeName),
                collectionName),
            params,
            headers)
        return resp

    """
    Creates a scheduled backup for a bucket.
    In order to access this endpoint, the provided API key must have at least one of the following roles:
        Organization Owner
        Project Own
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param dayOfWeek (str) Day of the week for the backup.
    :param startAt  (int) Start at hour (in 24-Hour format).
    :param incrementalEvery  (int) Interval in hours for incremental backup.
    :param retentionTime  (str) Retention time in days.
    :param costOptimizedRetention  (bool) Optimize backup retention to reduce total cost of ownership (TCO). This gives the option to keep all but the last backup cycle of the month for thirty days; the last cycle will be kept for the defined retention period
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_backup_schedule(self, organizationId, projectId, clusterId,
                               bucketId,
                               type, dayOfWeek, startAt, incrementalEvery,
                               retentionTime, costOptimizedRetention,
                               headers=None,
                               **kwargs):

        params = {
            "type": type,
            "weeklySchedule": {
                "dayOfWeek": dayOfWeek,
                "startAt": startAt,
                "incrementalEvery": incrementalEvery,
                "retentionTime": retentionTime,
                "costOptimizedRetention": costOptimizedRetention
            }
        }

        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            self.backup_schedule_endpoint.format(
                organizationId,
                projectId,
                clusterId,
                bucketId),
            params,
            headers)
        return resp

    """
    Fetched the backup schedule for a bucket in a cluster.
    In order to access this endpoint, the provided API key must have at least one of the following roles:
        Organization Owner
        Project Own
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def get_backup_schedule(self, organizationId, projectId, clusterId,
                            bucketId,
                            headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_get(
            self.backup_schedule_endpoint.format(
                organizationId,
                projectId,
                clusterId,
                bucketId),
            params,
            headers
        )

        return resp

    """
    Updates an existing backup schedule.
    In order to access this endpoint, the provided API key must have at least one of the following roles:
        Organization Owner
        Project Own
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param dayOfWeek (str) Day of the week for the backup.
    :param startAt  (int) Start at hour (in 24-Hour format).
    :param incrementalEvery  (int) Interval in hours for incremental backup.
    :param retentionTime  (str) Retention time in days.
    :param costOptimizedRetention  (bool) Optimize backup retention to reduce total cost of ownership (TCO). This gives the option to keep all but the last backup cycle of the month for thirty days; the last cycle will be kept for the defined retention period
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def update_backup_schedule(self, organizationId, projectId, clusterId,
                               bucketId,
                               type, dayOfWeek, startAt, incrementalEvery,
                               retentionTime, costOptimizedRetention,
                               headers=None,
                               **kwargs):
        params = {
            "type": type,
            "weeklySchedule": {
                "dayOfWeek": dayOfWeek,
                "startAt": startAt,
                "incrementalEvery": incrementalEvery,
                "retentionTime": retentionTime,
                "costOptimizedRetention": costOptimizedRetention
            }
        }

        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_put(
            self.backup_schedule_endpoint.format(
                organizationId,
                projectId,
                clusterId,
                bucketId),
            params,
            headers)
        return resp

    """
    Deletes an existing backup schedule
    In order to access this endpoint, the provided API key must have at least one of the following roles:
        Organization Owner
        Project Own
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster under which the bucket is present.
    :param bucketId (str) The ID of the bucket. It is the URL-compatible base64 encoding of the bucket name.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_backup_schedule(self, organizationId, projectId, clusterId,
                               bucketId,
                               headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = None

        resp = self.api_del(
            self.backup_schedule_endpoint.format(
                organizationId,
                projectId,
                clusterId,
                bucketId),
            params,
            headers
        )

        return resp

    def list_appservices(self, tenant_id, page=None, perPage=None, sortBy=None,
                         sortDirection=None, projectId=None, headers=None,
                         **kwargs):
        """
        Lists all the clusters under the organization.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        -Project Manager
        -Project Viewer
        -Database Data Reader/Writer
        -Database Data Reader
        :param tenant_id: Organization id
        :param page (int) Sets what page you would like to view
        :param perPage (int) Sets how many results you would like to have on each page
        :param sortBy ([string]) Sets order of how you would like to sort results and also the key you would like to order by
                             Example: sortBy=name
        :param sortDirection (str) The order on which the items will be sorted. Accepted Values - asc / desc
        :param projectId (str) The GUID4 ID of the project.
        """
        url = self.org_appservice_api.format(tenant_id)
        params = {}
        if page:
            params["page"] = page
        if perPage:
            params["perPage"] = perPage
        if perPage:
            params["sortBy"] = sortBy
        if perPage:
            params["sortDirection"] = sortDirection
        if projectId:
            params["projectId"] = projectId
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_get(url, params=params, headers=headers)
        return resp

    def create_appservice(self, tenant_id, project_id, cluster_id,
                          appservice_name, compute, nodes=None, version=None,
                          description="", headers=None, **kwargs):
        """
        Creates a new App Service.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        :param organizationId (str) Organization ID under which the app service is present.
        :param projectId (str) Project ID under which the app service is present.
        :param clusterId (str) ID of the cluster under which the app service is present.
        :param appservice_name: Name of the appservice.
        :param compute (obj)
            :param cpu: Number of cpu CORES in appservices. Accepted values = [2, 4, 8, 16, 26]
            :param ram: Size of ram (in GBs. Accepted values = [4, 8, 16, 32, 72])
        :param description: Description of the appservice (optional, can be empty)
        :param nodes: Number of nodes in appservices (optional, Number of nodes configured for the App Service. The number of nodes can range from 2 to 12.)
        :param version: Version of appservice to deploy (optional, if not given, defaults to the latest version)
        :param headers (dict) Headers to be sent with the API call.
        :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
        """
        url = self.cluster_appservice_api.format(tenant_id, project_id,
                                                 cluster_id)
        params = {
            "name": appservice_name,
            "compute": compute
        }
        if description:
            params["description"] = description
        if nodes:
            params["nodes"] = nodes
        if version:
            params["version"] = version

        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(url, params, headers)
        return resp

    def delete_appservice(self, tenant_id, project_id, cluster_id,
                          appservice_id, headers=None, **kwargs):
        """
        Deletes an existing App Service.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        -Project Manager
        :param organizationId (str) Organization ID under which the app service is present.
        :param projectId (str) Project ID under which the app service is present.
        :param clusterId (str) ID of the cluster under which the app service is present.
        :param appservice_id: ID of the app service.
        :param headers (dict) Headers to be sent with the API call.
        :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
        """
        url = (self.cluster_appservice_api + "/{}").format(tenant_id,
                                                           project_id,
                                                           cluster_id,
                                                           appservice_id)
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(url, request_body=params, headers=headers)
        return resp

    def get_appservice(self, tenant_id, project_id, cluster_id, appservice_id,
                       headers=None, **kwargs):
        """
        Fetches the details of the given App Service.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        -Project Manager
        -Project Viewer
        -Database Data Reader/Writer
        -Database Data Reader
        """
        url = (self.cluster_appservice_api + "/{}").format(tenant_id,
                                                           project_id,
                                                           cluster_id,
                                                           appservice_id)
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(url, params=params, headers=headers)
        return resp

    def add_app_service_admin_user(self, tenant_id, project_id, cluster_id,
                          appservice_name, headers=None, **kwargs):
        """
        Creates a new App Service Admin User.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        :param organizationId (str) Organization ID under which the app service is present.
        :param projectId (str) Project ID under which the app service is present.
        :param clusterId (str) ID of the cluster under which the app service is present.
        :param appservice_name: Name of the appservice.
        :param headers (dict) Headers to be sent with the API call.
        :param kwargs (dict) the body of the admin users
        """
        url = self.app_service_admin_users.format(tenant_id, project_id,
                                                 cluster_id, appservice_name)
        params = {
            "name": "user1",
            "password": "passwordD,",
            "access": {
                "accessAllEndpoints": True
            }
        }

        for k, v in kwargs.items():
            if isinstance(v, dict) and isinstance(params.get(k), dict):
                params[k].update(v)  # Merge nested dicts like "access"
            else:
                params[k] = v

        resp = self.api_post(url, params, headers)
        return resp

    def fetch_app_service_admin_user_info(self, tenant_id, project_id, cluster_id,
                                    appservice_id, user_id, headers=None,
                                          **kwargs):
        """
        Fetches the admin users of the given App Service.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        -Project Manager
        -Project Viewer
        -Database Data Reader/Writer
        -Database Data Reader
        """
        url = (self.app_service_admin_users + "/{}").format(tenant_id,
                                                            project_id,
                                                            cluster_id,
                                                            appservice_id,
                                                            user_id)
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(url, params=params, headers=headers)
        return resp

    def list_app_service_admin_user(self, tenant_id, project_id, cluster_id,
                                          appservice_id, headers=None,**kwargs):
        """
        Fetches the admin users of the given App Service.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        -Project Manager
        -Project Viewer
        -Database Data Reader/Writer
        -Database Data Reader
        """
        url = self.app_service_admin_users.format(tenant_id,
                                                           project_id,
                                                           cluster_id,
                                                           appservice_id)
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(url, params=params, headers=headers)
        return resp

    def list_app_endpoint_admin_user(self, tenant_id, project_id, cluster_id,
                                     appservice_id, appendpointname,
                                     headers=None,**kwargs):
        """
        Lists the Admin Users that have access to the specified App Endpoint.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        -Project Manager
        -Project Viewer
        -Database Data Reader/Writer
        -Database Data Reader
        """
        url = self.app_endpoint_admin_users.format(tenant_id, project_id,
                                                      cluster_id,
                                                      appservice_id, appendpointname)
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(url, params=params, headers=headers)
        return resp


    def update_app_service_admin_user(self, tenant_id, project_id, cluster_id,
                           appservice_id, user_id, headers=None,
                           **kwargs):
        """
        Updates an existing App Service Admin user.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        -Project Manager
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param appservice_id: Name of the appservice
        :param user_id : Name of the admin user
        :param If-Match: A precondition header that specifies the entity tag of a resource.
        """
        url = (self.app_service_admin_users + "/{}").format(tenant_id,
                                                            project_id,
                                                            cluster_id,
                                                            appservice_id,
                                                            user_id)
        if "accessAllEndpoints" in kwargs:
            params = {
                "accessAllEndpoints": kwargs["accessAllEndpoints"]
            }
        else:
            params = {
                "endpoints": kwargs.get("endpoints", ["v4-test-endpoint"])
            }

        resp = self.api_put(url, params, headers=headers)
        return resp

    def delete_app_service_admin_user(self, tenant_id, project_id, cluster_id,
                          appservice_id, user_id, headers=None, **kwargs):
        """
        Deletes an existing Admin user for the App Service.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        -Project Manager
        :param organizationId (str) Organization ID under which the app service is present.
        :param projectId (str) Project ID under which the app service is present.
        :param clusterId (str) ID of the cluster under which the app service is present.
        :param appservice_id: ID of the app service.
        :param user_id : ID of the user
        :param headers (dict) Headers to be sent with the API call.
        :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
        """
        url = (self.app_service_admin_users + "/{}").format(tenant_id,
                                                            project_id,
                                                            cluster_id,
                                                            appservice_id,
                                                            user_id)
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(url, request_body=params, headers=headers)
        return resp

    def get_cluster(self, tenant_id, project_id, cluster_id, headers=None,
                    **kwargs):
        """
        Fetches the details of the given Cluster.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        -Project Manager
        -Project Viewer
        -Database Data Reader/Writer
        -Database Data Reader
        """
        url = (self.cluster_endpoint + "/{}").format(tenant_id, project_id,
                                                     cluster_id)
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(url, params=params, headers=headers)
        return resp

    def update_appservices(self, tenant_id, project_id, cluster_id,
                           appservice_id, nodes, cpu, ram, headers=None,
                           **kwargs):
        """
        Updates an existing App Service.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        -Organization Owner
        -Project Owner
        -Project Manager
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param appservice_name: Name of the appservice
        :param nodes: Number of nodes in appservices
        :param cpu: Number of cpus in appservices
        :param ram: Size of ram
        :param If-Match: A precondition header that specifies the entity tag of a resource.
        """
        url = (self.cluster_appservice_api + "/{}").format(tenant_id,
                                                           project_id,
                                                           cluster_id,
                                                           appservice_id)
        params = {
            "nodes": nodes,
            "compute": {
                "cpu": cpu,
                "ram": ram
            }
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_put(url, params, headers=headers)
        return resp

    """
    Switches on the App Service.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
        Organization Owner
        Project Owner
        Project Manager
    :param organizationId (str) Organization ID under which the cluster is present.
    :param projectId (str) Project ID under which the cluster is present.
    :param clusterId (str) Cluster ID of the cluster which has the sample bucket.
    :param appServiceId (str) Name of the App Service which has to be switched on.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def switch_app_service_on(self, organizationId, projectId, clusterId,
                              appServiceId, headers=None, **kwargs):
        self.cluster_ops_API_log.info(
            "Switching on App Service {} in cluster {} in project {} in "
            "organization {}".format(appServiceId, clusterId, projectId,
                                     organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_post(
            self.appservice_on_off_endpoint.format(
                organizationId, projectId, clusterId, appServiceId),
            params, headers)
        return resp

    """
        Switches off the App Service.
        In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
            Organization Owner
            Project Owner
            Project Manager
        :param organizationId (str) Organization ID under which the cluster is present.
        :param projectId (str) Project ID under which the cluster is present.
        :param clusterId (str) Cluster ID of the cluster which has the sample bucket.
        :param appServiceId (str) Name of the App Service which has to be switched off.
        :param headers (dict) Headers to be sent with the API call.
        :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
        """

    def switch_app_service_off(self, organizationId, projectId, clusterId,
                               appServiceId, headers=None, **kwargs):
        self.cluster_ops_API_log.info(
            "Switching off App Service {} in cluster {} in project {} in "
            "organization {}".format(appServiceId, clusterId, projectId,
                                     organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            self.appservice_on_off_endpoint.format(
                organizationId, projectId, clusterId, appServiceId),
            params, headers)
        return resp

    def get_express_scaling_status(self, organizationId, projectId, clusterId, headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get("{}/{}".format(
            self.cluster_endpoint.format(organizationId, projectId),
            clusterId), params, headers)
        express_scaling_status = resp.json()["expressScaling"]
        return express_scaling_status

    def enable_express_scaling(self, organizationId, projectId, clusterId, headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = {"expressScaling": True}
        resp = self.api_put(
            self.express_scaling_endpoint.format(
                organizationId, projectId, clusterId), params, headers)
        return resp

    def disable_express_scaling(self, organizationId, projectId, clusterId,
                               headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = {"expressScaling": False}
        resp = self.api_put(
            self.express_scaling_endpoint.format(
                organizationId, projectId, clusterId), params, headers)
        return resp

    def create_app_service_log_streaming(self, organizationId, projectId, clusterId, appServiceId, headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_post(
            self.app_svc_log_streaming_endpoint.format(organizationId, projectId, clusterId, appServiceId), params, headers)
        return resp

    def get_app_service_log_streaming(self, organizationId, projectId, clusterId, appServiceId, headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            self.app_svc_log_streaming_endpoint.format(organizationId, projectId, clusterId, appServiceId), params, headers)
        return resp

    def create_app_endpoint_log_streaming(self, organizationId, projectId, clusterId, appServiceId, appEndpointId, headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_put(
            self.app_endpoint_log_streaming_endpoint.format(organizationId, projectId, clusterId, appServiceId, appEndpointId), params, headers)
        return resp

    def get_app_endpoint_log_streaming(self, organizationId, projectId, clusterId, appServiceId, appEndpointId, headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            self.app_endpoint_log_streaming_endpoint.format(organizationId, projectId, clusterId, appServiceId, appEndpointId), params, headers)
        return resp

    def disable_app_service_log_streaming(self, organizationId, projectId, clusterId, appServiceId, headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            self.app_endpoint_log_streaming_endpoint.format(organizationId, projectId, clusterId, appServiceId), params, headers)
        return resp

    def pause_app_service_log_streaming(self, organizationId, projectId, clusterId, appServiceId, headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            self.app_svc_log_streaming_pause_resume_endpoint.format(organizationId, projectId, clusterId, appServiceId), params, headers)
        return resp

    def resume_app_service_log_streaming(self, organizationId, projectId, clusterId, appServiceId, headers=None, **kwargs):
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_post(
            self.app_svc_log_streaming_pause_resume_endpoint.format(organizationId, projectId, clusterId, appServiceId), params, headers)
        return resp

class CapellaAPI(CommonCapellaAPI):

    def __init__(self, url, secret, access, user, pwd, bearer_token,
                 TOKEN_FOR_INTERNAL_SUPPORT=None):
        """
        Making explicit call to init function of inherited classes because the init params differ.
        """
        super(CapellaAPI, self).__init__(
            url=url, secret=secret, access=access, user=user, pwd=pwd,
            bearer_token=bearer_token,
            TOKEN_FOR_INTERNAL_SUPPORT=TOKEN_FOR_INTERNAL_SUPPORT)
        self.cluster_ops_apis = ClusterOperationsAPIs(
            url, secret, access, bearer_token)
        self.capellaAPI_log = logging.getLogger(__name__)

    def set_logging_level(self, level):
        self.capellaAPI_log.setLevel(level)

    # Cluster methods
    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.list_clusters

    def get_clusters(self, params=None):
        api_response = self.api_get('/v3/clusters', params)
        return (api_response)
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.fetch_cluster_info

    def get_cluster_info(self, cluster_id):
        api_response = self.api_get('/v3/clusters/' + cluster_id)

        return (api_response)
    """

    def get_cluster_status(self, cluster_id):
        api_response = self.api_get(
            '/v3/clusters/' + cluster_id + '/status')

        return (api_response)

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.create_cluster

    def create_cluster(self, cluster_configuration):
        api_response = self.api_post('/v3/clusters', cluster_configuration)

        return (api_response)
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.update_cluster
    def update_cluster_servers(self, cluster_id, new_cluster_server_configuration):
        api_response = self.api_put('/v3/clusters' + '/' + cluster_id + '/servers',
                                                    new_cluster_server_configuration)

        return (api_response)
    """

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

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.delete_cluster
    def delete_cluster(self, cluster_id):
        api_response = self.api_del('/v3/clusters' + '/' + cluster_id)
        return (api_response)
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.list_database_users
    def get_cluster_users(self, cluster_id):
        api_response = self.api_get('/v3/clusters' + '/' + cluster_id +
                                                    '/users')
        return (api_response)
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.delete_database_user
    def delete_cluster_user(self, cluster_id, cluster_user):
        api_response = self.api_del('/v3/clusters' + '/' + cluster_id +
                                                    '/users/' + cluster_user)
        return (api_response)
    """

    """
    Cluster Certificate
    Method Deprecated
    New Method - CLusterOperationsAPIs.get_cluster_certificate
    def get_cluster_certificate(self, cluster_id):
        api_response = self.api_get(
            '/v3/clusters' + '/' + cluster_id + '/certificate')
        return (api_response)
    """

    # Cluster buckets
    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.list_buckets
    def get_cluster_buckets(self, cluster_id):
        api_response = self.api_get('/v2/clusters' + '/' + cluster_id +
                                                    '/buckets')
        return (api_response)
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.create_bucket
    def create_cluster_bucket(self, cluster_id, bucket_configuration):
        api_response = self.api_post('/v2/clusters' + '/' + cluster_id +
                                                     '/buckets', bucket_configuration)
        return (api_response)
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.update_bucket_config
    def update_cluster_bucket(self, cluster_id, bucket_id, new_bucket_configuration):
        api_response = self.api_put('/v2/clusters' + '/' + cluster_id +
                                                    '/buckets/' + bucket_id, new_bucket_configuration)
        return (api_response)
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.delete_bucket
    def delete_cluster_bucket(self, cluster_id, bucket_configuration):
        api_response = self.api_del('/v2/clusters' + '/' + cluster_id +
                                                    '/buckets', bucket_configuration)
        return (api_response)
    """

    # Cluster Allow lists
    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.list_allowed_CIDRs
    def get_cluster_allowlist(self, cluster_id):
        api_response = self.api_get('/v2/clusters' + '/' + cluster_id +
                                                    '/allowlist')
        return (api_response)
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.delete_allowed_CIDR
    def delete_cluster_allowlist(self, cluster_id, allowlist_configuration):
        api_response = self.api_del('/v2/clusters' + '/' + cluster_id +
                                                    '/allowlist', allowlist_configuration)
        return (api_response)
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.add_CIDR_to_allowed_CIDRs_list
    def create_cluster_allowlist(self, cluster_id, allowlist_configuration):
        api_response = self.api_post('/v2/clusters' + '/' + cluster_id +
                                                     '/allowlist', allowlist_configuration)
        return (api_response)
    """

    def update_cluster_allowlist(
            self,
            cluster_id,
            new_allowlist_configuration):
        api_response = self.api_put(
            '/v2/clusters' + '/' + cluster_id + '/allowlist',
            new_allowlist_configuration)
        return (api_response)

    # Cluster user
    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.create_database_user
    def create_cluster_user(self, cluster_id, cluster_user_configuration):
        api_response = self.api_post('/v3/clusters' + '/' + cluster_id +
                                                     '/users', cluster_user_configuration)
        return (api_response)
    """

    # Capella Users
    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.list_database_users
    def get_users(self):
        api_response = self.api_get('/v2/users?perPage=' + str(self.perPage))
        return (api_response)
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.create_bucket
    def create_bucket(self, tenant_id, project_id, cluster_id,
                      bucket_params):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/buckets'.format(url)
        default = {"name": "default", "bucketConflictResolution": "seqno",
                   "memoryAllocationInMb": 100, "flush": False, "replicas": 0,
                   "durabilityLevel": "none", "timeToLive": None}
        default.update(bucket_params)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(default))
        return resp
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.list_buckets
    def get_buckets(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/buckets'.format(url)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp
    """

    def flush_bucket(self, tenant_id, project_id, cluster_id, bucket_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = url + "/buckets/" + bucket_id + "/flush"
        resp = self.do_internal_request(url, method="POST")
        return resp

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.delete_bucket
    def delete_bucket(self, tenant_id, project_id, cluster_id,
                      bucket_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/buckets/{}'.format(url, bucket_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.update_bucket_config
    def update_bucket_settings(self, tenant_id, project_id, cluster_id,
                               bucket_id, bucket_params):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/{}" \
            .format(self.internal_url, tenant_id, project_id,
                    cluster_id, bucket_id)
        resp = self.do_internal_request(url, method="PUT", params=json.dumps(bucket_params))
        return resp
    """

    def jobs(self, project_id, tenant_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/jobs'.format(url)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.fetch_cluster_info
    def get_cluster_internal(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)

        resp = self.do_internal_request(url, method="GET",
                                        params='')
        return resp
    """

    def get_nodes(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = '{}/nodes'.format(url)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.list_database_users
    def get_db_users(self, tenant_id, project_id, cluster_id,
                     page=1, limit=100):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        url = url + '/users?page=%s&perPage=%s' % (page, limit)
        resp = self.do_internal_request(url, method="GET")
        return resp
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.delete_database_user
    def delete_db_user(self, tenant_id, project_id, cluster_id, user_id):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/users/{}" \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    user_id)
        resp = self.do_internal_request(url, method="DELETE",
                                        params='')
        return resp
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.create_database_user
    def create_db_user(self, tenant_id, project_id, cluster_id,
                       user, pwd):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        body = {"name": user, "password": pwd,
                "permissions": {"data_reader": {}, "data_writer": {}}}
        url = '{}/users'.format(url)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(body))
        return resp
    """

    def allow_my_ip(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self._urllib_request("https://ifconfig.me", method="GET")
        if resp.status_code != 200:
            raise Exception("Fetch public IP failed!")
        body = {"create": [{"cidr": "{}/32".format(resp.content.decode()),
                            "comment": ""}]}
        url = '{}/allowlists-bulk'.format(url)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(body))
        return resp

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.add_CIDR_to_allowed_CIDRs_list
    def add_allowed_ips(self, tenant_id, project_id, cluster_id, ips):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}' \
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
    """

    def load_sample_bucket(self, tenant_id, project_id, cluster_id,
                           bucket_name):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/samples" \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        param = {'name': bucket_name}
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(param))
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

    def create_eventing_function(
            self,
            cluster_id,
            name,
            body,
            function_scope=None):
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/functions/{}'.format(
            self.internal_url, cluster_id, name)

        if function_scope is not None:
            url += "?bucket={0}&scope={1}".format(function_scope["bucket"],
                                                  function_scope["scope"])

        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(body))
        return resp

    def __set_eventing_function_settings(
            self, cluster_id, name, body, function_scope=None):
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/functions/{}/settings'.format(
            self.internal_url, cluster_id, name)

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
        return self.__set_eventing_function_settings(
            cluster_id, name, body, function_scope)

    def resume_eventing_function(self, cluster_id, name, function_scope=None):
        body = {
            "processing_status": True,
            "deployment_status": True,
        }
        return self.__set_eventing_function_settings(
            cluster_id, name, body, function_scope)

    def deploy_eventing_function(self, cluster_id, name, function_scope=None):
        body = {
            "deployment_status": True,
            "processing_status": True,
        }
        return self.__set_eventing_function_settings(
            cluster_id, name, body, function_scope)

    def undeploy_eventing_function(
            self,
            cluster_id,
            name,
            function_scope=None):
        body = {
            "deployment_status": False,
            "processing_status": False
        }
        return self.__set_eventing_function_settings(
            cluster_id, name, body, function_scope)

    def get_composite_eventing_status(self, cluster_id):
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/status'.format(
            self.internal_url, cluster_id)

        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_all_eventing_stats(self, cluster_id, seqs_processed=False):
        url = '{}/v2/databases/{}/proxy/_p/event/api/v1/stats'.format(
            self.internal_url, cluster_id)

        if seqs_processed:
            url += "?type=full"

        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_eventing_function(self, cluster_id, name, function_scope=None):
        url = '{}/v2/databases/{}/proxy/_p/event/deleteAppTempStore/?name={}'.format(
            self.internal_url, cluster_id, name)

        if function_scope is not None:
            url += "&bucket={0}&scope={1}".format(function_scope["bucket"],
                                                  function_scope["scope"])
        resp = self.do_internal_request(url, method="GET")
        return resp

    def create_private_network(self, tenant_id, project_id, cluster_id,
                               private_network_params):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/virtualnetworks" \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(
            url, method="POST", params=json.dumps(private_network_params))
        return resp

    def get_private_network(self, tenant_id, project_id, cluster_id,
                            private_network_id):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/virtualnetworks/{}".format(
            self.internal_url, tenant_id, project_id, cluster_id,
            private_network_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def update_specs(self, tenant_id, project_id, cluster_id, specs):
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/specs" \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(specs))
        return resp

    def restore_from_backup(
            self,
            tenant_id,
            project_id,
            cluster_id,
            bucket_name):
        """
        method used to restore from the backup
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param bucket_name:
        :return: response object
        """
        payload = {
            "sourceClusterId": cluster_id,
            "targetClusterId": cluster_id,
            "options": {
                "services": [
                    "data",
                    "query",
                    "index",
                    "search"],
                "filterKeys": "",
                "filterValues": "",
                "mapData": "",
                "includeData": "",
                "excludeData": "",
                "autoCreateBuckets": True,
                "autoRemoveCollections": True,
                "forceUpdates": True}}
        bucket_id = self.get_backups_bucket_id(
            tenant_id=tenant_id,
            project_id=project_id,
            cluster_id=cluster_id,
            bucket_name=bucket_name)
        url = r"{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/{}/restore" \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    bucket_id)
        resp = self.do_internal_request(
            url, method="POST", params=json.dumps(payload))
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

    def get_backups_bucket_id(
            self,
            tenant_id,
            project_id,
            cluster_id,
            bucket_name):
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
        resp = self.do_internal_request(
            url, method="POST", params=json.dumps(payload))
        return resp

    def list_all_bucket_backups(
            self,
            tenant_id,
            project_id,
            cluster_id,
            bucket_id):
        """
        method to obtain the list of backups of a bucket
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param bucket_id:
        :return: response object
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/buckets/{}/backups" \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    bucket_id)
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
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backup_id)
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
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    bucket_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def generate_export_link(
            self,
            tenant_id,
            project_id,
            cluster_id,
            export_id):
        """
        method to generate a pre-signed link for the given export
        :param tenant_id:
        :param project_id:
        :param cluster_id:
        :param export_id:
        :return: response object
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/exports/{}/link" \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    export_id)
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

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.delete_user
    def remove_user(self, tenant_id, user_id):
        url = "{}/tenants/{}/users/{}".format(self.internal_url, tenant_id, user_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp
    """

    def create_xdcr_replication(
            self,
            tenant_id,
            project_id,
            cluster_id,
            payload):
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
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr" \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(payload))
        return resp

    def list_cluster_replications(self, tenant_id, project_id, cluster_id):
        """
        Get all XDCR replications for a cluster
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr" \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def get_replication(
            self,
            tenant_id,
            project_id,
            cluster_id,
            replication_id):
        """
        Get a specific XDCR replication for a cluster
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr/{}".format(
            self.internal_url, tenant_id, project_id, cluster_id,
            replication_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_replication(
            self,
            tenant_id,
            project_id,
            cluster_id,
            replication_id):
        """
        Delete an XDCR replication
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr/{}".format(
            self.internal_url, tenant_id, project_id, cluster_id,
            replication_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def pause_replication(
            self,
            tenant_id,
            project_id,
            cluster_id,
            replication_id):
        """
        Pause an XDCR replication
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr/{}/pause".format(
            self.internal_url, tenant_id, project_id, cluster_id,
            replication_id)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def start_replication(
            self,
            tenant_id,
            project_id,
            cluster_id,
            replication_id):
        """
        Start an XDCR replication
        """
        url = "{}/v2/organizations/{}/projects/{}/clusters/{}/xdcr/{}/start".format(
            self.internal_url, tenant_id, project_id, cluster_id,
            replication_id)
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
        url = '{}/v2/organizations/{}/backends'.format(
            self.internal_url, tenant_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def get_sgw_backend(self, tenant_id, project_id, cluster_id, backend_id):
        """
        Get details about a SyncGateway backend for a cluster
        """
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}'.format(
            self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def delete_sgw_backend(
            self,
            tenant_id,
            project_id,
            cluster_id,
            backend_id):
        """
        Delete a SyncGateway backend
        """
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}'.format(
            self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp

    def create_sgw_database(
            self,
            tenant_id,
            project_id,
            cluster_id,
            backend_id,
            config):
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
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backend_id)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def get_sgw_databases(self, tenant_id, project_id, cluster_id, backend_id):
        "Get a list of all available sgw databases (app endpoints)"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases' \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backend_id)
        resp = self.do_internal_request(url, method="GET")
        return resp

    def resume_sgw_database(
            self,
            tenant_id,
            project_id,
            cluster_id,
            backend_id,
            db_name):
        "Resume the sgw database (app endpoint)"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/online' \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backend_id, db_name)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def pause_sgw_database(
            self,
            tenant_id,
            project_id,
            cluster_id,
            backend_id,
            db_name):
        "Resume the sgw database (app endpoint)"
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/offline' \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backend_id, db_name)
        resp = self.do_internal_request(url, method="POST")
        return resp

    def allow_my_ip_sgw(self, tenant_id, project_id, cluster_id, backend_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/allowip' \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backend_id)
        resp = self._urllib_request("https://ifconfig.me", method="GET")
        if resp.status_code != 200:
            raise Exception("Fetch public IP failed!")
        body = {"cidr": "{}/32".format(resp.content.decode()), "comment": ""}
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(body))
        return resp

    def add_allowed_ip_sgw(
            self,
            tenant_id,
            project_id,
            cluster_id,
            backend_id,
            ip):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/allowip' \
            .format(self.internal_url, tenant_id, project_id, backend_id,
                    cluster_id)
        body = {"cidr": "{}/32".format(ip), "comment": ""}
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(body))
        return resp

    def update_sync_function_sgw(
            self,
            tenant_id,
            project_id,
            cluster_id,
            backend_id,
            db_name,
            config):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/sync' \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backend_id, db_name)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def add_app_role_sgw(
            self,
            tenant_id,
            project_id,
            cluster_id,
            backend_id,
            db_name,
            config):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/roles' \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backend_id, db_name)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def add_user_sgw(
            self,
            tenant_id,
            project_id,
            cluster_id,
            backend_id,
            db_name,
            config):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/users' \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backend_id, db_name)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def add_admin_user_sgw(
            self,
            tenant_id,
            project_id,
            cluster_id,
            backend_id,
            db_name,
            config):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/adminusers' \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backend_id, db_name)
        resp = self.do_internal_request(url, method="POST",
                                        params=json.dumps(config))
        return resp

    def get_sgw_links(
            self,
            tenant_id,
            project_id,
            cluster_id,
            backend_id,
            db_name):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/connect' \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backend_id, db_name)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_sgw_info(self, tenant_id, project_id, cluster_id, backend_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}'.format(
            self.internal_url, tenant_id, project_id, cluster_id, backend_id)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_sgw_certificate(
            self,
            tenant_id,
            project_id,
            cluster_id,
            backend_id,
            db_name):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/backends/{}/databases/{}/publiccert' \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    backend_id, db_name)
        resp = self.do_internal_request(url, method="GET", params='')
        return resp

    def get_node_metrics(
            self,
            tenant_id,
            project_id,
            cluster_id,
            metrics,
            step,
            start,
            end):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/metrics/{}/query_range' \
            .format(self.internal_url, tenant_id, project_id, cluster_id,
                    metrics)
        payload = {'step': step, 'start': start, 'end': end}
        resp = self.do_internal_request(url, method="GET", params=payload)
        return resp

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.create_project
    def create_project(self, tenant_id, name):
        project_details = {"name": name, "tenantId": tenant_id}

        url = '{}/v2/organizations/{}/projects'.format(self.internal_url, tenant_id)
        api_response = self.do_internal_request(url, method="POST",
                                                        params=json.dumps(project_details))
        return api_response
    """

    """
    Method Deprecated.
    New Method - ClusterOperationsAPIs.delete_project
    def delete_project(self, tenant_id, project_id):
        url = '{}/v2/organizations/{}/projects/{}'.format(self.internal_url, tenant_id,
                                                          project_id)
        api_response = self.do_internal_request(url, method="DELETE",
                                                        params='')
        return api_response
    """

    def turn_off_cluster(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/off' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        resp = self.do_internal_request(url, method="POST", params='')
        return resp

    def turn_on_cluster(self, tenant_id, project_id, cluster_id):
        url = '{}/v2/organizations/{}/projects/{}/clusters/{}/on' \
            .format(self.internal_url, tenant_id, project_id, cluster_id)
        payload = "{\"turnOnAppService\":true}"
        resp = self.do_internal_request(
            url, method="POST", params=json.dumps(payload))
        return resp

    def get_root_ca(self, cluster_id):
        url = '{}/v2/databases/{}/proxy/pools/default/trustedCAs' \
            .format(self.internal_url, cluster_id)
        resp = self.do_internal_request(url, method="GET")
        return resp
