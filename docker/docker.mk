# docker commands (danger zone)
docker-stop-all:
	@if [ "$(CONFIRM)" != "1" ]; then echo "Add CONFIRM=1 to proceed"; exit 1; fi
	docker stop $$(docker ps -q)

docker-system-prune:
	@if [ "$(CONFIRM)" != "1" ]; then echo "Add CONFIRM=1 to proceed"; exit 1; fi
	docker system prune -f -a || true

docker-container-prune:
	@if [ "$(CONFIRM)" != "1" ]; then echo "Add CONFIRM=1 to proceed"; exit 1; fi
	docker container prune -f || true

docker-image-prune:
	docker image prune -f || true

docker-builder-prune:
	docker builder prune --filter "until=36h" -f || true
