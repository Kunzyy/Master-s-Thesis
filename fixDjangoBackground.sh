pip uninstall django-background-tasks
pip install django4-background-tasks

python manage.py makemigrations
python manage.py migrate

python manage.py runserver 8000
python manage.py process_tasks



