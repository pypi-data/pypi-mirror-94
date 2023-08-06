import jinja2
import os
import json
import yaml
from jinja2 import contextfilter, Markup
import fnmatch
from plugin_foundation.data import exclude_dirs, exclude_files


def exclude_dir(path):
    for exclude_dir in exclude_dirs:
        for path_part in path.split('/'):
            if fnmatch.fnmatch(path_part, exclude_dir):
                return True
    return False


def exclude_file(file):
    for exclude_file in exclude_files:
        if fnmatch.fnmatch(file, exclude_file):
            return True
    return False


def get_config(vars_files):
    config = {}
    for vars_file in vars_files:
        try:
            with open(vars_file, 'r') as stream:
                _, vars_file_extension = os.path.splitext(vars_file)
                if vars_file_extension == '.json':
                    config.update(json.load(stream))
                elif vars_file_extension == '.yml' or vars_file_extension == '.yaml':
                    config.update(yaml.safe_load(stream))
                else:
                    exit('Vars file not reconized (only json or yaml supported)')
        except Exception as e:
            exit('Output file %s not found or not JSON. (Error: %s)' % (vars_file, e))
    return config


@contextfilter
def subrender_filter(context, value):
    _template = context.eval_ctx.environment.from_string(value)
    result = _template.render(**context)
    if context.eval_ctx.autoescape:
        result = Markup(result)
    return result


# Creating jinja2 Environment
j2_env = jinja2.Environment(
    extensions=['jinja2_ansible_filters.AnsibleCoreFiltersExtension'],
    loader=jinja2.FileSystemLoader('/'),
    trim_blocks=True,
    # block_start_string='#{',
    # block_end_string='#}',
    # line_statement_prefix='/*',
    # line_comment_prefix='*/',
    keep_trailing_newline=True
)

j2_env.filters['subrender'] = subrender_filter
