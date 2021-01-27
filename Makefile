current_dir := $(shell pwd)
user := $(shell whoami)

clean:
	docker-compose down
	cd bot/ && make clean

stop:
	docker-compose stop

############################## BOILERPLATE ##############################
first-run:
	make build
	make train
	make run-shell

build:
	make build-requirements
	make build-coach
	make build-bot

build-requirements:
	docker build . --no-cache -f docker/requirements.Dockerfile -t botrequirements

build-bot:
	docker-compose build --no-cache bot

build-coach:
	docker-compose build --no-cache coach


run-shell:
	docker-compose run --rm --service-ports bot make shell

run-api:
	docker-compose run --rm --service-ports bot make api

run-actions:
	docker-compose run --rm --service-ports bot make actions

train:
	mkdir -p bot/models
	docker-compose up --build coach

############################## TESTS ##############################
test:
	docker-compose run --rm bot make test

run-test-nlu:
	docker-compose run --rm bot make test-nlu

run-test-core:
	docker-compose run --rm bot make test-core

validate:
	docker-compose run --rm bot rasa data validate --domain domain.yml --data data/ -vv

visualize:
	docker-compose run --rm  -v $(current_dir)/bot:/coach coach rasa visualize --domain domain.yml --stories data/stories.md --config config.yml --nlu data/nlu.md --out ./graph.html -vv
	$(info )
	$(info Caso o FIREFOX não seja iniciado automáticamente, abra o seguinte arquivo com seu navegador:)
	$(info bot/graph.html)
	firefox bot/graph.html