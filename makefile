API_DOCKERFILE_PATH=stack-1/api/dockerfile
API_IMAGE_NAME=webapp-api
DOCKER_HUB_USERNAME=
DOCKER_HUB_PASSWORD=
DOCKER_HUB_IMAGE_TAG=latest
DOCKER_HUB_IMAGE=$(DOCKER_HUB_USERNAME)/$(API_IMAGE_NAME):$(DOCKER_HUB_IMAGE_TAG)
COMPOSE_STACK_1=./stack-1/docker-compose.yml
COMPOSE_STACK_2=./stack-2/docker-compose.yml
COMPOSE_STACK_3=./stack-3/docker-compose.yml

create-network:
	@if [ -z $$(docker network ls -q -f name=test-devops-network) ]; then \
        echo "Creating network: test-devops-network"; \
        docker network create --driver overlay test-devops-network; \
	else \
        echo "Network test-devops-network already exists"; \
	fi


create-stack-1: create-network
	docker stack deploy -c $(COMPOSE_STACK_1) webapp-stack

create-stack-2: create-network
	docker stack deploy -c $(COMPOSE_STACK_2) graylog-stack

create-stack-3: create-network
	docker stack deploy -c $(COMPOSE_STACK_3) nginx-stack

build-and-push: docker-login
	docker build -t $(API_IMAGE_NAME) --platform linux/amd64 -f $(API_DOCKERFILE_PATH) .
	docker tag $(API_IMAGE_NAME) $(DOCKER_HUB_IMAGE)
	docker push $(DOCKER_HUB_IMAGE)

docker-login:
	@echo "Iniciando sesión en Docker Hub..."
	@docker login -u $(DOCKER_HUB_USERNAME) -p $(DOCKER_HUB_PASSWORD) docker.io

init-graylog:
	bash ./stack-2/config/init.sh