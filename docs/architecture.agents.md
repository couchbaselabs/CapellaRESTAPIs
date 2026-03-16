# CapellaRESTAPIs Architecture for AI Agents

## System Overview
CapellaRESTAPIs is a Python client library that provides programmatic access to Couchbase Capella REST APIs. It serves as a middleware layer between test automation frameworks and Capella's API endpoints.

## Architecture Layers

### Layer 1: Infrastructure Layer (`capella/lib/`)
Base components that provide fundamental functionality for all API interactions.

#### APIAuth
**Purpose**: Authentication handler for Capella API requests  
**Location**: `capella/lib/APIAuth.py`  
**Key Methods**:
- `__call__(self, r)` - Authentication middleware for requests
- Implements dual authentication:
  - v3 APIs: HMAC signature using secret key, access key, timestamp
  - v4 APIs: Bearer token authentication  

#### APIRequests
**Purpose**: HTTP request wrapper and session management  
**Location**: `capella/lib/APIRequests.py`  
**Key Methods**:
- `api_get(endpoint, params, headers)` - GET requests
- `api_post(endpoint, body, headers)` - POST requests
- `api_put(endpoint, json_body, data_body, headers)` - PUT requests
- `api_patch(endpoint, body, headers)` - PATCH requests
- `api_del(endpoint, body, headers)` - DELETE requests
- Maintains reusable `network_session` for connection pooling

#### APIExceptions
**Purpose**: Custom exception hierarchy for error handling  
**Location**: `capella/lib/APIExceptions.py`  
**Exception Types**:
- `CbcAPIError` - Base exception (terminates execution)
- `MissingAccessKeyError`, `MissingSecretKeyError`, `MissingBaseURLError`
- `GenericHTTPError`, `AllowlistRuleError`, `UserBucketAccessListError`, `InvalidUuidError`

### Layer 2: Common Service Layer (`capella/common/`)
Shared operations that apply across all service types.

#### OrganizationOperationsAPIs
**Location**: `capella/common/CapellaAPI_v4.py`  
**Endpoints**: `/v4/organizations/*`  
**Operations**:
- `fetch_organization_info(organizationId)` - Get organization details
- `list_organizations()` - List all organizations
- `create_api_key(organizationId, ...)` - Create API keys
- `delete_api_key(organizationId, apiKeyId)` - Delete API keys

#### CommonCapellaAPI
**Location**: `capella/common/CapellaAPI_v4.py`  
**Purpose**: Internal support operations and common utilities  
**Operations**:
- Internal support endpoints (log collection, feature flags)
- User management (signup, verification)
- Project management (create, delete, access)
- Circuit breaker operations
- Query execution and FTS index management

### Layer 3: Service-Specific Layers

#### Dedicated Service (`capella/dedicated/`)
**Location**: `capella/dedicated/CapellaAPI_v4.py`  
**Components**: `ClusterOperationsAPIs`
**Endpoints**: `/v4/organizations/{orgId}/projects/{projectId}/clusters/*`  
**Operations**:
- Cluster lifecycle (create, delete, update, list)
- CIDR management (allowed CIDRs for cluster access)
- User management (database users, bucket access)
- Bucket operations (create, delete, update, list)
- Scope and collection management
- Backup operations and scheduling
- Sample bucket deployment
- App service integration
- On/off scheduling

#### Serverless Service (`capella/serverless/`)
**Location**: `capella/serverless/CapellaAPI.py`  
**Purpose**: Serverless-specific cluster operations  
**Note**: Primarily v3 API support

#### Columnar Service (`capella/columnar/`)
**Location**: `capella/columnar/ColumnarAPI_v4.py`  
**Components**: `ColumnarAPIs`
**Purpose**: Columnar database service operations  
**Operations**: Columnar-specific cluster and database management

## Data Flow Patterns

### Request Flow
```
User Code → Service API Class → APIRequests → APIAuth → Capella API
```

### Authentication Flow
```
Credentials Provided → APIAuth.__call__ → Authorization Header → APIRequests
```

### Error Handling Flow
```
API Response → APIRequests Method → Exception Processing → Custom Exception → User Code
```

## Component Boundaries and Responsibilities

### Infrastructure Layer (No Business Logic)
- **Responsibility**: HTTP transport, authentication, error handling
- **Business Logic**: None
- **Dependencies**: requests library, Python stdlib
- **Interface**: Method signatures for HTTP verbs

### Service Layer (Business Logic Container)
- **Responsibility**: Capella-specific business operations
- **Business Logic**: Endpoint construction, request/response transformation
- **Dependencies**: Infrastructure layer
- **Interface**: Domain-specific method names

### Common Layer (Cross-Cutting Operations)
- **Responsibility**: Operations shared across service types
- **Business Logic**: Organization/project/user management
- **Dependencies**: Infrastructure layer
- **Interface**: Common operations used by multiple services

## Runtime Context

### External Integration Points
- **Parent Repositories**: testrunner, TAF (consume this library as submodule)
- **Capella API**: Cloud API endpoints (various environments)
- **Credential Sources**: Environment variables, runtime parameters

