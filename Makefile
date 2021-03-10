SHELL 		:= /bin/bash

LINT_ARGS	:= --disable=C0111
LINT_ARGS   += --include-naming-hint=y
LINT_ARGS	+= --variable-rgx=^[a-z][a-z0-9]*\(\(_[a-z0-9]+\)*\)?$$
LINT_ARGS	+= --argument-rgx=^[a-z][a-z0-9]*\(\(_[a-z0-9]+\)*\)?$$

PIP_MODULES	:= pylint pydocstyle pycodestyle mypy rope

CACHE 		:= $(wildcard $(patsubst %, %/modules/*/__pycache__, .))
INITS		:= $(wildcard $(patsubst %, %/modules/*/__init__.py, .))
MODULES 	:= $(patsubst %/__init__.py, %, $(INITS))

VENV 		:= venv
PY 			:= python3
PYTHON 		:= ./$(VENV)/bin/$(PY)
MAIN 		:= main.py

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
	$(PYTHON) main.py

.PHONY: lint
lint: $(VENV) activate
	$(PYTHON) -m pylint $(LINT_ARGS) $(MAIN) $(MODULES)

.PHONY: full_lint
full_lint: $(VENV) activate
	$(PYTHON) -m pylint $(MAIN) $(MODULES)

.PHONY: deep
deep:
	-$(RM) -r $(VENV)

.PHONY: clean
clean:
	-$(RM) -r $(CACHE)
