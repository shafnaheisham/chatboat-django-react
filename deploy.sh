#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define the old app directory
OLD_APP_DIR="old_app"

# Check if the old app directory exists and delete it
if [ -d "$OLD_APP_DIR" ]; then
    echo "Deleting old app directory: $OLD_APP_DIR"
    rm -rf "$OLD_APP_DIR"
    echo "Old app deleted."
else
    echo "No old app directory found to delete."
fi