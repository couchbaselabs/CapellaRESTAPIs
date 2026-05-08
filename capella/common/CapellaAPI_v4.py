# -*- coding: utf-8 -*-
# Generic/Built-in
import logging

import json
from ..lib.APIRequests import APIRequests

"""
Import CommonCapellaAPI to get access to all the API functionalities.
APIs are segregated according to class for better code management.
"""


class OrganizationOperationsAPIs(APIRequests):

    def __init__(self, url, secret, access, bearer_token):
        super(OrganizationOperationsAPIs, self).__init__(
            url, secret, access, bearer_token)
        self.org_ops_API_log = logging.getLogger(__name__)
        self.organization_endpoint = "/v4/organizations"
        self.apikeys_endpoint = self.organization_endpoint + "/{}/apikeys"
        self.users_endpoint = self.organization_endpoint + "/{}/users"
        self.project_endpoint = self.organization_endpoint + "/{}/projects"
        self.project_cmek_endpoint = self.project_endpoint + "/{}/cmek"
        self.cloud_accounts_endpoint = self.organization_endpoint + "/{}/cloudAccounts"
        self.cmek_endpoint = self.organization_endpoint + "/{}/cmek"
        self.cmek_history_endpoint = self.cmek_endpoint + "/{}/history"
        self.cmek_providers_endpoint = self.cmek_endpoint + "/providers"
        self.project_cmek_providers_endpoint = self.project_cmek_endpoint + "/providers"
        self.cmek_azure_application_endpoint = self.organization_endpoint + "/{}/cmekAzureApplication"
        self.project_cmek_azure_application_endpoint = self.project_endpoint + "/{}/cmekAzureApplication"

    """
    Method fetches the info of the organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Creator
    - Organization Member
    :param organizationId (str) Organization ID under which the user is present
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_organization_info(self, organizationId, headers=None, **kwargs):
        self.org_ops_API_log.info(
            "Fetching info for organization {}".format(organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            "{}/{}".format(self.organization_endpoint, organizationId), params, headers)
        return resp

    """
    Method lists all the organizations.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Creator
    - Organization Member
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_organizations(self, headers=None, **kwargs):
        self.org_ops_API_log.info("Listing all the organizations")
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            self.organization_endpoint, params, headers)
        return resp

    """
    Method lists all the cloud accounts under organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Creator
    - Organization Member
    :param organizationId (str) Organization ID under which cloud accounts are present
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_cloud_accounts(self, organizationId, headers=None):
        self.org_ops_API_log.info(
            "Listing cloud accounts for organization {}".format(organizationId))
        resp = self.api_get(
            self.cloud_accounts_endpoint.format(organizationId), headers)
        return resp

    """
    Method lists all CMEK metadata under organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Organization Member
    :param organizationId (str) Organization ID under which CMEK metadata are present
    :param page (int) Sets what page you would like to view
    :param perPage (int) Sets how many results you would like to have on each page
    :param sortBy ([string]) Sets order of how you would like to sort results and also the key you would like to order by
                             Example: sortBy=name
    :param sortDirection (str) The order on which the items will be sorted. Accepted Values - asc / desc
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_cmek_metadata(
            self,
            organizationId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Listing CMEK metadata for organization {}".format(organizationId))

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

        resp = self.api_get(self.cmek_endpoint.format(organizationId),
                            params, headers)
        return resp

    """
    Method creates CMEK metadata under an organization.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    :param organizationId (str) Organization ID under which CMEK metadata has to be created.
    :param name (str) Name of the key.
    :param config (dict) Config for provider key metadata.
    :param description (str) Description of the key metadata.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_cmek_metadata(
            self,
            organizationId,
            name,
            config,
            description="",
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Creating CMEK metadata in organization {}".format(organizationId))
        params = {
            "name": name,
            "config": config
        }
        if description:
            params["description"] = description
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            self.cmek_endpoint.format(organizationId), params, headers)
        return resp

    """
    Method lists all project-level CMEK metadata under organization and project mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    - Project Cluster Manager
    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID under which CMEK metadata are present.
    :param page (int) Sets what page you would like to view
    :param perPage (int) Sets how many results you would like to have on each page
    :param sortBy ([string]) Sets order of how you would like to sort results and also the key you would like to order by
                             Example: sortBy=name
    :param sortDirection (str) The order on which the items will be sorted. Accepted Values - asc / desc
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_project_cmek_metadata(
            self,
            organizationId,
            projectId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Listing project CMEK metadata for project {} in organization {}".format(
                projectId, organizationId))

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

        resp = self.api_get(
            self.project_cmek_endpoint.format(organizationId, projectId),
            params, headers)
        return resp

    """
    Method creates project-level CMEK metadata under an organization and project.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    - Project Cluster Manager
    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID under which CMEK metadata has to be created.
    :param name (str) Name of the key.
    :param config (dict) Config for provider key metadata.
    :param description (str) Description of the key metadata.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_project_cmek_metadata(
            self,
            organizationId,
            projectId,
            name,
            config,
            description="",
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Creating project CMEK metadata in project {} in organization {}".format(
                projectId, organizationId))
        params = {
            "name": name,
            "config": config
        }
        if description:
            params["description"] = description
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            self.project_cmek_endpoint.format(organizationId, projectId),
            params, headers)
        return resp

    """
    Method fetches project-level CMEK metadata by id.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    - Project Cluster Manager
    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID under which the CMEK metadata is present.
    :param cmekId (str) CMEK metadata ID to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_project_cmek_metadata(
            self,
            organizationId,
            projectId,
            cmekId,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Fetching project CMEK metadata {} in project {} in organization {}".format(
                cmekId, projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            "{}/{}".format(
                self.project_cmek_endpoint.format(organizationId, projectId),
                cmekId),
            params, headers)
        return resp

    """
    Method updates project-level CMEK metadata by id.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    - Project Cluster Manager
    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID under which the CMEK metadata is present.
    :param cmekId (str) CMEK metadata ID to be updated.
    :param config (dict) Config for provider key metadata.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def update_project_cmek_metadata(
            self,
            organizationId,
            projectId,
            cmekId,
            config,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Updating project CMEK metadata {} in project {} in organization {}".format(
                cmekId, projectId, organizationId))
        params = {
            "config": config
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_put(
            "{}/{}".format(
                self.project_cmek_endpoint.format(organizationId, projectId),
                cmekId),
            params, headers)
        return resp

    """
    Method deletes project-level CMEK metadata by id.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    - Project Cluster Manager
    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID under which the CMEK metadata is present.
    :param cmekId (str) CMEK metadata ID to be deleted.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_project_cmek_metadata(
            self,
            organizationId,
            projectId,
            cmekId,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Deleting project CMEK metadata {} in project {} in organization {}".format(
                cmekId, projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            "{}/{}".format(
                self.project_cmek_endpoint.format(organizationId, projectId),
                cmekId),
            params, headers)
        return resp

    """
    Method deletes CMEK metadata under an organization.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    :param organizationId (str) Organization ID under which the CMEK metadata is present.
    :param cmekId (str) CMEK metadata ID to be deleted.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_cmek_metadata(
            self,
            organizationId,
            cmekId,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Deleting CMEK metadata {} in organization {}".format(
                cmekId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del(
            "{}/{}".format(self.cmek_endpoint.format(organizationId), cmekId),
            params, headers)
        return resp

    """
    Method enables CMEK feature for a cloud services provider under an organization.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    :param organizationId (str) Organization ID under which CMEK provider has to be enabled.
    :param cloudProvider (str) Cloud provider. Accepted values: aws, gcp, azure.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def enable_cmek_provider(
            self,
            organizationId,
            cloudProvider,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Enabling CMEK for provider {} in organization {}".format(
                cloudProvider, organizationId))
        params = {
            "cloudProvider": cloudProvider
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_put(
            self.cmek_providers_endpoint.format(organizationId),
            params, headers)
        return resp

    """
    Method enables CMEK feature for a cloud services provider under an organization project.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    - Project Cluster Manager
    :param organizationId (str) Organization ID under which project is present.
    :param projectId (str) Project ID under which CMEK provider has to be enabled.
    :param cloudProvider (str) Cloud provider. Accepted values: azure.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def enable_project_cmek_provider(
            self,
            organizationId,
            projectId,
            cloudProvider,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Enabling project CMEK for provider {} in project {} in organization {}".format(
                cloudProvider, projectId, organizationId))
        params = {
            "cloudProvider": cloudProvider
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_put(
            self.project_cmek_providers_endpoint.format(
                organizationId, projectId),
            params, headers)
        return resp

    """
    Method fetches CMEK metadata by id under an organization.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Organization Member
    :param organizationId (str) Organization ID under which the CMEK metadata is present.
    :param cmekId (str) CMEK metadata ID to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_cmek_metadata(
            self,
            organizationId,
            cmekId,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Fetching CMEK metadata {} in organization {}".format(
                cmekId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            "{}/{}".format(self.cmek_endpoint.format(organizationId), cmekId),
            params, headers)
        return resp

    """
    Method rotates CMEK metadata by id under an organization.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    :param organizationId (str) Organization ID under which the CMEK metadata is present.
    :param cmekId (str) CMEK metadata ID to be rotated.
    :param config (dict) Config for provider key metadata.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def rotate_cmek_metadata(
            self,
            organizationId,
            cmekId,
            config,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Rotating CMEK metadata {} in organization {}".format(
                cmekId, organizationId))
        params = {
            "config": config
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_put(
            "{}/{}".format(self.cmek_endpoint.format(organizationId), cmekId),
            params, headers)
        return resp

    """
    Method lists CMEK key rotation history by id under an organization.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Organization Member
    :param organizationId (str) Organization ID under which the CMEK metadata is present.
    :param cmekId (str) CMEK metadata ID whose history has to be listed.
    :param page (int) Sets what page you would like to view
    :param perPage (int) Sets how many results you would like to have on each page
    :param sortBy ([string]) Sets order of how you would like to sort results and also the key you would like to order by
                             Accepted values: active, associatedAt, associatedBy, key
    :param sortDirection (str) The order on which the items will be sorted. Accepted Values - asc / desc
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_cmek_history(
            self,
            organizationId,
            cmekId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Listing CMEK history for metadata {} in organization {}".format(
                cmekId, organizationId))
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
        resp = self.api_get(
            self.cmek_history_endpoint.format(organizationId, cmekId),
            params, headers)
        return resp

    """
    Method fetches the Azure CMEK application ID under an organization.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Organization Member
    :param organizationId (str) Organization ID under which Azure application is to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_cmek_azure_application(
            self,
            organizationId,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Fetching Azure CMEK application in organization {}".format(
                organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            self.cmek_azure_application_endpoint.format(organizationId),
            params, headers)
        return resp

    """
    Method fetches the Azure CMEK application ID under an organization project.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - Organization Owner
    - Project Owner
    - Project Cluster Manager
    :param organizationId (str) Organization ID under which project is present.
    :param projectId (str) Project ID under which Azure application is to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_project_cmek_azure_application(
            self,
            organizationId,
            projectId,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Fetching Azure project CMEK application for project {} in organization {}".format(
                projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get(
            self.project_cmek_azure_application_endpoint.format(
                organizationId, projectId),
            params, headers)
        return resp

    """
    Method to creates a new API key under an organization.
    - Organization Owners can create Organization and Project scoped APIKeys.
    - Organization Members and Project Creators can create a Project scoped APIKeys for which they are Project Owner.

    :param organizationId (str) Organization ID under which the API key has to be created.
    :param name (str) Name of the APIKey.
    :param organizationRoles ([str]) Organization roles assigned to the APIKey. Accepted values - "organizationOwner"
    "organizationMember" "projectCreator"
    :param description (str) Description for the APIKey.
    Default Value - ""
    :param expiry (int) Expiry of the APIKey in number of days. When it is set to 0, token will not expire.
    Default Value - 180
    :param allowedCIDRs ([str]) List of inbound CIDRs for the APIKey. System making a request must come
    from CIDRs listed in the allowedCIDRs.
    Default Value - ["0.0.0.0/0"]
    :param resources ([APIKeyResources]) Resources are the resource level permissions associated with the APIKey.
    Default Value - []
    [ APIKeyResources (dict)
        {
            type (str) Type of the resource.
            Default Value - project
            id (str) Id of the project.
            roles ([str]) Project Roles associated with the APIKey.
            Accepted Value - "projectOwner" "projectManager" "projectViewer" "projectDataReaderWriter" "projectDataReader"
        }
    ]
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_api_key(
            self,
            organizationId,
            name,
            organizationRoles,
            description="",
            expiry=180,
            allowedCIDRs=["0.0.0.0/0"],
            resources=[],
            headers=None,
            **kwargs):
        self.org_ops_API_log.info("Creating a new API key - {}".format(name))
        params = {
            "name": name,
            "organizationRoles": organizationRoles,
            "description": description,
            "expiry": expiry,
            "allowedCIDRs": allowedCIDRs,
            "resources": resources
        }
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            self.apikeys_endpoint.format(organizationId), params, headers)
        return resp

    """
    Method lists all the apikeys under organization mentioned.
    Organization Owners can list all the APIKeys inside the Organization.
    Organization Members and Project Creators can list all the Project scoped APIKey for which they are Project Owner.

    :param organizationId (str) Organization ID for which the api keys have to be listed.
    :param page (int) Sets what page you would like to view
    :param perPage (int) Sets how many results you would like to have on each page
    :param sortBy ([string]) Sets order of how you would like to sort results and also the key you would like to order by
                             Example: sortBy=name
    :param sortDirection (str) The order on which the items will be sorted. Accepted Values - asc / desc
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_api_keys(
            self,
            organizationId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "List all the API key for Organization {}".format(organizationId))
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
            self.apikeys_endpoint.format(organizationId), params, headers)
        return resp

    """
    Method fetches the details of given APIKey under an organization.
    Organization Owners can get any APIKey inside the Organization.
    Organization Members and Project Creator can get any Project scoped APIKey for which they are Project Owner.

    :param organizationId (str) Organization ID under which the api key is present.
    :param accessKey (str) The ID(acecssKey) of the APIKey.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_api_key_info(
            self,
            organizationId,
            accessKey,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Fetching API key info for {} in organization {}".format(
                accessKey, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get("{}/{}".format(self.apikeys_endpoint.format(
            organizationId), accessKey), params, headers)
        return resp

    """
    Method deletes the api key mentioned.
    Organization Owners can delete any APIKey inside the Organization.
    Organization Members and Project Creator can delete any Project scoped APIKey for which they are Project Owner.

    :param organizationId (str) Organization ID under which the api key is present.
    :param accessKey (str) The ID(acecssKey) of the APIKey to be deleted.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_api_key(
            self,
            organizationId,
            accessKey,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Deleting API key {} in organization {}".format(
                accessKey, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del("{}/{}".format(self.apikeys_endpoint.format(
            organizationId), accessKey), params, headers)
        return resp

    """
    Method rotates secret key of apikeys under organization mentioned.
    Organization Owners can rotate all the APIKeys inside the Organization.
    Organization Members and Project Creators can rotate all the Project scoped APIKey for which they are Project Owner.

    :param organizationId (str) Organization ID for which the api keys have to be rotated.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def rotate_api_key(
            self,
            organizationId,
            accessKey,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info("Rotating secret key for API key - {}".format(accessKey))
        params = {}
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            "{}/{}/rotate".format(self.apikeys_endpoint.format(
                organizationId), accessKey), params, headers)
        return resp

    """
    Method send invites to the user under organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - organizationOwner
    :param organizationId (str) Organization ID for which the user has to be invited
    :param name (str) The name of the user.
    :param email (str) Email of the user.
    :param organizationRole ([string]) 	Items Enum: "organizationOwner" "organizationMember" "projectCreator"
    :param resources ([resource object])
    [
        Resource Object
        {
            resourceId (str) ResourceId of the resource.
            resourceType (str) The type of resource like projects. Current accepted value is project
            roles ([string]) Items Enum: "projectOwner" "projectClusterManager" "projectClusterViewer"
            "projectDataWriter" "projectDataViewer"
        }
    ]
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def invite_users_to_organization(
            self,
            organizationId,
            email,
            organizationRoles,
            name="",
            resources=[],
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Inviting user {} to organization {} with role {}".format(
                email, organizationId, organizationRoles))
        params = {
            "email": email,
            "organizationRoles": organizationRoles
        }
        if name:
            params["name"] = name
        if resources:
            params["resources"] = resources

        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_post(
            self.users_endpoint.format(organizationId), params, headers)
        return resp

    """
    Method lists all the users under organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - organizationOwner
    - organizationMember
    - projectCreator
    :param organizationId (str) Organization ID for which the users have to be listed.
    :param page (int) Sets what page you would like to view
    :param perPage (int) Sets how many results you would like to have on each page
    :param sortBy ([string]) Sets order of how you would like to sort results and also the key you would like to order by
                             Example: sortBy=name
    :param sortDirection (str) The order on which the items will be sorted. Accepted Values - asc / desc
    :param projectId (str) Project ID of the project to list only users under that project.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_org_users(
            self,
            organizationId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            projectId=None,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "List all the users for Organization {}".format(organizationId))

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

        resp = self.api_get(
            self.users_endpoint.format(organizationId), params, headers)
        return resp

    """
    Method fetches the info of the user mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - organizationOwner
    - organizationMember
    - projectCreator
    :param organizationId (str) Organization ID under which the user is present
    :param userId (str) User ID of the user whose info has to be fetched.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_user_info(self, organizationId, userId, headers=None, **kwargs):
        self.org_ops_API_log.info(
            "Fetching user info for {} in organization {}".format(
                userId, organizationId))

        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get("{}/{}".format(self.users_endpoint.format(
            organizationId), userId), params, headers)
        return resp

    """
    Method updates organizational role and resources of the user.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - organizationOwner
    - projectOwner
    - An "organizationOwner" API key can be utilized to update organizational-level roles and project-level
    roles for all projects within the organization.
    - The "ProjectOwner" API key allows for updating project-level roles, solely within the projects
    where the API key holds the "ProjectOwner" role.

    :param organizationId (str) Organization ID under which the user is present.
    :param userId (str) User ID of the user which is to be updated.
    :param update_info ([dict])
    {
        :param op (str) Type of operation. Accepted Values: "add" "replace" "remove".
        :param path (str) Path of resource that needs to be updated. Can be of following forms -
        /organizationRole
        /resources/{resourceId}/
        /resources/{resourceId}/role
        :param value Array of OrganizationRole (strings) or Array of Role (strings) or ResourcePermission (object)

        OrganizationRole ([string])
        Accepted values: "organizationOwner" "organizationMember" "projectCreator"
        - "organizationOwner" is the admin and has unrestricted access to all resources within the organization.
        - "organizationMember" can view settings, users, connected clouds, projects they're a part of, and teams.
        Project role determines privileges within a project.
        - "projectCreator" role includes all Organization Member privileges and automatically assigns the
        Project Owner role to any project the user creates

        Role ([string])
        Accepted values: "projectOwner" "projectClusterManager" "projectClusterViewer" "projectDataWriter"
        "projectDataViewer"
        - "projectOwner" provides complete database-management access. Users with this role can access data
        in any database in a project, referred as Project Owner in docs.
        - "projectClusterManager" Provides access to management actions for all databases in a project.
        This role can create and delete databases but doesn’t provide access to data, referred as Project Manager in docs.
        - "projectClusterViewer" provides read-only access to view all databases in a project.
        This role does not provide access to data, referred as Project Viewer in docs.
        - "projectDataWriter" provides read and write access to data within any database in a project,
        referred as Database Data Reader/Writer in docs.
        - "projectDataViewer" provides read-only access to view data within any database in a project.
        This role allows use of tools like Query Workbench to read data but can’t modify or write data,
        referred as Database Data Reader in docs.

        ResourcePermission (dict)
        {
            resourceId (str) ResourceId of the resource.
            resourceType (str) The type of resource like projects. Current accepted value is project
            roles ([str]) Items Enum: "projectOwner" "projectClusterManager" "projectClusterViewer"
            "projectDataWriter" "projectDataViewer"
        }
    }
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def update_user(
            self,
            organizationId,
            userId,
            update_info,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Updating user {} in organization {}".format(
                userId, organizationId))

        if kwargs:
            update_info += kwargs
        resp = self.api_patch("{}/{}".format(self.users_endpoint.format(
            organizationId), userId), update_info, headers)
        return resp

    """
    Method deletes the user mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - organizationOwner
    :param organizationId (str) Organization ID under which the user to be deleted is present.
    :param userId (str) User ID of the user which has to be deleted
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_user(self, organizationId, userId, headers=None, **kwargs):
        self.org_ops_API_log.info(
            "Deleting user {} in organization {}".format(
                userId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del("{}/{}".format(self.users_endpoint.format(
            organizationId), userId), params, headers)
        return resp

    """
    Method creates a project under organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - organizationOwner
    - projectCreator
    :param organizationId (str) Organization ID under which the project has to be created.
    :param name (str) Name of the project to be created.
    :param description (str) Description of the project. Optional.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def create_project(
            self,
            organizationId,
            name,
            description="",
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Creating Project {} in organization {}".format(
                name, organizationId))
        params = {
            "name": name,
        }
        if description:
            params["description"] = description
        for k, v in kwargs.items():
            params[k] = v
        resp = self.api_post(
            self.project_endpoint.format(organizationId), params, headers)
        return resp

    """
    Method lists all the projects under organization mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - organizationOwner
    - projectOwner
    - projectClusterManager
    - projectClusterManager
    - projectDataWriter
    - projectDataViewer
    :param organizationId (str) Organization ID for which the projects have to be listed.
    :param page (int) Sets what page you would like to view
    :param perPage (int) Sets how many results you would like to have on each page
    :param sortBy ([string]) Sets order of how you would like to sort results and also the key you would like to order by
                             Example: sortBy=name
    :param sortDirection (str) The order on which the items will be sorted. Accepted Values - asc / desc
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def list_projects(
            self,
            organizationId,
            page=None,
            perPage=None,
            sortBy=None,
            sortDirection=None,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "List all the project for Organization {}".format(organizationId))

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
            self.project_endpoint.format(organizationId), params, headers)
        return resp

    """
    Method lists all the info of the project mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - organizationOwner
    - projectOwner
    - projectClusterManager
    - projectDataWriter
    - projectDataViewer
    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID of the project whose info has to be fetched
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def fetch_project_info(
            self,
            organizationId,
            projectId,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Fetching project info for {} in organization {}".format(
                projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_get("{}/{}".format(self.project_endpoint.format(
            organizationId), projectId), params, headers)
        return resp

    """
    Method updates name and description of the project mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - organizationOwner
    - projectOwner
    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID of the project whose info has to be updated
    :param name (str) Updated name of the project.
    :param description (str) Updated Description of the project.
    :param ifmatch (bool) Is set to true then it uses a precondition header that specifies the entity tag of a resource.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def update_project(
            self,
            organizationId,
            projectId,
            name,
            description,
            ifmatch,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Updating project {} in organization {}".format(
                projectId, organizationId))
        params = {
            "name": name,
            "description": description
        }

        if ifmatch:
            if not headers:
                headers = {}
            result = self.fetch_project_info(organizationId, projectId)
            version_id = result.json()["audit"]["version"]
            headers["If-Match"] = "Version: {}".format(version_id)

        for k, v in kwargs.items():
            params[k] = v

        resp = self.api_put(
            "{}/{}".format(self.project_endpoint.format(organizationId), projectId), params, headers)
        return resp

    """
    Method deletes the project mentioned.
    In order to access this endpoint, the provided API key must have at least one of the roles referenced below:
    - organizationOwner
    - projectOwner
    :param organizationId (str) Organization ID under which the project is present.
    :param projectId (str) Project ID of the project which has to be deleted.
    :param headers (dict) Headers to be sent with the API call.
    :param kwargs (dict) Do not use this under normal circumstances. This is only to test negative scenarios.
    """

    def delete_project(
            self,
            organizationId,
            projectId,
            headers=None,
            **kwargs):
        self.org_ops_API_log.info(
            "Deleting project {} in organization {}".format(
                projectId, organizationId))
        if kwargs:
            params = kwargs
        else:
            params = None
        resp = self.api_del("{}/{}".format(self.project_endpoint.format(
            organizationId), projectId), params, headers)
        return resp


