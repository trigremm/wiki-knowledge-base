# docker/Makefile
all: ps

ps:
	docker ps

stop-all:
	docker stop $$(docker ps -a -q)

prune-containers:
	docker container prune -f

prune-system:
	docker system prune -f -a

prune: prune-containers
