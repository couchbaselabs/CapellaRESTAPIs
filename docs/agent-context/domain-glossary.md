# Capella Domain Glossary

## Core Product Names and Concepts

### Capella
Couchbase Capella - Couchbase's fully managed Database-as-a-Service (DBaaS) platform.

### Service Types
- **Dedicated** - Traditional dedicated cluster deployment with full control over resources
- **Serverless** - Serverless database offering with automatic scaling and pay-per-use pricing
- **Columnar** - Columnar database service for analytical workloads
- **Common** - Shared operations across all service types (organizations, users, projects)

### API Versions
- **v3 APIs** - Earlier API version using HMAC signature authentication
- **v4 APIs** - Current API version using Bearer token authentication

## Authentication and Authorization

### API Keys
- **Access Key** - Public identifier used with HMAC signature authentication (v3)
- **Secret Key** - Private key used to generate HMAC signatures (v3)
- **Bearer Token** - OAuth-style token used for v4 API authentication
- **Organization API Key** - API key scoped at organization level
- **Project API Key** - API key scoped at project level

### Roles and Permissions
- **Organization Owner** - Full administrative access to organization
- **Organization Member** - Standard member access with limited permissions
- **Project Creator** - Can create new projects within organization
- **Project Owner** - Full administrative access to specific project
- **Project Manager** - Can manage project resources but not delete project
- **Project Viewer** - Read-only access to project resources
- **Project Data Reader Writer** - Read and write access to cluster data
- **Project Data Reader** - Read-only access to cluster data

## Capella Resources

### Organization
Top-level container for projects, users, and resources in Capella.

### Project
Container for clusters and resources within an organization. Projects allow logical grouping and resource allocation.

### Cluster
Running Couchbase database instance.
- **Dedicated Cluster** - Cluster with dedicated resources
- **Serverless Cluster** - Serverless database endpoint

### Database Components
- **Bucket** - Logical container for data (similar to database in relational systems)
- **Scope** - Logical grouping of collections within a bucket
- **Collection** - Container for documents within a scope (similar to tables)

### Security Components
- **Allowed CIDRs** - IP ranges allowed to connect to clusters
- **Database User** - User credentials for cluster access
- **Bucket Access** - Permission mapping for database users to buckets

### Operational Components
- **Backup** - Point-in-time copy of cluster data
- **Backup Schedule** - Automated schedule for creating backups
- **Sample Buckets** - Pre-populated sample datasets for testing
- **App Service** - Application services integrated with clusters
- **On-Off Schedule** - Automated cluster start/stop scheduling
- **Log Streaming** - Real-time log export from clusters

## API Concepts

### API Response Patterns
- **Pagination** - Results returned in pages with `perPage` parameter (default 100)
- **Rate Limiting** - Request throttling to prevent abuse
- **Error Responses** - Structured error messages with status codes

### API Endpoints Structure
- **Base URL**: `https://cloudapi.qe-17.sandbox.nonprod-project-avengers.com` (common example)
- **v4 Pattern**: `/v4/organizations/{orgId}/projects/{projectId}/clusters/{clusterId}`
- **Resource Format**: RESTful resource hierarchy

### Request/Response Formats
- **Content-Type**: `application/json` for all API requests
- **Authentication Headers**:
  - v3: `Authorization: Bearer <access_key>:<signature>`
  - v4: `Authorization: Bearer <bearer_token>`
- **Timestamp Header**: `Couchbase-Timestamp` (v3 only)

## Testing and Development

### Test Environments
- **Sandbox** - Testing environment used by QE teams
- **NonProd** - Non-production staging environments
- **Production** - Live customer-facing environment

### Parent Repositories
- **Testrunner** - QA test automation framework that uses CapellaRESTAPIs
- **TAF** - Test Automation Framework that uses CapellaRESTAPIs

## Error Handling

### Exception Types
- **CbcAPIError** - Base exception for all Capella API errors
- **MissingAccessKeyError** - Access key not available
- **MissingSecretKeyError** - Secret key not available
- **MissingBaseURLError** - Base URL not configured
- **GenericHTTPError** - Generic HTTP request failures
- **AllowlistRuleError** - Invalid CIDR allowlist configuration
- **UserBucketAccessListError** - Invalid user bucket access configuration
- **InvalidUuidError** - Invalid UUID format in resource IDs

### HTTP Status Codes
- **200** - Success
- **201** - Resource created
- **400** - Bad request
- **401** - Authentication failed
- **403** - Authorization failed
- **404** - Resource not found
- **409** - Conflict (resource already exists)
- **500** - Internal server error

## Development Tools

### IDE
- **JetBrains IDE** - Primary development environment (PyCharm/IntelliJ)

### Build Tools
- **setuptools** - Package management and distribution
- **setup.py** - Package configuration file

## Security Considerations

### SSL Verification
- **Current Status**: Disabled (`verify=False`) in all requests
- **Security Risk**: Vulnerable to man-in-middle attacks
- **Recommendation**: Implement proper SSL certificate validation

### Credential Management
- **Storage**: Passed from parent repositories at runtime
- **Exposure Risk**: Should never be hardcoded or committed to version control
- **Recommendation**: Use environment variables or secure secret management

## Common Acronyms
- **API** - Application Programming Interface
- **HMAC** - Hash-based Message Authentication Code
- **CIDR** - Classless Inter-Domain Routing (IP address ranges)
- **JWT** - JSON Web Token (used for Bearer tokens)
- **UUID** - Universally Unique Identifier (resource identifiers)
- **REST** - Representational State Transfer (API architecture)
- **DBaaS** - Database-as-a-Service
- **QE** - Quality Engineering
- **TAF** - Test Automation Framework
