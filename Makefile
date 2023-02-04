.ONESHELL:
ENV_PREFIX=$(shell python3 -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

info:
	@echo "Current environment:"
	@echo "Running using $(ENV_PREFIX)"
	
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

show:             ## Show the current environment.
	@echo "Current environment:"
	@echo "Running using $(ENV_PREFIX)"
	@$(ENV_PREFIX)python -V
	@$(ENV_PREFIX)python -m site

install:          ## Install the project in dev mode.
	$(ENV_PREFIX)pip install pipenv
	PIPENV_VENV_IN_PROJECT=1 $(ENV_PREFIX)pipenv install --deploy
	PIPENV_VENV_IN_PROJECT=1 $(ENV_PREFIX)pipenv install --dev --deploy 
	$(ENV_PREFIX)pip install -e .[test]

fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)isort async_pipeline/
	$(ENV_PREFIX)black -l 88 async_pipeline/
	$(ENV_PREFIX)black -l 88 tests/

lint: info            ## Run pep8, black, mypy linters.
	$(ENV_PREFIX)flake8 async_pipeline/
	$(ENV_PREFIX)black -l 88 --check async_pipeline/
	$(ENV_PREFIX)black -l 88 --check tests/
	
test:        ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=async_pipeline -l --tb=short --maxfail=1 tests/
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

watch:            ## Run tests on every change.
	ls **/**.py | entr $(ENV_PREFIX)pytest -s -vvv -l --tb=long --maxfail=1 tests/

clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

virtualenv:       ## Create a virtual environment.
	@if [ "$(USING_POETRY)" ]; then poetry install && exit; fi
	@echo "creating virtualenv ..."
	@rm -rf .venv
	@python3 -m venv .venv
	@./.venv/bin/pip install -U pip
	@./.venv/bin/pip install -e .[test]
	@echo
	@echo "!!! Please run 'source .venv/bin/activate' to enable the environment !!!"

release:          ## Create a new tag for release.
	@echo "WARNING: This operation will create s version tag and push to github"
	@read -p "Version? (provide the next x.y.z semver) : " TAG
	@echo "$${TAG}" > async_pipeline/VERSION
	@$(ENV_PREFIX)gitchangelog > HISTORY.md
	@git add async_pipeline/VERSION HISTORY.md
	@git commit -m "release: version $${TAG} 🚀"
	@echo "creating git tag : $${TAG}"
	@git tag $${TAG}
	@git push -u origin HEAD --tags
	@echo "Github Actions will detect the new tag and release the new version."

docs:             ## Build the documentation.
	@echo "building documentation ..."
	@$(ENV_PREFIX)mkdocs build
	URL="site/index.html"; xdg-open $$URL || sensible-browser $$URL || x-www-browser $$URL || gnome-open $$URL

switch-to-poetry: ## Switch to poetry package manager.
	@echo "Switching to poetry ..."
	@if ! poetry --version > /dev/null; then echo 'poetry is required, install from https://python-poetry.org/'; exit 1; fi
	@rm -rf .venv
	@poetry init --no-interaction --name=a_flask_test --author=rochacbruno
	@echo "" >> pyproject.toml
	@echo "[tool.poetry.scripts]" >> pyproject.toml
	@echo "async_pipeline = 'async_pipeline.__main__:main'" >> pyproject.toml
	@cat requirements.txt | while read in; do poetry add --no-interaction "$${in}"; done
	@cat requirements-test.txt | while read in; do poetry add --no-interaction "$${in}" --dev; done
	@poetry install --no-interaction
	@mkdir -p .github/backup
	@mv requirements* .github/backup
	@mv setup.py .github/backup
	@echo "You have switched to https://python-poetry.org/ package manager."
	@echo "Please run 'poetry shell' or 'poetry run async_pipeline'"