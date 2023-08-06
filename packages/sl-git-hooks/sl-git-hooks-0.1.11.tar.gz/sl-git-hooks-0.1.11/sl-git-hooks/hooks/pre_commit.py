import pygit2

import os
import sys

import config
import utils


def precommitHandler():
    print('Precommit hook!')

    cwd = os.getcwd()

    repository = pygit2.Repository(cwd)
    project_config = config.find_config_by_repo_hash(utils.find_repo_hash(repository))

    if project_config.getboolean('profile', 'enabled'):
        username = repository.config["user.name"]
        email = repository.config["user.email"]

        project_name = project_config.get('profile', 'name')
        project_email = project_config.get('profile', 'email')

        if username != project_name:
            print(f'[ERROR] git user.name expected {project_name}, got {username}')
            sys.exit(1)

        if email != project_name:
            print(f'[ERROR] git user.email expected {project_email}, got {email}')
            sys.exit(1)

    return 0
