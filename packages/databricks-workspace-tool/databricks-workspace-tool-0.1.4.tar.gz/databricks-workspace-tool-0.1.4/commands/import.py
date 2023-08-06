import base64
import json
from zipfile import ZipFile
from firehelper import CommandRegistry
from utils.db import ws_import

def import_zip(path, import_root='IMPORT', overwrite=False, format='JUPYTER'):
    with ZipFile(path, 'r') as z:
        for fn in z.namelist():
            with z.open(fn) as f:
                content = base64.b64encode(f.read())
                path = '/{}{}'.format(import_root, '.'.join(fn.split('.')[:-2]))
                language = fn.split('.')[-2]
                ws_import(path, language, format, content, overwrite)
    print('done')
 
import_commands = {
    'import': {
        'zip': import_zip
    }
}

CommandRegistry.register(import_commands)
