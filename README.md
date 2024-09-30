# cudocpy | A ClickUp DOCs extractor for Python

Extract all files and data from a CU workspace by traversing the documents.

## Description

**cudocpy** is a command-line interface (CLI) tool designed for extracting all documents from a ClickUp workspace. It allows users to specify the workspace, user, and paths for storing the extracted documents and associated media. This tool is particularly useful for backups, migrations, or data analysis.

## Features

- Extract documents from a specified ClickUp workspace.
- Automatically use the current working directory if no base path is provided.
- Store media files in a specified or default sub-directory.
- Utilize parameters provided via command line or defaults from environment variables.

## Installation

Clone the repository and install the required dependencies.

```bash
git clone https://github.com/yourusername/cudocpy.git
cd cudocpy
pip install -r requirements.txt
```

## Usage

Run the CLI tool with various options to customize the extraction process.

```bash
python main.py [options]
```

### Options

- `-w`, `--workspace_id` (optional): Specify the Workspace ID. If not provided, the ID from the environment variable is used.
- `-u`, `--user` (optional): Specify the User ID.
- `-bp`, `--base_path` (optional): Specify the base path for storing extracted documents. Defaults to the current working directory.
- `-mp`, `--media_path` (optional): Specify the media path for storing associated media files. Defaults to a `media` sub-directory in the base path.

### Examples

Extract all documents using default settings:

```bash
python main.py
```

Specify a workspace ID and base path:

```bash
python main.py -w your_workspace_id -bp /path/to/base
```


## Code Overview

The `main.py` script handles the argument parsing and calls the `get_and_store_docs` function from the `utility` module to perform the extraction. Default values are used if certain arguments are not provided, ensuring a smooth user experience.


## License

License file will be included soon.

For any issues or suggestions, please open an issue on the [GitHub repository](https://github.com/renerichter/cudocpy).