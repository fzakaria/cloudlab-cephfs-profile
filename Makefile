PHONY: install lint freeze run

venv:
	test -d venv || virtualenv venv

requirements.txt: venv
	. venv/bin/activate && pip install -r requirements.txt

install: requirements.txt

venv/bin/yapf: # Installs yapf code formatter
	venv/bin/pip install -U yapf

venv/bin/flake8: # Installs flake8 code linter
	venv/bin/pip install -U flake8

lint: install venv/bin/flake8 venv/bin/yapf
	venv/bin/yapf --diff --recursive --exclude=venv .
	venv/bin/flake8 --exclude 'venv' .

format: install venv/bin/yapf
	venv/bin/yapf --in-place --recursive --exclude=venv .

freeze: install
	venv/bin/pip freeze > requirements.txt .

run: install
	venv/bin/python profile.py