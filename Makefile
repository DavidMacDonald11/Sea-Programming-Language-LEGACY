SHELL 		:= /bin/bash

LINT_ARGS	:= --disable=C0111
LINT_ARGS	+= --include-naming-hint=y
LINT_ARGS	+= --variable-rgx=^[a-z][a-z0-9]*\(\(_[a-z0-9]+\)*\)?$$
LINT_ARGS	+= --argument-rgx=^[a-z][a-z0-9]*\(\(_[a-z0-9]+\)*\)?$$
LINT_ARGS	+= --max-parents=15

PIP_MODULES	:= pylint pydocstyle pycodestyle mypy rope

CACHE 		:= $(wildcard $(patsubst %, %/**/__pycache__, .))
MODULES 	:= modules

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
	$(PYTHON) -m pylint $(LINT_ARGS) $(MODULES)

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