class CommonCapellaAPI(APIRequests):

    def __init__(self, url, secret, access, user, pwd, bearer_token,
                 TOKEN_FOR_INTERNAL_SUPPORT=None):
        super(CommonCapellaAPI, self).__init__(
            url, secret, access, bearer_token)
        self.user = user
        self.pwd = pwd
        self.internal_url = url.replace("https://cloud", "https://", 1)
        self.commonCapellaAPI_log = logging.getLogger(__name__)
        self.perPage = 100
        self.TOKEN_FOR_INTERNAL_SUPPORT = TOKEN_FOR_INTERNAL_SUPPORT
        self.cbc_api_request_headers = {
            'Authorization': 'Bearer %s' % self.TOKEN_FOR_INTERNAL_SUPPORT,
            'Content-Type': 'application/json'
        }
        self.org_ops_apis = OrganizationOperationsAPIs(
            url, secret, access, bearer_token)

    def trigger_log_collection(self, cluster_id, log_id={}):
        url = self.internal_url + \
            "/internal/support/logcollections/clusters/{}".format(cluster_id)
        resp = self._urllib_request(url, "POST", params=json.dumps(log_id),
                                    headers=self.cbc_api_request_headers)
        return resp

    def ff_update(self, ff, value):
        url = self.internal_url + \
              "/internal/support/features/flags/{}".format(ff)
        body = {
            "value": bool(value)
        }
        resp = self._urllib_request(url, "PUT", params=json.dumps(body),
                                    headers=self.cbc_api_request_headers)
        return resp

    def get_cluster_tasks(self, cluster_id):
        url = self.internal_url + \
            "/internal/support/clusters/{}/pools/default/tasks".format(cluster_id)
        resp = self._urllib_request(url, "GET",
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

    """
    Method Deprecated.
    New Method - OrganizationAPIs.list_organizations
    def list_accessible_tenants(self):
        url = "{}/tenants".format(self.internal_url)
        resp = self.do_internal_request(url, method="GET")
        return resp
    """

    """
    Method Deprecated.
    New Method - APIKeysAPIs.create_api_key
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
    """

    """
    Method Deprecated.
    New Method - APIKeysAPIs.delete_api_key
    def revoke_access_secret_key(self, tenant_id, key_id):
        url = "{}/tokens/{}?tenantId={}".format(self.internal_url, key_id, tenant_id)
        resp = self.do_internal_request(url, method="DELETE")
        return resp
    """
    def create_circuit_breaker(self, cluster_id, duration_seconds=-1):
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

    """
    Method Deprecated.
    New Method - UsersAPIs.invite_users_to_organization
    def add_user_to_project(self, tenant_id, payload):
        url = "{}/v2/organizations/{}/permissions".format(self.internal_url, tenant_id)
        resp = self.do_internal_request(url, "PUT", params=payload)
        return resp
    """

    """
    Method Deprecated.
    New Method - UsersAPIs.delete_user
    def remove_user_from_project(self, tenant_id, user_id, project_id):
        url = "{}/v2/organizations/{}/permissions/{}/resource/{}" \
            .format(self.internal_url, tenant_id, user_id, project_id)
        resp = self.do_internal_request(url, "DELETE")
        return resp
    """

    """
    Method Deprecated.
    New Method - ProjectAPIs.create_project
    def create_project(self, tenant_id, name):
        project_details = {"name": name, "tenantId": tenant_id}

        url = '{}/v2/organizations/{}/projects'.format(self.internal_url, tenant_id)
        api_response = self.do_internal_request(url, method="POST",
                                                        params=json.dumps(project_details))
        return api_response
    """

    """
    Method Deprecated.
    New Method - ProjectAPIs.delete_project
    def delete_project(self, tenant_id, project_id):
        url = '{}/v2/organizations/{}/projects/{}'.format(self.internal_url, tenant_id,
                                                          project_id)
        api_response = self.do_internal_request(url, method="DELETE",
                                                        params='')
        return api_response
    """

    """
    Method Deprecated.
    New Method - ProjectAPIs.fetch_project_info
    def access_project(self, tenant_id, project_id):
        url = "{}/v2/organizations/{}/projects/{}".format(self.internal_url, tenant_id,
                                                          project_id)
        api_response = self.do_internal_request(url, method="GET", params='')
        return api_response
    """

    def run_query(self, cluster_id, payload):
        url = "{0}/v2/databases/{1}/proxy/_p/query/query/service" \
            .format(self.internal_url, cluster_id)
        resp = self.do_internal_request(
            url, method="POST", params=json.dumps(payload))
        return resp

    def create_fts_index(self, database_id, fts_index_name, payload):
        url = "{}/v2/databases/{}/proxy/_p/fts/api/bucket/{}/scope/samples/index/{}" \
            .format(self.internal_url, database_id, database_id, fts_index_name)
        resp = self.do_internal_request(
            url, method="PUT", params=json.dumps(payload))
        return resp

    def create_control_plane_api_key(
            self,
            organizationID,
            name,
            roles=["organizationOwner"],
            keyType="machine",
            description=""):
        self.commonCapellaAPI_log.info("Creating V2 control plane API key {"
                                       "0} with role {1}".format(name, roles))
        url = "{}/v2/organizations/{}/apikeys".format(
            self.internal_url, organizationID)
        params = {
            "name": name,
            "organizationRoles": roles,
            "keyType": keyType,
            "description": description
        }
        resp = self.do_internal_request(
            url, method="POST", params=json.dumps(params))
        return resp

    def delete_control_plane_api_key(self, organizationID, accesskey):
        self.commonCapellaAPI_log.info("Deleting V2 control plane API key {"
                                       "0}".format(accesskey))
        url = "{}/v2/organizations/{}/apikeys/{}".format(
            self.internal_url, organizationID, accesskey)
        resp = self.do_internal_request(url, method="DELETE")
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
    hostedGCP, hostedAzure
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
                "description": "Cluster Upgrade to {}".format(new_image),
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

