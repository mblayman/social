.PHONY: local

local:
	heroku local

deploy:
	git push heroku main

graph:
	./manage.py graph_models \
		users \
		invites \
		-o models.png

coverage:
	coverage run --source='social' -m pytest --migrations
	coverage report

mypy:
	mypy social project manage.py
