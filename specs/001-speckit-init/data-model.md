# Data Model: speckit-init

No new data entities. Development infrastructure only.

## Configuration Entities

### CI Environment Variables
- LOG_LEVEL: INFO
- RABBITMQ_HOST: localhost
- RABBITMQ_USER: guest
- RABBITMQ_PASSWORD: guest
- RABBITMQ_QUEUE: test
- RABBITMQ_RESULT_QUEUE: test-result

### Flake8 Configuration (NEW)
- max-line-length: 100
- exclude: .git,__pycache__,.specify
