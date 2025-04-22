
@echo off

REM Set the path to your virtual environment
set VENV_PATH=D:\programing\python\online_shop

REM Activate the virtual environment
call "%VENV_PATH%\Scripts\activate.bat"

REM CD IN DIR
cd D:\programing\python\online_shop\online-shop-django

REM Run the Django development server
py manage.py runserver

REM Pause to keep the terminal open
pause
