# CapellaRESTAPIs Repository Inventory

## Summary
Python client library for Couchbase Capella REST APIs. Used as a submodule by testrunner and TAF repositories for QA/test automation. Supports multiple service types (dedicated, serverless, columnar, common) with v3 and v4 API versions.

## Detected Languages and Frameworks
- **Python 3.x** - Primary language
- **requests** - HTTP client library (only external dependency)
- **setuptools** - Package management and distribution

## Package and Build Systems
- **setup.py** - Standard setuptools configuration
- **Installation**: `pip install -e .` (editable install for development)
- **Dependencies**: 
  - requests (HTTP client)
  - No additional dependencies or virtual environment requirements detected

## Test Frameworks and Entry Points
- **No test infrastructure** - No test files, pytest, or testing framework detected
- **Manual testing** - Library is called directly from parent repositories (testrunner, TAF)
- **Entry points**:
  - `capella.dedicated.CapellaAPI_v4` - Dedicated service v4 APIs
  - `capella.serverless.CapellaAPI` - Serverless service APIs  
  - `capella.columnar.ColumnarAPI_v4` - Columnar service v4 APIs
  - `capella.common.CapellaAPI` - Common/shared APIs

## Important Top-Level Directories
- `capella/lib/` - Core infrastructure (authentication, requests, exceptions)
- `capella/dedicated/` - Dedicated cluster operations
- `capella/serverless/` - Serverless cluster operations
- `capella/columnar/` - Columnar database operations
- `capella/common/` - Organization and shared operations
- `docs/agent-context/` - Agent documentation context

## CI, Devcontainer, Hook, and Lint Evidence
- **No CI/CD** - No GitHub Actions, workflows, or CI configuration detected
- **No devcontainer** - No container configuration files
- **No pre-commit hooks** - No hook automation or linting configuration
- **No lint configuration** - No flake8, pylint, black, or other linting tools configured
- **Development environment**: JetBrains IDE (`.idea/` directory present)

## Key Infrastructure Components
- **APIAuth** (`capella/lib/APIAuth.py`) - Dual authentication support:
  - HMAC signature authentication (v3 APIs)
  - Bearer token authentication (v4 APIs)
- **APIRequests** (`capella/lib/APIRequests.py`) - HTTP request wrapper supporting GET/POST/PUT/PATCH/DELETE with session management
- **APIExceptions** (`capella/lib/APIExceptions.py`) - Custom exception hierarchy for API errors

## API Version Support
- **v3 APIs** - HMAC signature-based authentication
- **v4 APIs** - Bearer token-based authentication
- **Service types** - All services support both versions where applicable

## Missing Documents Needed for Better Agent Operation
- **AGENTS.md** - Primary agent operational documentation
- **build-test-matrix.md** - Validation and command patterns
- **domain-glossary.md** - Capella-specific terminology and concepts
- **architecture.agents.md** - System design and component relationships
- **requirements.txt** - Formal dependency specification
- **API usage examples** - Concrete usage patterns for each service type
- **Environment setup guide** - How to configure credentials and base URLs

## Unknowns Requiring Maintainer Input
- **Base URL patterns** - Complete list of supported Capella environments (production, staging, sandbox)
- **Credential management** - Standard environment variable names and patterns for passing credentials
- **API rate limits** - Request throttling or retry patterns needed
- **SSL verification** - Current code disables SSL verification (`verify=False`) - security implications unknown
- **Error handling patterns** - Standard retry logic, timeout values, and failure modes
- **API key lifecycle** - How bearer tokens are obtained, refreshed, and managed
- **Service-specific constraints** - Limitations or special handling per service type

## Security Concerns
- **SSL verification disabled** - All API requests use `verify=False`, disabling SSL certificate validation
- **Credentials in code** - Potential exposure if not properly managed through environment variables
- **No secrets management** - No documented pattern for secure credential handling
