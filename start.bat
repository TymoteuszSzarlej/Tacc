@echo off
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
python .\Tacc\manage.py makemigrations
echo.
echo.
echo.
echo.
echo.
echo.
python .\Tacc\manage.py migrate
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo
python .\Tacc\manage.py runserver