# marketplace-gen-template
This repo will accelerate the creation of new apps in the Akamai Connected Cloud Marketplace Repository.

https://github.com/akamai-compute-marketplace/marketplace-apps 

# How to Use Marketplace-gen-template
This script will require you to pull down the gitgen.py onto your local machine. To run this script, you will need to have python3 installed along with having your own fork of Akamai Marketplace repository already setup on your machine with proper remote upstream configured.

The gitgen.py includes variables that you will need to update to reflect where you've configured the Akamai Marketplace repository. For the example below, my Akamai Marketplace repository is configured `~/Projects/marketplace-apps`. 

https://github.com/hmorris3293/marketplace-gen-template/blob/main/gitgen.py#L37
```
# Variables
repo_directory = os.path.expanduser("~/Projects/marketplace-apps")
gen_repo = "https://github.com/hmorris3293/marketplace-gen-template.git"
gen_dir = "/tmp/marketplace-gen-template"
```

This script will handle creating the git branch for the new app you're working on. To ensure it follows the correct git workflow the script does the following (in order):

```
git checkout develop # start with develop
git fetch upstream # fetch upstream develop to ensure you're starting with the latest code
git merge upstream/develop # merge current upstream develop to your local develop
git checkout -b app_name-UUID # creates the branch with appname and random 4 char uuid to avoid branch name collision
```
Once you have gitgen.py variable updated, you are ready to run! Here is how you run the script:

```
Usage: python3 pythongitgen.py <new_app_name>
Example: python3 pythongitgen.py wordpress
```

Caveats: If an app already exists in the Akamai Marketplace repository, the script will not run and will output the following:

```
python3 pythongitgen.py docker
Error: The directory ~/Projects/marketplace-apps/apps/linode-marketplace-docker already exists. App creation aborted.
```

