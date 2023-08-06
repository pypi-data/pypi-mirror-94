import json
from zipfile import ZipFile
from firehelper import CommandRegistry
from utils.db import ws_import


def import_notebooks(path = 'notebooks.zip', import_prefix = 'IMPORT'):
    with ZipFile(path, 'r') as z:
        for fn in z.namelist():
            with z.open(fn) as f:
                notebook_obj = json.loads(f.read())
                notebook_obj['path'] = '/' + import_prefix + notebook_obj['path']
                ws_import(notebook_obj)
    print('done')
 
import_commands = {
    'import': {
        'zip': import_zip
    }
}

CommandRegistry.register(import_commands)
