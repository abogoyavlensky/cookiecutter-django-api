COMPOSE = docker-compose -f docker-compose.yml
GOALS = $(filter-out $@,$(MAKECMDGOALS))
BASE_APP = app
VERSION ?= $(shell git describe --always --tags | sed -e 's/-/\+/' | sed -e 's/-/\./' | sed -e 's/+/\-/')

YELLOW := "\e[1;33m"
NC := "\e[0m"
INFO := @sh -c '\
    printf $(YELLOW); \
    echo "=> $$1"; \
    printf $(NC)' VALUE

.SILENT: # Ignore output of make `echo` command

.PHONY: help # [Info] Generate list of targets with descriptions
help:
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/\1 > \2/' | column -tx -s ">"

.PHONY: version  # [Info] Display current project version based on git tag
version:
	@echo "$(VERSION)"


# LOCAL TARGETS

# Lint
PYFORMAT_EXCLUDE = --exclude  migrations --exclude __pycache__
YAPF_EXCLUDE = --exclude "*migrations/*.py" --exclude "*__pycache__*"
PEP8_CLEANED ?= src/apps

.PHONY: format # [Local] Run code auto-formatting of project py-files
format:
	@$(INFO) "Running autoformatter..."
	@isort -rc $(PEP8_CLEANED)
	@pyformat $(PYFORMAT_EXCLUDE) -j 4 -a -i -r $(PEP8_CLEANED)
	@yapf $(YAPF_EXCLUDE) -i -p -r $(PEP8_CLEANED)

.PHONY: mypy # [Local] Run mypy for project py-files
mypy:
	@$(INFO) "Running mypy..."
	@mypy $(PEP8_CLEANED)

.PHONY: xenon # [Local] Checking code complexity of project py-files
xenon:
	@$(INFO) "Checking code complexity..."
	@xenon --max-absolute A --max-modules A --max-average A --exclude "*migrations*" src/apps

.PHONY: lint # [Local] Run autoformatting and full linting of py-files
lint: format mypy xenon
	@$(INFO) "Running flake8..."
	@flake8 --statistics --config=setup.cfg $(PEP8_CLEANED)
	@$(INFO) "Running pylint..."
	@pylint -j 4 $(PEP8_CLEANED)

.PHONY: check # [Local] Check py-files for pep8 compatiblity. May be used for CI
check: lint
	@$(INFO) "Checking diff..."
	@git diff $(PEP8_CLEANED)
	@[ `git ls-files -m $(PEP8_CLEANED) | wc -l` = "0" ] || false

.PHONY: clean # [Local] Clean temp files from projects: .pyc. .pyo, __pycache__
clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf .pytest_cache .mypy_cache


# COMPOSE ALIAS TARGETS

.PHONY: build # [Docker] Build images for project
build:
	@$(COMPOSE) build $(GOALS)

.PHONY: ps # [Docker] Check status of containers
ps:
	@$(COMPOSE) ps

.PHONY: up # [Docker] Run all apps using local docker-compose
up:
	@$(COMPOSE) up $(GOALS)

.PHONY: detach # [Docker] Run all apps using local docker-compose in background
detach:
	@$(COMPOSE) up -d $(GOALS)

.PHONY: logs # [Docker] Follow logs from containers
logs:
	@$(COMPOSE) logs -f --tail=120 $(GOALS)

.PHONY: stop # [Docker] Stop all containers
stop:
	@$(COMPOSE) stop $(GOALS)

.PHONY: down # [Docker] Stop and destroy all containers
down:
	@$(COMPOSE) down $(GOALS)

.PHONY: rm # [Docker] Remove container for services
rm:
	@$(COMPOSE) rm -s -f $(GOALS)

.PHONY: run # [Docker] Run any shell command inside app container. Example `make run ls`
run:
	@$(COMPOSE) run --rm $(BASE_APP) $(GOALS)
%:
	@:

.PHONY: manage # [Docker] Run any django manage command
manage:
	@$(COMPOSE) run --rm $(BASE_APP) python src/manage.py $(GOALS)
%:
	@:

.PHONY: graph # [Docker] Update db_graph.png file at the root of project
graph:
	@$(COMPOSE) run --rm $(BASE_APP) python src/manage.py graph_models -o db_graph.png

.PHONY: restart # [Docker] Restart any service in compose, for example: `make restart app`
restart:
	@$(COMPOSE) restart $(GOALS)
%:
	@:

.PHONY: rebuild # [Docker] Rebuild image and restart any service in compose, for example: `make rebuild app`
rebuild:
	@$(COMPOSE) up -d --no-deps --build $(GOALS)
%:
	@:

.PHONY: fmt # [Docker] Run code linting and formating for app. Example: `make fmt`
fmt:
	@$(COMPOSE) run $(BASE_APP) $(MAKE) lint

.PHONY: test # [Docker] Run test with forcing creting db. Example: `make test`
test:
	@$(COMPOSE) run $(BASE_APP) pytest --create-db $(GOALS)

.PHONY: watch # [Docker] Run test in watch mode. Example: `make watch`
watch:
	@$(COMPOSE) run $(BASE_APP) ptw $(GOALS)


# RELEASE TARGETS

.PHONY: release  # [Relase] Release the app
release:
	@$(if $(GOALS),$(echo "Release $(GOALS) is starting..."),$(error Relase version is not set))
	@git checkout master && git pull origin master
	@echo "Adding tag..."
	@git tag -a $(GOALS) -m 'Release $(GOALS)'
	@git push origin $(GOALS)

.PHONY: push  # [Relase] Push docker test image for testing with CI
push: version
	@docker login -u $(DOCKER_USER) -p $(DOCKER_PASS) registry.gitlab.com \
	&& docker build --build-arg DOCKER_ENTRYPOINT=$(DOCKER_ENTRYPOINT) \
		              --pull \
									-f docker/Dockerfile \
									-t $(DOCKER_TEST_IMAGE):$(VERSION) . \
	&& docker tag $(DOCKER_TEST_IMAGE):$(VERSION) $(DOCKER_TEST_IMAGE):latest \
	&& docker push $(DOCKER_TEST_IMAGE):$(VERSION) \
	&& docker push $(DOCKER_TEST_IMAGE):latest
%:
        @:
