@echo off

set VENV_DIR=env

if not exist %VENV_DIR% (
    python -m venv %VENV_DIR%
)

call %VENV_DIR%\Scripts\activate

pip install -r requirements.txt

set FLASK_APP=app.py 

flask run