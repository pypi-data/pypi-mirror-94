import configparser
import os

import sl_git_hooks.utils as utils


def find_config_by_repo_hash(repo_hash):
    configs_path = os.path.join(utils.get_script_location(), 'configs')

    directory = os.listdir(configs_path)

    config_path = ''

    for filename in directory:
        filepath = os.path.join(configs_path, filename)
        if os.path.isfile(filepath):
            file = open(filepath, 'r')

            if repo_hash in file.read():
                print(f'Matched config ${filepath}')
                config_path = filepath
                break

    if config_path == '':
        return None

    config = configparser.ConfigParser()
    config.read(os.path.join(configs_path, config_path))

    return config


def generate_project_config(repository, interactive=True):
    global_config = repository.config.get_global_config()

    repository_hash = utils.find_repo_hash(repository)
    project_name = ''
    project_id = ''

    profile_enabled = 'off'
    profile_name = global_config['user.name']
    profile_email = global_config['user.email']

    if interactive:
        project_name = input('Enter project name (default: empty): ') or ''
        project_id = input('Enter project\'s internal ID (default: empty): ' or '')

        profile_enabled = input('Enable git profile check? (default: False) (on/off): ') or 'off'

        if profile_enabled:
            profile_name = input(f'Enter git profile name (default: {profile_name}): ') or profile_name
            profile_email = input(f'Enter git profile email (default: {profile_email}): ') or profile_email

    parser = configparser.SafeConfigParser()

    parser.add_section('general')
    parser.set('general', 'repository_hash', repository_hash)
    parser.set('general', 'project_name', project_name)
    parser.set('general', 'project_id', project_id)

    parser.add_section('profile')
    parser.set('profile', 'enabled', profile_enabled)
    parser.set('profile', 'name', profile_name)
    parser.set('profile', 'email', profile_email)

    filename = repository_hash

    if project_name != '': filename = project_name

    file = open(os.path.join(utils.get_script_location(), 'configs', f'{filename}.ini'), 'w')

    parser.write(file)

    file.close()