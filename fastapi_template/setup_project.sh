#!/bin/bash
PROJECT_ROOT="."
APP_NAME="app"

# Base folder
mkdir -p ${PROJECT_ROOT}/src/{${APP_NAME}/{api/v1/endpoints,core,models,repositories,schemas,services,db},tests,alembic/versions}

# Create example files
touch ${PROJECT_ROOT}/src/${APP_NAME}/main.py
touch ${PROJECT_ROOT}/src/${APP_NAME}/api/v1/endpoints/example.py
touch ${PROJECT_ROOT}/src/${APP_NAME}/core/{config.py,security.py}
touch ${PROJECT_ROOT}/src/${APP_NAME}/models/example.py
touch ${PROJECT_ROOT}/src/${APP_NAME}/repositories/example_repository.py
touch ${PROJECT_ROOT}/src/${APP_NAME}/schemas/example.py
touch ${PROJECT_ROOT}/src/${APP_NAME}/services/example_service.py
touch ${PROJECT_ROOT}/src/${APP_NAME}/db/{base.py,session.py}
touch ${PROJECT_ROOT}/src/tests/test_example.py
touch ${PROJECT_ROOT}/requirements.txt
touch ${PROJECT_ROOT}/pyproject.toml
touch ${PROJECT_ROOT}/.gitignore
touch ${PROJECT_ROOT}/Dockerfile
touch ${PROJECT_ROOT}/docker-compose.yml

# echo complete message
echo "Project structure created successfully!"
