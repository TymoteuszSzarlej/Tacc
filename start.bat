echo '\n\n\n\n\n\n\n\n\n\n'
python .\Tacc\manage.py makemigrations
echo '\n\n\n\n\n\n'
echo '\n\n\n\n\n\n'
python .\Tacc\manage.py migrate
echo '\n\n\n\n\n\n\n\n\n\n'
python .\Tacc\manage.py runserver