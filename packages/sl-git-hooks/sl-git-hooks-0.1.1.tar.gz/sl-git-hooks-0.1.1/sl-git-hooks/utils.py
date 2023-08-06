import os
from pygit2 import GIT_SORT_TOPOLOGICAL


def get_script_location():
    return os.path.dirname(os.path.realpath(__file__))


def find_repo_hash(repository):
    repository_hash = None

    for commit in repository.walk(repository.head.target, GIT_SORT_TOPOLOGICAL):
        repository_hash = str(commit.oid)
        break

    return repository_hash
