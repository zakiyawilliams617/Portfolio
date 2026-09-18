#!/bin/bash
THRESHOLD=80
USAGE=$(df -h / | grep / | awk '{print $5}' | tr -d '%')

echo "Current disk usagee: $USAGE%"

if [ $USAGE -gt $THRESHOLD ]; then
	echo "WARNING: Disk space is above $THRESHOLD%!"
else
	echo "OK: Disk space is fine"
fi 
