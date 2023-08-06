import click
import os
import git
from one.one import cli
from shutil import copy
from plugin_foundation.jinja2_env import exclude_dir, exclude_file, j2_env, get_config
from plugin_foundation.data import bubbletea_repos, exclude_files
from plugin_foundation.data import GIT, GITLAB_BASE_URL, BUBBLETEA_REPOSITORY_URL


def __init__():
    cli.add_command(foundation)


@click.group(help='Group of foundation commands.')
def foundation():
    pass


@foundation.command(name='clone', help='Clone DNX foundation.')
def clone():
    for repository in bubbletea_repos:
        if not os.path.exists('./' + repository):
            git.Git('./').clone(GITLAB_BASE_URL + BUBBLETEA_REPOSITORY_URL + repository + GIT)
            print('Cloned ' + repository)
        else:
            print('Skipping stack' + repository + ', folder already exist')


@foundation.command(name='start', help='Start DNX foundation config for stacks.')
@click.argument('source_dir')
@click.argument('dest_dir')
@click.option('--vars', 'vars_files',
              help='Vars file to load (can be passed multiple times)',
              required=False, multiple=True)
def start(source_dir, dest_dir, vars_files):
    cwd = os.getcwd()
    config = get_config(vars_files)

    for path, _, files in os.walk(source_dir):
        if exclude_dir(path):
            continue

        path_dest = path.replace(source_dir, dest_dir)
        os.makedirs(path_dest, exist_ok=True)

        for file in files:
            if exclude_file(file):
                continue

            file_src = os.path.join(os.path.sep, cwd, path, file)
            file_dest = os.path.join(os.path.sep, cwd, path_dest, file)

            file_name, file_extension = os.path.splitext(file)

            if file_extension == '.j2':
                # files with .j2 extension will override its counterpart
                output = j2_env.get_template(file_src).render(config)
                file_dest = os.path.join(os.path.sep, cwd, path_dest, file_name)
                with open(file_dest, 'w') as writer:
                    writer.write(output)
                exclude_files.append(file_name)

            else:
                copy(file_src, file_dest)

            print("COPY %s -> %s" % (file_src, file_dest))
