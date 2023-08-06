# databricks-workspace-tool

dwt is a tool to clear run cells from notebooks, for example where there might be concern about data held in run cells, or as preparation for commit to source control.

You can also use it to import/export multiple notebooks with this capability, in use cases where dbc export may not be possible due to volume limits.

## Commands
|Command|Sub-Command|Parameters|Description|
|--------|---------|--------|--------|
|list|notebooks||List all notebooks in workspace.|
|list|libraries||List all libraries in workspace.|
|export|notebooks|path: location to output zip of notebooks|Exports all notebooks from a workspace as base64 source code. The process will remove annotations for run cells|
|import|notebooks|path: location of notebooks.zip<br>import_prefix: folder to import into (default: IMPORT)|Import notebooks into workspace.|
|clean|folders||Delete all empty folders in workspace.|
|clean|notebooks||Remove annotations for run cells from all notebooks in workspace.|

## Installation

In a python 3.7 environment install this repository, e.g: </br>
pip install git+https://github.com/frogrammer/fire-commands.git </br>
The tool can be installed to an azure cloud shell.

## Databricks Workspace Login

The dwt CLI is built using the databricks CLI sdk https://github.com/databricks/databricks-cli, and uses its authentication mechanism to login to a workspace.  </br>
To login to an azure databricks workspace using a user token:  </br>
```bash
echo MY_TOKEN >> token.txt
databricks configure --host MY_HOST -f token.txt
rm token.txt 
```