### Session Management
- **Connection Reuse**: `APIRequests.network_session` maintains HTTP session
- **Thread Safety**: `Lock` used for JWT refresh in internal API calls
- **Timeout**: Default 300 seconds for internal requests

### Configuration Points
- **Base URL**: Capella API endpoint (environment-specific)
- **Authentication Credentials**: Access key, secret key, bearer token
- **Internal Support Token**: Separate token for internal operations
- **SSL Verification**: Currently disabled across all requests

## API Version Strategy

### v3 APIs (Legacy)
- **Authentication**: HMAC signature with access/secret keys
- **Header Structure**: `Authorization: Bearer {access_key}:{signature} + Couchbase-Timestamp`
- **Code Pattern**: Methods in `CapellaAPI.py` files

### v4 APIs (Current)
- **Authentication**: Bearer token
- **Header Structure**: `Authorization: Bearer {bearer_token}`
- **Code Pattern**: Methods in `CapellaAPI_v4.py` files

### Detection Logic
```python
if "v4" in r.url:
    # Use Bearer token
else:
    # Use HMAC signature
```

## Validation Clues for Operations

### Success Indicators
- **HTTP Status**: 200 for successful GET/PUT/DELETE, 201 for creation
- **Response Structure**: JSON with expected fields
- **No Exceptions raised**

### Failure Indicators
- **HTTP Status**: 4XX for client errors, 5XX for server errors
- **Exception Raised**: Custom exception from APIExceptions hierarchy
- **Response Content**: Error message in JSON format

### Retry Patterns
- **401 Unauthorized**: JWT refresh logic in internal API calls
- **Connection Errors**: Handled by session retry in APIRequests
- **No explicit retry**: Application-level retry not implemented

## Security Architecture

### Authentication Boundary
- **v3**: HMAC signature computed on client side
- **v4**: Bearer token obtained externally and passed in

### Data Protection
- **Transport**: HTTPS (SSL verification currently disabled)
- **Credentials**: Passed from parent repositories, never stored locally
- **Logging**: Request/response content logged at DEBUG level

### Security Gaps
- **SSL Verification Disabled**: `verify=False` in all requests
- **No Credential Validation**: No validation of credential format before use
- **Logging Risk**: May log sensitive data at DEBUG level

## Extension Points

### Adding New Service Types
1. Create new directory in `capella/`
2. Create API class inheriting from `APIRequests`
3. Implement service-specific methods
4. Define endpoint constants in `__init__`

### Adding New API Operations
1. Add method to appropriate service class
2. Define endpoint using existing patterns
3. Use appropriate HTTP verb method from `APIRequests`
4. Add error handling as needed

### Adding New API Versions
1. Create new file following `{Service}API_v{version}.py` pattern
2. Implement version-specific authentication if needed
3. Update `APIAuth` to recognize new version pattern

## Performance Considerations

### Optimization Points
- **Session Reuse**: Network session prevents connection overhead
- **Pagination Support**: `perPage` parameter for large result sets
- **Thread Safety**: Lock-based JWT refresh

### Bottlenecks
- **Synchronous Requests**: Blocking HTTP calls, no async support
- **SSL Verification**: Disabled verification adds security risk
- **No Request Pooling**: Limited concurrent request handling

## Maintenance Patterns

### Method Signature Patterns
```python
def operation_name(self, required_params, optional_params=None, headers=None, **kwargs):
    # Log operation
    # Call appropriate APIRequests method
    # Return response
```

### Error Handling Patterns
```python
try:
    # API call
except requests.exceptions.HTTPError:
    raise GenericHTTPError(...)
except MissingAccessKeyError:
    # Log and handle
except Exception as e:
    raise CbcAPIError(e)
```

### Endpoint Construction Patterns
```python
self.resource_endpoint = "/v4/organizations/{}/projects/{}/resource"
# Usage:
"{}/{}".format(self.resource_endpoint.format(org_id, project_id), resource_id)
```

## Tooling and Development

### Development Environment
- **IDE**: JetBrains (PyCharm/IntelliJ)
- **Python Version**: 3.x
- **Build System**: setuptools

### Testing Infrastructure
- **Status**: No automated testing infrastructure
- **Parent Repositories**: Test runner and TAF provide validation
- **Manual Testing**: Direct API calls during development

### Code Quality Tools
- **Status**: No linting, formatting, or type checking configured
- **Recommendation**: Add pytest, flake8, black, mypy

## Unknowns and Assumptions

### Unknowns
- Complete list of supported Capella environments
- API key lifecycle and refresh patterns
- Rate limiting and retry requirements
- Performance benchmarks and SLA requirements

### Assumptions
- Credentials are always provided by parent repositories
- SSL verification can remain disabled (security risk)
- No concurrent modifications to same resources
- Network connectivity is reliable

## Migration Path

### Library Evolution
1. **Current**: v3 + v4 dual support
2. **Recommended**: Focus on v4, deprecate v3
3. **Future**: Async support, improved security

### Breaking Changes
- **SSL Verification**: Enabling SSL verification would require certificate management
- **API Version Migration**: v3 to v4 migration requires authentication update
