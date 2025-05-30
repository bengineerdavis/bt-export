.PHONY: help
.DEFAULT_GOAL := help

SCRIPT := sawmill
PYTHON := $$(pyenv which python)
PY_VERSION := 3.11
VENV_NAME := bt-export-dev

INSTALL_DIR := ../

define PRINT_HELP_PYSCRIPTpyen
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: clean clean-venv
clean: clean-venv  ## cleans up all python caching and other artifact files, including removal of the local venv for this directory
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.log' -exec rm -fr {} +

clean-venv:  # removes auto-activation of venv and then deletes the venv T3RAP environment
	if [ -f .python-version ]; then \
    	printf '.python-version found!\n\n\n' && \
		pyenv local --unset && \
		pyenv virtualenv-delete -f $(VENV_NAME); \
	else \
		echo '.python-version not found!'; \
	fi


.PHONY: check
check:  ## confirms that a pyenv virtual environment is activated
	@echo "check for successfully created and activated Python venv or stopping make command ..."
	if [ ! -f .python-version ]; then \
    	echo '.python-version not found! .python-version is missing -- pyenv virtual environment is not activated' && \
		exit 1; \
	else \
		echo 'Confirmed that a pyenv Python virtual environment is activated!'; \
	fi


.PHONY: update
update: check  ## use to update venv's Python dependencies and auxiliary tools; also updates user-wide pipx installation of t3reports
	@echo "using pipx to update poetry"
	pipx upgrade poetry
	pipx upgrade pre-config

	@update pip
	python -m pip install --upgrade pip

	@echo "Updating requirements with poetry"
	poetry update


.PHONY: venv venv-update install
venv:  ## create a fresh, dedicated venv for the T3RAP local repo and t3report app with pyenv-virtualenv plugin
	@echo "Making sure that Python version $(PY_VERSION) has been installed by pyenv!"
	pyenv install --skip-existing $(PY_VERSION)

	@echo "Creating a fresh virtualenv is install for the $(VENV_NAME) directory with Python version $(PY_VERSION)"
	pyenv virtualenv $(PY_VERSION) $(VENV_NAME)

	@echo "Assigning the $(VENV_NAME) venv to the current directory"
	pyenv local $(VENV_NAME)


install: clean venv  ## fresh developer installation of the t3reports app and Python dependencies
	@echo "installing Python dependencies with poetry"
	poetry install --extras dev

	# @echo "installing Node.js dependencies for Mermaid.js markdown diagrams with pnpm"
	# pnpm install

	@echo "installing pre-commit hooks"
	pre-commit install

.PHONY: tests
tests:  ## run all tests for the t3reports app
	poetry run pytest -v -n auto

# TODO: attempt to move part of these tests into merge pre-commit hooks
.PHONY: watch
watch:  ## run all tests for the sawmill app in watch mode; source: https://stackoverflow.com/a/63148860
	poetry run ptw . -v -n auto --xdoctest --picked --testmon

# TODO: add to both pre-commit and pre-merge hooks
.PHONY: check
check:  ## run all pre-commit checks
	pre-commit run --all-files

.PHONY: demo
TEST_FILE := 'test_files/1d4c79af_c5c3_4b7c_9347_beb5eda819e8_job_10344_attempt_1_txt.txt'
demo:  ## run the demo script

	$(SCRIPT) view $(TEST_FILE)
