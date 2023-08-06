from invisibleroads_macros_log import get_log
from os.path import expanduser


CLIENT_URL = 'https://crosscompute.com'
SERVER_URL = 'https://services.crosscompute.com'
BASH_CONFIGURATION_TEXT = '''
export CROSSCOMPUTE_CLIENT={client_url}
export CROSSCOMPUTE_SERVER={server_url}
export CROSSCOMPUTE_TOKEN={token}
'''.strip()


AUTOMATION_FILE_NAME = 'automation.yml'
TOOL_FILE_NAME = 'tool.yml'
RESULT_FILE_NAME = 'result.yml'
PROJECT_FILE_NAME = 'project.yml'


# TODO: Load supported views from server
VIEW_NAMES = [
    'text',
    'number',
    'markdown',
    'table',
    'image',
    'map',
    'electricity-network',
    'file',
]
DEFAULT_VIEW_NAME = 'text'


PRINT_FORMAT_NAMES = [
    'pdf'
]


DEBUG_VARIABLE_DEFINITIONS = [{
    'id': 'stdout',
    'name': 'Standard Output',
    'view': 'text',
    'path': 'stdout.txt',
}, {
    'id': 'stderr',
    'name': 'Standard Error',
    'view': 'text',
    'path': 'stderr.txt',
}]


S = {
    'folder': expanduser('~/.crosscompute'),
    'draft.id.length': 16,
    'maximum_variable_value_length': 1024,
}
L = get_log('crosscompute')
