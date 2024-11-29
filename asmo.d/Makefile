UTILS_DIR := utils

DC_BIN := docker compose
MAIN_SERVICE_NAME := python_project_template

.PHONY: all gitinfo ps logs 
.PHONY: docker-stop-all prune-containers prune-system prune prune-containers
.PHONY: pull build up stop down restart recreate 
.PHONY: install_uv install_dev shell runshell ishell
.PHONY: format
.PHONY: l s i r rl rs ri f


export GIT_COMMIT_ID=$(shell git rev-parse HEAD)
export GIT_COMMIT_DATE=$(shell git log -1 --format=%cd --date=iso)
export GIT_COMMIT_MESSAGE=$(shell git log -1 --pretty=%B)

all: ps

gitinfo:
	@echo "Git Commit ID: $(GIT_COMMIT_ID)"
	@echo "Git Commit Date: $(GIT_COMMIT_DATE)"
	@echo "Git Commit Message: $(GIT_COMMIT_MESSAGE)"

ps: gitinfo
	$(DC_BIN) ps

logs:
	while true; do $(DC_BIN) logs -f --tail=100 ; sleep 10; done

docker-stop-all:
	@echo 'docker stop $$(docker ps -a -q)'
	@echo docker ps -a

prune-containers:
	docker container prune -f

prune-system:
	docker system prune -f -a

prune: prune-containers

pull:
	git pull || echo 'some error '

build:
	$(DC_BIN) build

up:
	$(DC_BIN) up -d --remove-orphans

stop:
	$(DC_BIN) stop

down:
	$(DC_BIN) down

restart: stop up

recreate: build stop up

install_uv:
	$(DC_BIN) exec --user root ${MAIN_SERVICE_NAME} sh -c "pip install uv==0.5.4"

install_dev: # install_uv
	$(DC_BIN) exec --user root ${MAIN_SERVICE_NAME} sh -c "uv pip install --no-cache-dir --system .[dev]"

shell: # install_dev
	$(DC_BIN) exec --user root ${MAIN_SERVICE_NAME} bash

runshell:
	# $(DC_BIN) run --rm --user root ${MAIN_SERVICE_NAME} sh
	$(DC_BIN) run --rm --user root --entrypoint=sh ${MAIN_SERVICE_NAME}

ishell: install_dev
	$(DC_BIN) exec --user root ${MAIN_SERVICE_NAME} sh -c "ipython"

format:
	ruff check . || exit 0
	ruff format .

# shortcuts
l: logs

s: shell

i: ishell

r: recreate

rl: r l

rs: r s

ri: r i

f: format

# fallback commands
%:
	@echo try to run command in other locations
	$(MAKE) -C $(UTILS_DIR) $@ || echo 'no target found'
