# dc.d/Makefile
DC_BIN=docker compose
BACKEND_SERVICE_NAME=backend
MAIN_SERVICE_NAME=${BACKEND_SERVICE_NAME}

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

pull:
	git pull || echo 'some error '

build:
	$(DC_BIN) build

prune-containers:
	docker container prune -f

prune-system:
	docker system prune -f -a

prune: prune-containers

up-all:
	$(DC_BIN) up -d

up-main:
	$(DC_BIN) up -d ${MAIN_SERVICE_NAME}

up: up-all

stop-all:
	$(DC_BIN) stop

stop-main:
	$(DC_BIN) stop ${MAIN_SERVICE_NAME}

stop: stop-main

down:
	$(DC_BIN) down

restart: stop up

recreate: pull build stop up

shell-main:
	$(DC_BIN) exec ${MAIN_SERVICE_NAME} bash

shell: shell-main

runshell-main:
	$(DC_BIN) run --rm ${MAIN_SERVICE_NAME} bash

runshell: runshell-main

ishell-main:
	$(DC_BIN) exec ${MAIN_SERVICE_NAME} bash -c 'poetry install && python manage.py shell'

ishell: ishell-main

irunshell-main:
	$(DC_BIN) run --rm ${MAIN_SERVICE_NAME} sh -c 'poetry install && python manage.py shell'

irunshell: pull build irunshell-main

# shortcuts
l: logs

s: shell

i: ishell

r: recreate

rl: r l

rs: r s

ri: r i

rm: build stop-main up-main logs
