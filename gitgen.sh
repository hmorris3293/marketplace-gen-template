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
# cd $gen_dir don't need this

# find & replace all $app_name to $new_app_name aka $1
find $gen_dir -type f -exec sed -i 's/\$app_name/$new_app_name/g' {} + -o -type d -exec bash -c 'mv "$0" "${0/\$app_name/$new_app_name}"' {} \;

# Copy all things over to new branch
## app
cp -R $gen_dir/apps $repo_directory/apps
## deployment_script
cp -R $gen_dir/apps $repo_directory/deployment_scripts

# Verify
app_directory="$repo_directory/apps/linode-marketplace-$new_app_name"

if [ -d "$app_directory" ]; then
    echo "The directory exists: $app_directory"
    echo "All systems GO"
else
    echo "Error: The directory does not exist: $app_directory"
    echo "Elvis or Pat Broke something...."
    exit 1
fi

# Generation complete
echo "Operation new Marketplace app, COMPLETE!"








