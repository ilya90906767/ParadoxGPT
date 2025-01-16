#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Archive the database
docker-compose exec db pg_dump -U $DB_USER $DB_NAME > database_backup.sql