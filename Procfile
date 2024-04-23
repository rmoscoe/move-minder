web: gunicorn cd move_minder && move_minder.wsgi --log-file -
release: python move_minder/manage.py tailwind build && python move_minder/manage.py makemigrations && python move_minder/manage.py migrate
