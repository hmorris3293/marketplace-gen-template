#!/bin/bash

# Function to generate a random UUID4
generate_uuid4() {
  uuid4=$(uuidgen | tr -d '-' | cut -c 1-4)
}

# Check if the app name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <new_app_name>"
  exit 1
fi

# Variables
repo_directory="path/to/marketplace-apps"
new_app_name="$1"
new_branch="${new_app_name}-$(generate_uuid4)"
gen_repo="https://github.com/hmorris3293/marketplace-gen-template.git"
gen_dir="/tmp/marketplace-gen-template"

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
cd $gen_dir

# find & replace all $app_name to $new_app_name aka $1
find $gen_dir -type f -exec sed -i 's/\$app_name/$new_app_name/g' {} + -o -type d -exec bash -c 'mv "$0" "${0/\$app_name/$new_app_name}"' {} \;






