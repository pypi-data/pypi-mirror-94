from commands import *  # noQA
from databricks_cli.utils import InvalidConfigurationError
from firehelper import start_fire_cli


def main():
    try:
        start_fire_cli('dwt')
    except InvalidConfigurationError:
        print('Please configure databricks CLI using command "databricks configure --token".')
        pass

if __name__ == '__main__':
    main()
