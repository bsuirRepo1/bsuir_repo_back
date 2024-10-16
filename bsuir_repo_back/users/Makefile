MANAGE = python manage.py
DOCKER_LOAD_DATA = docker-compose exec backend python bsuir_repo_core/manage.py loaddata

.PHONY = run backend test

FILES = input output

.DEFAULT_COAL = help

 help:
	@echo "---------------HELP-----------------"
	@echo "To run the project type make run"
	@echo "To load fixtures after running containers type make test"
	@echo "------------------------------------"

run:
	sudo docker-compose up --build

backend:
	${MANAGE} collectstatic --noinput
	${MANAGE} makemigrations users
	${MANAGE} migrate

	docker-compose exec backend bsuir_repo_core/manage.py test

load_fixtures:
	# write a code to load fixtures here
