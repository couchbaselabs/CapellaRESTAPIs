# CapellaRESTAPIs - Agent Documentation

## Project Purpose and Scope
Python client library for Couchbase Capella REST APIs, used as a submodule by testrunner and TAF repositories for QA/test automation. Provides programmatic access to Capella Cloud APIs across multiple service types (dedicated, serverless, columnar, common) with dual API version support (v3 and v4).

**Primary Users**: Internal QE/test automation teams  
**Usage Pattern**: Library imported and called directly from parent repositories during test execution

## Core Commands

### Installation and Setup
```bash
# Development installation (required for submodule usage)
pip install -e .

# Verify installation
python -c "from capella.lib.APIRequests import APIRequests; print('OK')"
```

### Library Verification
```bash
# Test core infrastructure
python -c "from capella.lib.APIAuth import APIAuth; from capella.lib.APIRequests import APIRequests; print('Core OK')"

# Test service imports
python -c "from capella.dedicated.CapellaAPI_v4 import ClusterOperationsAPIs; from capella.serverless.CapellaAPI import CapellaAPI; from capella.columnar.ColumnarAPI_v4 import ColumnarAPIs; from capella.common.CapellaAPI_v4 import OrganizationOperationsAPIs; print('Services OK')"
```

### Operational Patterns
```python
# v4 API usage pattern (Bearer token)
from capella.dedicated.CapellaAPI_v4 import ClusterOperationsAPIs
api = ClusterOperationsAPIs(
    url="https://cloudapi.qe-17.sandbox.nonprod-project-avengers.com",
    secret=secret_key,  # v3 HMAC auth
    access=access_key,   # v3 HMAC auth  
    bearer_token=token   # v4 Bearer auth
)
response = api.list_clusters(organizationId, projectId)
```

## Repo Layout

### Core Infrastructure
- `capella/lib/` - Base components (APIAuth, APIRequests, APIExceptions)
- `capella/common/` - Organization-level and shared operations
- `capella/dedicated/` - Dedicated cluster operations
- `capella/serverless/` - Serverless cluster operations
- `capella/columnar/` - Columnar database operations
- `docs/agent-context/` - Agent documentation context
- `setup.py` - Package configuration

### File Conventions
- `CapellaAPI.py` - v3 API implementations (HMAC auth)
- `CapellaAPI_v4.py` - v4 API implementations (Bearer auth)
- `ColumnarAPI_v4.py` - Columnar-specific v4 operations

## Development Patterns and Constraints

### Authentication Strategy
- **v3 APIs**: HMAC signature using secret key, access key, timestamp
- **v4 APIs**: Bearer token authentication
- **Detection**: API determines auth method based on URL containing "v4"

### Request Patterns
- Use service-specific API classes (ClusterOperationsAPIs, OrganizationOperationsAPIs)
- All methods follow pattern: `operation_{name}(required_params, optional_params=None, headers=None, **kwargs)`
- HTTP methods: `api_get()`, `api_post()`, `api_put()`, `api_patch()`, `api_del()`

### Code Style Constraints
- No automated linting or formatting currently configured
- Thread-safety: Lock-based JWT refresh in internal API calls
- Session reuse: `network_session` maintains HTTP connections
- **SSL verification disabled** across all requests (security concern)

### API Version Compatibility
- Maintain both v3 (legacy) and v4 (current) versions when adding features
- v4 preferred for new implementations
- Check existing service files to determine version requirements

## Validation and Evidence Required Before Completion

### Mandatory Verification Steps
1. **Import Validation**: All service classes import correctly in parent repository context
2. **Authentication Test**: Successful API call using credentials provided by parent repository
3. **Endpoint Verification**: Constructed API endpoints match Capella API documentation
4. **Error Handling**: Custom exceptions properly raised and propagate correctly
5. **Response Parsing**: JSON responses parse correctly without errors

### Testing Evidence Requirements
- Manual API call verification for each service type (dedicated, serverless, columnar, common)
- Both v3 and v4 endpoint testing when applicable
- Error path verification (invalid credentials, missing resources)
- Integration testing through parent repositories (testrunner, TAF)

### Validation Commands
```bash
# Manual verification pattern
python -c "
from capella.dedicated.CapellaAPI_v4 import ClusterOperationsAPIs
api = ClusterOperationsAPIs(base_url, secret, access, bearer_token)
# Perform test API call
response = api.list_clusters(org_id, project_id)
print('Success' if response.status_code == 200 else 'Failed')
"
```

## Security and Sensitive-Path Guidance

### Credential Management
- **Never hardcode** API keys, secret keys, or bearer tokens in code
- Credentials are **passed from parent repositories** at runtime
- Store credentials in parent repository environment variables
- No credential storage in CapellaRESTAPIs

### URL and Endpoint Security
- Base URLs vary by environment (sandbox, staging, production)
- Example: `https://cloudapi.qe-17.sandbox.nonprod-project-avengers.com`
- Verify endpoint URLs match intended Capella environment

### SSL Verification Warning
- **Critical Security Issue**: SSL verification (`verify=False`) is disabled throughout codebase
- This creates vulnerability to man-in-middle attacks
- **Immediate Action Required**: Implement proper SSL certificate handling
- For development: May be acceptable temporarily
- For production: SSL verification must be enabled

### Logging Security
- DEBUG logging may include request/response content
- Review logs before sharing to ensure no sensitive data exposure
- Credentials should never appear in log output

### Git Security
- Never commit environment files with actual credentials
- `.gitignore` should prevent credential file commits
- Review diffs carefully for accidental credential inclusion

### External References
- Capella API documentation for endpoint verification
- Security team guidance for SSL certificate management
- Credential rotation policies from Capella platform

## Supporting Documentation

### Agent Context Documents
- [Repo Inventory](docs/agent-context/repo-inventory.md) - Complete repository analysis
- [Build and Test Matrix](docs/agent-context/build-test-matrix.md) - Command patterns and validation workflows
- [Domain Glossary](docs/agent-context/domain-glossary.md) - Capella terminology and concepts

### Architecture Documentation
- [Architecture for Agents](docs/architecture.agents.md) - System design and component relationships

### Operational Guidance
- When adding new API operations: Follow existing method signature patterns
- When creating new service types: Inherit from APIRequests and implement service-specific methods
- When debugging API failures: Check exception hierarchy and API response content
- When updating authentication: Verify both v3 and v4 paths as needed

### Integration Context
- Primary integration: testrunner repository (QA test automation)
- Secondary integration: TAF repository (Test Automation Framework)
- Credentials flow: Parent repos → CapellaRESTAPIs → Capella Cloud APIs
- No direct user interaction: Library called programmatically only
