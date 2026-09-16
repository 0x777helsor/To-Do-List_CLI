# Task CLI

A dependency-free Python command-line application for adding, viewing, and deleting tasks. Tasks persist in a JSON file in the user's home directory by default.

## Requirements

    Python 3.9 or later

## Commands

> bash
###  Add a task
• a python task_cli.py add "Ship the CLI prototype"

### View tasks
• python task_cli.py list
### `view` is an alias for `list`

### Delete a task by its displayed ID
• python task_cli.py delete 1
### `remove` and `rm` are aliases

### Make script(file)executable as standalone
• chmod +x task_cli.py

• ./task_cli.py add "[Task]"

># Use a project-local task file

bash
python task_cli.py --store tasks.json add "Write tests"
python task_cli.py --store tasks.json list
python task_cli.py --store tasks.json delete 1

The default storage location is ~/.task_cli_tasks.json.
