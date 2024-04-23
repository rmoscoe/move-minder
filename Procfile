web: gunicorn move_minder.wsgi --log-file -
release: cd move_minder/theme/static_src && npm install && cd ../../.. && python move_minder/manage.py tailwind build && python move_minder/manage.py collectstatic && python move_minder/manage.py makemigrations && python move_minder/manage.py migrate
