from databricks_cli.configure import provider as db_cfg
from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.sdk.service import WorkspaceService
from requests.exceptions import HTTPError

from utils.stdout import *


def get_config():
    return db_cfg.get_config()

def get_client():
    cfg = get_config()
    api_opts = {
        'user': cfg.username,
        'password': cfg.password,
        'host': cfg.host,
        'token': cfg.token
    }

    return ApiClient(**api_opts)

def __list_all(delete_empty_folders = False):
    cli = get_client()
    ws = WorkspaceService(cli)
    all_obj = ws.list('/')['objects']
    empty_folders = []
    while len([o for o in all_obj if o['object_type'] == 'DIRECTORY']):
        for dir in [o for o in all_obj if o['object_type'] == 'DIRECTORY']:
            stdout_print('Searching {0}\r'.format(dir['path']))
            dir_obj = []
            try:
                dir_obj = ws.list(dir['path'])['objects']
            except KeyError:
                if delete_empty_folders:
                    try:
                        ws.delete(dir['path'])
                        empty_folders = empty_folders + [dir]
                        stdout_print('Deleted {0}\r'.format(dir['path']))
                    except HTTPError as e:
                        if 'error_code' in e.response.json() and e.response.json()['error_code'] == 'DIRECTORY_NOT_EMPTY':
                            pass
                        else:
                            raise e
                pass

            all_obj = all_obj + dir_obj
            all_obj.remove(dir)
            del dir
    if delete_empty_folders:
        return (all_obj, empty_folders)
    else:
        return all_obj


def list_all_notebooks():
    all_obj = __list_all()
    return [o for o in all_obj if o['object_type'] == 'NOTEBOOK']


def list_all_libraries():
    all_obj = __list_all()
    return [o for o in all_obj if o['object_type'] == 'LIBRARY']

def ws_export(path, format='SOURCE'):  # formats: https://docs.databricks.com/dev-tools/api/latest/workspace.html#notebookexportformat
    cli = get_client()
    ws = WorkspaceService(cli)
    stdout_print('Exporting {0}\r'.format(path))
    return ws.export_workspace(path, format=format)

def ws_export_list(list_of_notebooks: list, format='SOURCE'):
    for notebook in list_of_notebooks:
        notebook['obj'] = ws_export(notebook['path'], format=format)
        yield notebook

def ws_import(path, language, format, content, overwrite=False):
    cli = get_client()
    ws = WorkspaceService(cli)

    if path[0] == '/':
        folder_structure = path.split('/')
        if len(folder_structure) > 2:
            folder = '/'.join(folder_structure[:-1])
            stdout_print('Creating folder {0}\r'.format(folder))
            ws.mkdirs(folder)
    stdout_print('Importing {0}\r'.format(path))
    ws.import_workspace(content=str(content, encoding='UTF-8'), path=path, language=language, format=format, overwrite=overwrite)


def delete_empty_folders():
    _, folders = __list_all(delete_empty_folders=True)
    return folders
