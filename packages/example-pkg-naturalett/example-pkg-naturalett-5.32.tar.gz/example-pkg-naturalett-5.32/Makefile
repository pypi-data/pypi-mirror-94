VER=$(shell git rev-parse --short HEAD)

tag:
	echo GIT_COMMIT=$(VER)
build:
	docker build -t naturalett/playground:latest -t naturalett/playground:$(VER) .

login:
	docker login --username=$(DOCKER_USERNAME) --password=$(DOCKER_PASSWORD)
push:
	docker push naturalett/playground:latest docker push naturalett/playground:$(VER)
