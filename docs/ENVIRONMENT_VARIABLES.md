# Environment Variables Configuration

This document describes all environment variables used in the AWS Ontology project for configuration and deployment.

## Database Configuration

### ArangoDB Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ARANGO_PASSWORD` | ArangoDB root password | `openSesame` | No |
| `ARANGO_HOST` | ArangoDB server host | `http://localhost:8529` | No |
| `ARANGO_USERNAME` | ArangoDB username | `root` | No |
| `ARANGO_DATABASE` | Default database name | `aws_ontology` | No |

### Usage Examples

#### Setting Environment Variables

**Linux/macOS:**
```bash
# Set for current session
export ARANGO_PASSWORD="your_secure_password"
export ARANGO_HOST="http://your-server:8529"

# Set permanently in ~/.bashrc or ~/.zshrc
echo 'export ARANGO_PASSWORD="your_secure_password"' >> ~/.bashrc
```

**Windows:**
```cmd
# Set for current session
set ARANGO_PASSWORD=your_secure_password

# Set permanently
setx ARANGO_PASSWORD "your_secure_password"
```

**Docker:**
```bash
# Pass environment variables to container
docker run -d \
  --name arangodb \
  -p 8529:8529 \
  -e ARANGO_ROOT_PASSWORD=${ARANGO_PASSWORD:-openSesame} \
  arangodb/arangodb:latest
```

#### Using in Python Scripts

```python
import os

# Get password from environment with fallback
password = os.getenv('ARANGO_PASSWORD', 'openSesame')

# Connect to ArangoDB
from arango import ArangoClient
client = ArangoClient(hosts=os.getenv('ARANGO_HOST', 'http://localhost:8529'))
db = client.db(
    os.getenv('ARANGO_DATABASE', 'aws_ontology'),
    username=os.getenv('ARANGO_USERNAME', 'root'),
    password=password
)
```

## Development Configuration

### Python Environment

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PYTHONPATH` | Additional Python module paths | None | No |
| `AWS_ONTOLOGY_ROOT` | Project root directory | Auto-detected | No |

### Testing Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SKIP_SLOW_TESTS` | Skip performance tests | `false` | No |
| `TEST_TIMEOUT` | Test timeout in seconds | `300` | No |

## Monitoring and Automation

### Email Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SMTP_HOST` | SMTP server hostname | None | Yes* |
| `SMTP_PORT` | SMTP server port | `587` | No |
| `SMTP_USERNAME` | SMTP authentication username | None | Yes* |
| `SMTP_PASSWORD` | SMTP authentication password | None | Yes* |
| `EMAIL_FROM` | Sender email address | None | Yes* |
| `EMAIL_TO` | Recipient email addresses (comma-separated) | None | Yes* |

*Required only if using email notifications

### Monitoring Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONITOR_INTERVAL` | Monitoring check interval (hours) | `24` | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` | No |
| `LOG_DIR` | Log file directory | `automation/logs` | No |

## Security Best Practices

### Password Management

1. **Never hardcode passwords** in scripts or configuration files
2. **Use strong passwords** with mixed case, numbers, and symbols
3. **Rotate passwords regularly** in production environments
4. **Use environment-specific passwords** for different deployments

### Environment Files

Create `.env` files for local development (already in `.gitignore`):

```bash
# .env file (DO NOT COMMIT TO GIT)
ARANGO_PASSWORD=your_secure_password
ARANGO_HOST=http://localhost:8529
SMTP_PASSWORD=your_email_password
EMAIL_TO=admin@yourcompany.com
```

Load with:
```bash
# Load environment variables from .env file
set -a
source .env
set +a
```

### Production Deployment

For production deployments:

1. **Use container orchestration** environment variable injection
2. **Use secrets management** systems (AWS Secrets Manager, HashiCorp Vault)
3. **Limit environment variable scope** to necessary processes only
4. **Monitor access** to environment variables in logs

## Configuration Examples

### Local Development

```bash
# Minimal local setup
export ARANGO_PASSWORD="dev_password"

# Run import tool
python tools/import_to_arangodb.py
```

### Production Deployment

```bash
# Production environment variables
export ARANGO_PASSWORD="$(aws secretsmanager get-secret-value --secret-id prod/arango/password --query SecretString --output text)"
export ARANGO_HOST="https://prod-arango.company.com:8529"
export ARANGO_DATABASE="aws_ontology_prod"
export EMAIL_TO="devops@company.com,data-team@company.com"
export LOG_LEVEL="WARNING"

# Run with production settings
python tools/import_to_arangodb.py --database aws_ontology_prod
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  arangodb:
    image: arangodb/arangodb:latest
    environment:
      - ARANGO_ROOT_PASSWORD=${ARANGO_PASSWORD:-openSesame}
    ports:
      - "8529:8529"
    volumes:
      - arangodb_data:/var/lib/arangodb3

  ontology-importer:
    build: .
    environment:
      - ARANGO_PASSWORD=${ARANGO_PASSWORD}
      - ARANGO_HOST=http://arangodb:8529
    depends_on:
      - arangodb

volumes:
  arangodb_data:
```

## Troubleshooting

### Common Issues

1. **Environment variable not found**: Check spelling and ensure variable is exported
2. **Permission denied**: Verify user has access to read environment variables
3. **Connection failed**: Confirm ARANGO_HOST and ARANGO_PASSWORD are correct
4. **Import errors**: Check ARANGO_DATABASE exists and user has write permissions

### Debugging

Enable debug logging to see which environment variables are being used:

```bash
export LOG_LEVEL=DEBUG
python tools/import_to_arangodb.py
```

### Validation Script

Create a simple validation script:

```python
#!/usr/bin/env python3
import os

required_vars = ['ARANGO_PASSWORD']
optional_vars = ['ARANGO_HOST', 'ARANGO_USERNAME', 'ARANGO_DATABASE']

print("Environment Variable Status:")
print("=" * 40)

for var in required_vars:
    value = os.getenv(var)
    status = "✅ SET" if value else "❌ MISSING"
    print(f"{var}: {status}")

for var in optional_vars:
    value = os.getenv(var)
    status = f"✅ {value}" if value else "⚠️  Using default"
    print(f"{var}: {status}")
```

This ensures all necessary environment variables are properly configured before running the AWS Ontology tools.
