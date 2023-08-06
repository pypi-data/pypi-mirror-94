from utils.db import list_all_notebooks, list_all_libraries
from firehelper import CommandRegistry
from tabulate import tabulate

def list_notebooks():
    notebooks = list_all_notebooks()
    print(tabulate(notebooks))

def list_libraries():
    libraries = list_all_libraries()
    print(tabulate(libraries))

list_commands = {
    'list': {
        'notebooks': list_notebooks,
        'libraries': list_libraries
    }
}

CommandRegistry.register(list_commands)
