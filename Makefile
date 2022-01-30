SHELL 		:= /bin/bash

PIP_MODULES	:= pylint pydocstyle pycodestyle mypy rope

CACHE 		:= $(wildcard $(patsubst %, %/modules/**/__pycache__, .))
INITS		:= $(wildcard $(patsubst %, %/modules/*/__init__.py, .))
MODULES		:= $(patsubst ./modules/%/__init__.py, %, $(INITS))

VENV 		:= venv
PY			:= python3
PYTHON 		:= ./$(VENV)/bin/$(PY)

.DEFAULT_GOAL := run

$(VENV):
	$(PY) -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install $(PIP_MODULES)

.git:
	git init
	git add .
	git commit -m "Create initial project"

.PHONY: activate
activate: $(VENV)
	source $(VENV)/bin/activate

.PHONY: init
init: activate .git

.PHONY: run
run: $(VENV) activate
	./sea.bash

.PHONY: lint
lint: $(VENV) activate
	$(PYTHON) -m pylint --rcfile=.pylintrc $(MODULES)

.PHONY: full_lint
full_lint: $(VENV) activate
	$(PYTHON) -m pylint $(MODULES)

.PHONY: deep
deep:
	-$(RM) -r $(VENV)

.PHONY: clean
clean:
	-$(RM) -r $(CACHE)
	cd bin; ./clean.bash
	cd output; ./clean.bash

.PHONY: update
update:
	git push
	sea -u
