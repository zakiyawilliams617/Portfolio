x#!/bin/bash
SOURCE=/home/ec2-user
BACKUP_DIR=/tmp/backups
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FILE=$BACKUP_DIR/backup_$TIMESTAMP.tar.gz

mkdir -p $BACKUP_DIR

tar -czf $BACKUP_FILE $SOURCE

echo "Backup created: $BACKUP_FILE"
