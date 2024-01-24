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

# Find and replace in files
for root, dirs, files in os.walk(gen_dir):
    if '.git' in dirs:
        dirs.remove('.git')  # Exclude the .git directory from further processing
    for file in files:
        file_path = os.path.join(root, file)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        content = content.replace('app_name', new_app_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

# Replace in directory names
for root, dirs, files in os.walk(gen_dir):
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        new_dir_path = dir_path.replace('app_name', new_app_name)
        os.rename(dir_path, new_dir_path)

# Copy directories to the new branch
apps_dest_path = os.path.join(repo_directory, 'apps', f'linode-marketplace-{new_app_name}')
deployment_scripts_dest_path = os.path.join(repo_directory, 'deployment_scripts', f'linode-marketplace-{new_app_name}')

shutil.copytree(os.path.join(gen_dir, 'apps', f'linode-marketplace-{new_app_name}'), apps_dest_path)
shutil.copytree(os.path.join(gen_dir, 'deployment_scripts', f'linode-marketplace-{new_app_name}'), deployment_scripts_dest_path)

# Update roles directory
roles_dest_path = os.path.join(repo_directory, 'apps', f'linode-marketplace-{new_app_name}', 'roles')
for root, dirs, files in os.walk(roles_dest_path):
    for file in files:
        file_path = os.path.join(root, file)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Replace 'app_name' with the new app name
        content = content.replace('app_name', new_app_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # Rename the 'app_name' directory to the new app name
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        new_dir_path = os.path.join(root, dir_name.replace('app_name', new_app_name))
        os.rename(dir_path, new_dir_path)

print("Updated 'app_name' in role files and directory names.")

# Update deployment script files if they exist
deploy_script_path = os.path.join(repo_directory, 'deployment_scripts', f'linode-marketplace-{new_app_name}', 'app_name-deploy.sh')
new_deploy_script_path = os.path.join(repo_directory, 'deployment_scripts', f'linode-marketplace-{new_app_name}', f'{new_app_name}-deploy.sh')

if os.path.exists(deploy_script_path):
    # Use shutil.move to rename the file
    shutil.move(deploy_script_path, new_deploy_script_path)
    print(f"Updated deployment script: {new_deploy_script_path}")
else:
    print(f"Warning: Deployment script file not found at {deploy_script_path}. Make sure it exists.")

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
