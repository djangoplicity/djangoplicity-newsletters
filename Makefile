bash:
	docker exec -it djangoplicity-newsletters-web bash

test:
	docker exec -it djangoplicity-newsletters-web coverage run --source='.' manage.py test

coverage-html:
	docker exec -it djangoplicity-newsletters-web coverage html
	open ./htmlcov/index.html

test-python27:
	docker exec -it djangoplicity-newsletters-web tox -e py27-django111

migrate:
	docker exec -it djangoplicity-newsletters-web python manage.py migrate

makemigrations:
	docker exec -it djangoplicity-newsletters-web python manage.py makemigrations
