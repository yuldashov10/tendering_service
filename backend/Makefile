FILES = api/ core/ organizations/ tenders/ users/ backend/urls.py
VALIDATORS = flake8 pylint mypy

dev-pep8:
	isort $(FILES);
	black $(FILES);

dev-pep8-check:
	for validator in $(VALIDATORS); do \
		echo "\n\nChecking $$validator"; \
		$$validator $(FILES); \
	done;

dj-migrations:
	python manage.py makemigrations

dj-migrate:
	python manage.py makemigrations users
	python manage.py migrate

dj-user:
	python manage.py createsuperuser

dj-run:
	python manage.py runserver
