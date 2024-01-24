import os
import shutil
import subprocess
import sys
import uuid

# Function to remove a directory if it exists
def remove_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"Directory {directory} removed.")
    else:
        print("Directory does not exist. Moving on.")

# Function to replace text in files
def replace_text(directory, old_text, new_text):
    for root, _, files in os.walk(directory):
        # Skip processing files within the .git directory
        if '.git' in root:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                try:
                    content = f.read().decode('utf-8')
                except UnicodeDecodeError:
                    # Handle non-UTF-8 encoded files (you may adjust the encoding if needed)
                    content = f.read().decode('latin-1')

            content = content.replace(old_text, new_text)

            with open(file_path, 'wb') as f:
                f.write(content.encode('utf-8'))


# Variables
repo_directory = os.path.expanduser("~/Projects/marketplace-apps")
gen_repo = "https://github.com/hmorris3293/marketplace-gen-template.git"
gen_dir = "/tmp/marketplace-gen-template"

# Remove existing temporary directory
remove_directory(gen_dir)

# Check if the app name argument is provided
if len(os.sys.argv) != 2:
    print("Usage: {} <new_app_name>".format(os.sys.argv[0]))
    os.sys.exit(1)

new_app_name = os.sys.argv[1]
new_branch = "{}-{}".format(new_app_name, str(uuid.uuid4()).replace('-', '')[:4])

# Change directory to the repository
os.chdir(repo_directory)

# Checkout the develop branch
subprocess.run(["git", "checkout", "develop"])

# Fetch changes from upstream
subprocess.run(["git", "fetch", "upstream"])

# Merge changes from upstream/develop
subprocess.run(["git", "merge", "upstream/develop"])

# Create a new branch
subprocess.run(["git", "checkout", "-b", new_branch])
print("Successfully checked out branch:", new_branch)

# Pull down template in tmp
subprocess.run(["git", "-C", "/tmp", "clone", gen_repo])

# Find and replace all occurrences of 'app_name' with the new app name
replace_text(gen_dir, 'app_name', new_app_name)

# Replace directory names
os.rename(os.path.join(gen_dir, 'apps', 'linode-marketplace-app_name'),
          os.path.join(gen_dir, 'apps', 'linode-marketplace-{}'.format(new_app_name)))
os.rename(os.path.join(gen_dir, 'deployment_scripts', 'linode-marketplace-app_name'),
          os.path.join(gen_dir, 'deployment_scripts', 'linode-marketplace-{}'.format(new_app_name)))

# Copy all things over to new branch
shutil.copytree(os.path.join(gen_dir, 'apps'), os.path.join(repo_directory, 'apps', 'linode-marketplace-{}'.format(new_app_name)))
shutil.copytree(os.path.join(gen_dir, 'deployment_scripts'), os.path.join(repo_directory, 'deployment_scripts', 'linode-marketplace-{}'.format(new_app_name)))

# Verify
app_directory = os.path.join(repo_directory, 'apps', 'linode-marketplace-{}'.format(new_app_name))
if os.path.exists(app_directory):
    print("The directory exists:", app_directory)
    print("All systems GO")
else:
    print("Error: The directory does not exist:", app_directory)
    print("Elvis or Pat Broke something....")
    os.sys.exit(1)

# Generation complete
print("Operation new Marketplace app, COMPLETE!")
