import base64
import json
import pathlib
import os
from zipfile import ZipFile

from firehelper import CommandRegistry
from utils.db import list_all_notebooks, ws_export


def export_zip(path:str = 'notebooks.zip', format='JUPYTER'):  # formats: https://docs.databricks.com/dev-tools/api/latest/workspace.html#notebookexportformat
    notebook_list = list_all_notebooks()
    notebooks = ws_export(notebook_list, format)
    with ZipFile(path, 'w') as z:
        for notebook_path in notebooks:
            content = base64.b64decode(notebooks[notebook_path]['content'])
            z.writestr('{0}.{1}'.format(notebook_path, notebooks[notebook_path]['file_type']), content)
    print('done')
    
def export_folder(root:str = './notebooks', format='JUPYTER'):  # formats: https://docs.databricks.com/dev-tools/api/latest/workspace.html#notebookexportformat
    notebook_list = list_all_notebooks()
    notebooks = ws_export(notebook_list, format)
    for notebook_path in notebooks:
        full_path = os.path.join(root, notebook_path[1:])
        file_path = '{}.{}'.format(full_path, notebooks[notebook_path]['file_type'])
        pathlib.Path('/'.join(file_path.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
        content = base64.b64decode(notebooks[notebook_path]['content'])
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
