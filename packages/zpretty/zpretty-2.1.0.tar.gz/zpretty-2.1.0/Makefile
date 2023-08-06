.PHONY: pytests test flake8 black

all: bin/pip
test: pytest

bin/pip:
	virtualenv -p python3 . || python3 -m venv .
	./bin/pip install -U pip
	./bin/pip install -U .[development,test]

pytest: bin/pip
	@echo "==== Running nosetests ===="
	./bin/pytest

flake8: bin/pip
	@echo "==== Running Flake8 ===="
	./bin/flake8 zpretty *.py

bin/black: requirements-dev.txt
	./bin/pip install -r requirements-dev.txt
	touch bin/black

black: bin/black
	./bin/black --check zpretty

requirements: bin/pip
	./bin/pip install -Ue .[development,test]
	./bin/pip freeze --all|egrep -v '^(pip|pkg-resources|wheel|-e|-f)' > requirements-dev.txt
	@git difftool -y -x "colordiff -y" requirements-dev.txt
