import base64
import json
import pathlib
import os
from zipfile import ZipFile

from firehelper import CommandRegistry
from utils.db import list_all_notebooks, ws_export_list


def export_zip(path, format='JUPYTER'):  # formats: https://docs.databricks.com/dev-tools/api/latest/workspace.html#notebookexportformat
    notebook_list = list_all_notebooks()
    notebooks = ws_export_list(notebook_list, format)

    with ZipFile(path, 'w') as z:
        for notebook in notebooks:
            content = base64.b64decode(notebook['obj']['content'])
            z.writestr('{}.{}.{}'.format(notebook['path'], notebook['language'].lower(), notebook['obj']['file_type']), content)
    print('done')
    
def export_folder(root, format='JUPYTER'):  # formats: https://docs.databricks.com/dev-tools/api/latest/workspace.html#notebookexportformat
    notebook_list = list_all_notebooks()
    notebooks = ws_export_list(notebook_list, format)

    for notebook in notebooks:
        full_path = os.path.join(root, notebook['path'][1:])
        file_path = '{}.{}.{}'.format(full_path, notebook['language'].lower(), notebook['obj']['file_type'])
        pathlib.Path('/'.join(file_path.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
        content = base64.b64decode(notebook['obj']['content'])
        with open(file_path, 'wb') as f:
            f.write(content)
    print('done')

export_commands = {
    'export': {
        'zip': export_zip,
        'folder': export_folder
    }
}

CommandRegistry.register(export_commands)
