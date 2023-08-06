from firehelper import CommandRegistry
from tabulate import tabulate
from utils.db import (delete_empty_folders, list_all_notebooks, ws_export,
                      ws_import)


def clean_notebooks():
    notebook_list = list_all_notebooks()
    notebooks = ws_export(notebook_list, format='SOURCE')
    for notebook_path in notebooks:
        ws_import(path=notebook_path, **notebooks[notebook_path])
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
