#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Create a new database
docker-compose exec db createdb $DB_NAME

# Restore the archive to the new database
docker-compose exec db psql -U $DB_USER $DB_NAME < database_backup.sql