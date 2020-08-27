default:
	python manage.py runserver 0.0.0.0:8010

uwsgi:
	uwsgi --ini uwsgi.ini

test_uwsgi:
	uwsgi --http :8011 --wsgi-file test.py

clean:
	find . -type d -name __pycache__ | xargs rm -rf
	find . -type d -name migrations | xargs rm -rf
	rm debug.log
