# asmo.d/utils/py_utils/generate_howto_deploy.py
# version 2025-01-09
import argparse
import os
from pathlib import Path

from loguru import logger

RUN_SAMPLE = """
python generate_howto_deploy.py -w www.url.to.site -r https://github.com/path/to/repo [-o output_directory]
"""

HOWTO_TEMPLATE = """
# prepare for deploy snippet
# project_name: {project_name}
# repo_url    : {repo_url}
# git_url     : {git_url}
# www_domain  : {www_domain}

# generate ssh key in server for gitlab
ssh-keygen -b 2048 -t rsa -f ~/.ssh/deploy_key_{project_name} -C deploy_key_{project_name} -q -N ""

# add ssh key to gitlab deploy keys
cat ~/.ssh/deploy_key_{project_name}.pub
# gitlab case
# {repo_url}/-/settings/repository#js-deploy-keys-settings
# github case
# {repo_url}/settings/keys/new

# to clone
GIT_SSH_COMMAND='ssh -i ~/.ssh/deploy_key_{project_name}' git clone {git_url}

# to run
cd {project_name}
git config core.sshCommand "ssh -i ~/.ssh/deploy_key_{project_name} -F /dev/null"
cp dc.d/.env.example dc.d/.env
vim dc.d/.env
make up

# add site config to nginx
rm -rf /etc/nginx/sites-available/{www_domain} /etc/nginx/sites-enabled/{www_domain}
ls -alsht asmo.d/sites/{www_domain}
cp asmo.d/sites/{www_domain} /etc/nginx/sites-available/{www_domain}
ln -s /etc/nginx/sites-available/{www_domain} /etc/nginx/sites-enabled/{www_domain}
nginx -t && nginx -s reload

# add site config to certbot
certbot --nginx -d {www_domain} --non-interactive --agree-tos --redirect --email ssl@asmo.su --no-eff-email
nginx -t && nginx -s reload

# make sure that the certificates are installed otherwise cloudflare will show host error page

#  brute force
systemctl restart nginx
"""


def validate_repo_url(repo_url):
    if not repo_url.startswith(("https://gitlab.com/", "https://github.com/")):
        raise argparse.ArgumentTypeError(
            "Repo URL must start with 'https://gitlab.com/' or 'https://github.com/'"
        )
    return repo_url


def validate_output_dir(directory):
    """Validate and create output directory if it doesn't exist."""
    path = Path(directory)
    try:
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
    except Exception as e:
        raise argparse.ArgumentTypeError(
            f"Error creating directory {directory}: {str(e)}"
        )


def parse_args():
    parser = argparse.ArgumentParser(description="Process a domain and a Git URL.")

    parser.add_argument("-w", "--www_domain", help="The domain, must start with 'www.'")
    parser.add_argument("-r", "--repo_url", type=validate_repo_url, help="The Repo URL")
    parser.add_argument(
        "-o",
        "--output",
        type=validate_output_dir,
        default=".",
        help="Output directory (default: current directory)",
    )

    args = parser.parse_args()
    return args.www_domain, args.repo_url, args.output


def main():
    www_domain, repo_url, output_dir = parse_args()
    logger.info(f"{(www_domain, repo_url, output_dir)=}")

    if not repo_url:
        print(RUN_SAMPLE)
        return

    project_name = repo_url.strip("/").split("/")[-1]

    if "gitlab" in repo_url:
        git_url = repo_url.replace("https://gitlab.com/", "git@gitlab.com:") + ".git"
    elif "github" in repo_url:
        git_url = repo_url.replace("https://github.com/", "git@github.com:") + ".git"
    else:
        raise ValueError("unsupported repo_url")

    template = HOWTO_TEMPLATE.format(
        www_domain=www_domain,
        repo_url=repo_url,
        project_name=project_name,
        git_url=git_url,
    )

    output_file = os.path.join(output_dir, "howto.deploy.txt")
    with open(output_file, "w") as f:
        f.write(template)

    logger.success(f"howto.deploy.txt generated in {output_dir}")


if __name__ == "__main__":
    main()
