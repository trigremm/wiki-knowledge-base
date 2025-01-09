# gitlab/clone_all_group_projects/clone_all_group_projects.py
import os

from env_variables import ACCESS_TOKEN, CLONE_DIR, GROUP_ID

import gitlab

# Setup
gl = gitlab.Gitlab("https://gitlab.com", private_token=ACCESS_TOKEN)
group = gl.groups.get(GROUP_ID)

# Ensure the clone directory exists
os.makedirs(CLONE_DIR, exist_ok=True)

# Clone each project
for project in group.projects.list(all=True):
    os.system(f"git clone {project.ssh_url_to_repo} {os.path.join(CLONE_DIR, project.path)}")
