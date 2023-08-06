from firehelper import CommandRegistry
from tabulate import tabulate
from utils.db import (delete_empty_folders, list_all_notebooks, ws_export_list,
                      ws_import)


def clean_notebooks():
    notebook_list = list_all_notebooks()
    notebooks = ws_export_list(notebook_list)
    for notebook in notebooks:
        ws_import(path=notebook['path'], **notebook['obj'])
    print(tabulate(notebook_list))

def clean_empty_folders():
    folders = delete_empty_folders()
    print(tabulate(folders))



clean_commands = {
    'clean': {
        'notebooks': clean_notebooks,
        'folders': clean_empty_folders
    }
}

CommandRegistry.register(clean_commands)
