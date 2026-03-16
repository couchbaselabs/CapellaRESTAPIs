# Build and Test Matrix

## Current State
This repository currently has no automated build, test, or validation infrastructure. The library is used as a submodule and called directly by parent repositories (testrunner, TAF).

## Build Commands

### Package Installation
```bash
# Development installation (editable mode)
pip install -e .

# Standard installation
pip install .
```

### Distribution
```bash
# Build source distribution
python setup.py sdist

# Build wheel distribution
python setup.py bdist_wheel
```

## Test Commands (Not Currently Implemented)

### Unit Tests (Recommended Addition)
```bash
# Install test dependencies (to be added to requirements-dev.txt)
pip install pytest pytest-cov pytest-mock

# Run unit tests with coverage
pytest tests/ --cov=capella --cov-report=html --cov-report=term

# Run specific test files
pytest tests/test_api_auth.py -v
```

### Integration Tests (Recommended Addition)
```bash
# Run integration tests (requires valid credentials)
pytest tests/integration/ --skip-slow -v

# Run with specific environment
pytest tests/integration/ --env=sandbox -v
```

### Lint Commands (Recommended Addition)
```bash
# Install lint tools (to be added to requirements-dev.txt)
pip install flake8 black isort mypy

# Code formatting
black capella/

# Import sorting
isort capella/

# Linting
flake8 capella/

# Type checking
mypy capella/
```

## Validation Evidence Required Before Completion

### Manual Validation (Current Process)
1. **Authentication verification**
   - Test v3 API calls with HMAC signature authentication
   - Test v4 API calls with Bearer token authentication
   - Verify credentials passed from parent repositories correctly

2. **Service-specific validation**
   - Test each service type (dedicated, serverless, columnar, common)
   - Verify API endpoints respond correctly
   - Check error handling and exception propagation

3. **Integration verification**
   - Import library in parent repositories (testrunner, TAF)
   - Execute API calls through parent test frameworks
   - Verify response parsing and error handling

### Recommended Automated Validation

#### Pre-commit Checks
```bash
#!/bin/bash
# .git/hooks/pre-commit (recommended)

# Run linting
flake8 capella/ || exit 1

# Check formatting
black --check capella/ || exit 1

# Type checking
mypy capella/ || exit 1

# Run unit tests
pytest tests/unit/ || exit 1
```

#### Smoke Tests (Recommended Addition)
```bash
# Quick sanity checks before major changes
python -m pytest tests/smoke/ -v --timeout=30
```

## Component-Specific Commands

### Core Infrastructure
```bash
# Test authentication layer
python -c "from capella.lib.APIAuth import APIAuth; print('APIAuth OK')"

# Test request handling
python -c "from capella.lib.APIRequests import APIRequests; print('APIRequests OK')"

# Test exceptions
python -c "from capella.lib.APIExceptions import *; print('APIExceptions OK')"
```

### Service Types
```bash
# Test dedicated service imports
python -c "from capella.dedicated.CapellaAPI_v4 import ClusterOperationsAPIs; print('Dedicated OK')"

# Test serverless service imports
python -c "from capella.serverless.CapellaAPI import CapellaAPI; print('Serverless OK')"

# Test columnar service imports
python -c "from capella.columnar.ColumnarAPI_v4 import ColumnarAPIs; print('Columnar OK')"

# Test common service imports
python -c "from capella.common.CapellaAPI_v4 import OrganizationOperationsAPIs; print('Common OK')"
```

## Environment-Specific Configuration

### Development Environment
```bash
# Set up development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .[dev]  # Development dependencies (to be added in setup.py)
```

### Production Deployment
```bash
# Standard production installation
pip install capellaApi==1.0

# or from specific commit/branch
pip install git+https://github.com/couchbaselabs/CapellaRESTAPIs.git@master
```

## Dependency Management (Recommended Addition)

### requirements.txt (Recommended)
```
requests>=2.25.0
```

### requirements-dev.txt (Recommended)
```
requests>=2.25.0
pytest>=6.0.0
pytest-cov>=2.12.0
pytest-mock>=3.6.0
flake8>=3.9.0
black>=21.5b0
isort>=5.9.0
mypy>=0.910
```

## Common Issues and Solutions

### Import Errors
```bash
# Ensure editable install or correct PYTHONPATH
pip install -e .
# or
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### SSL Verification Warnings
```bash
# Currently SSL verification is disabled (verify=False)
# This is a security concern and should be addressed
# Recommended: Implement proper SSL certificate handling
```

### Authentication Failures
```bash
# Verify credentials are being passed correctly
# Check that environment variables are set in parent repositories
# Ensure Bearer tokens are valid and not expired
```

## Missing Infrastructure

### High Priority
1. **Test framework setup** - pytest configuration and test structure
2. **CI/CD pipeline** - GitHub Actions or equivalent for automated testing
3. **Pre-commit hooks** - Automated code quality checks before commits
4. **Requirements files** - Formal dependency management

### Medium Priority
1. **Code formatting** - black and isort configuration
2. **Type hints** - Add mypy for type checking
3. **Documentation generation** - API documentation from docstrings
4. **Security scanning** - Dependency vulnerability checks

### Low Priority
1. **Performance benchmarks** - API response time monitoring
2. **Integration test environments** - Staging sandbox configuration
3. **Release automation** - Automated version tagging and publishing
