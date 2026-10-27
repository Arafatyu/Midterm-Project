 Python Calculator

A command-line calculator written in Python. It supports 10 operations, undo/redo,
calculation history saved to CSV with pandas, and logging.

## Features
- Operations: add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff
- Factory pattern (operations), Memento pattern (undo/redo), Observer pattern (logging and auto-save)
- History saved and loaded with pandas
- Settings in a `.env` file

## Installation Instructions
```bash
git clone <git@github.com:Arafatyu/Midterm-Project.git>
cd project_root
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Configuration Setup
Create a `.env` file in the project_root
Add the following:
```
CALCULATOR_LOG_DIR=logs
CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_HISTORY_DIR=history
CALCULATOR_HISTORY_FILE=history.csv
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=4
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```
## Usage Guide
 
Start the calculator:
 
```
python3 main.py
```
 
Then type a command at the `calc>` prompt.
 
| Command | Example | What it does |
|---|---|---|
| add | `add 2 3` | Adds two numbers |
| subtract | `subtract 5 3` | Subtracts the second number from the first |
| multiply | `multiply 4 3` | Multiplies two numbers |
| divide | `divide 10 4` | Divides the first number by the second |
| power | `power 2 3` | Raises 2 to the power of 3 |
| root | `root 27 3` | Takes the 3rd root of 27 |
| modulus | `modulus 10 3` | Gives the remainder of 10 / 3 |
| int_divide | `int_divide 7 2` | Division without the decimal part |
| percent | `percent 50 200` | Calculates (50 / 200) * 100 |
| abs_diff | `abs_diff 3 10` | Absolute difference between two numbers |
| history | `history` | Shows past calculations |
| clear | `clear` | Clears the history |
| undo | `undo` | Undoes the last calculation |
| redo | `redo` | Redoes the last undone calculation |
| save | `save` | Saves history to a CSV file |
| load | `load` | Loads history from the CSV file |
| help | `help` | Shows the list of commands |
| exit | `exit` | Quits the calculator |
 
 ## Testing Instructions
 
Run the tests:
 
```
python -m pytest
```
 
Run the tests and check coverage (the project needs at least 90%):
 
```
python -m pytest --cov=app --cov-report=term-missing
```
## CI/CD Information
 
A GitHub Actions workflow in `.github/workflows/python-app.yml` runs on every
push or pull request to the `main` branch. It installs the packages, runs the
tests with pytest, and fails if test coverage is below 90%.