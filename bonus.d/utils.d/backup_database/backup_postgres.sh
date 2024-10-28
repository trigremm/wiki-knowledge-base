#!/bin/bash
# Date format includes date and time
# Example: dbname_2023-04-12_15-30.sql

DATE=$(date +%Y-%m-%d_%H-%M)
DB_BACKUP_PATH='/backups'
DB_HOST=${DATABASE_HOST}
DB_PORT=${DATABASE_PORT}
DB_NAME=${POSTGRES_DB}
DB_USER=${POSTGRES_USER}
DB_PASS=${POSTGRES_PASSWORD}

# Export database into SQL file
PGPASSWORD=${DB_PASS} pg_dump -h localhost -U ${DB_USER} ${DB_NAME} > ${DB_BACKUP_PATH}/${DB_NAME}_${DATE}.sql

PGPASSWORD=${DB_PASS} pg_dump -h localhost -U ${DB_USER} ${DB_NAME} | gzip > ${DB_BACKUP_PATH}/${DB_NAME}_${DATE}.sql.gz

## Optional: Remove backups older than 30 days
#find $DB_BACKUP_PATH/* -mtime +30 -exec rm {} \;
