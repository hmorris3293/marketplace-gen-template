#!/bin/bash

# Function to generate a random UUID4
generate_uuid4() {
  uuid4=$(uuidgen | tr -d '-' | cut -c 1-4)
}

# Check if the app name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <app_name>"
  exit 1
fi

# Variables
repo_directory="path/to/marketplace-apps"
app_name="$1"
new_branch="${app_name}-$(generate_uuid4)"
gen_repo="https://github.com/hmorris3293/marketplace-gen-template.git"

# Change directory to the repository
cd "$repo_directory" || exit

# Checkout the develop branch
git checkout develop

# Fetch changes from upstream
git fetch upstream

# Merge changes from upstream/develop
git merge upstream/develop

# Create a new branch
git checkout -b "$new_branch"

echo "Successfully checked out branch: $new_branch"

# Pull down template in tmp
git -C /tmp clone $gen_repo

# CD into template repo
cd /tmp/marketplace-gen-template





