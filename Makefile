MANAGE=src/manage.py
SETTINGS=yam.settings

install:
	pip install -r requirements.txt

test:
	python $(MANAGE) test
	flake8 --exclude '*migrations*' --ignore=F403
