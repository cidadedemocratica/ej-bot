
.PHONY: clean train-nlu train-core cmdline server

TEST_PATH=./tests

help:
	@echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    train-nlu"
	@echo "        Trains a new nlu model using the projects Rasa NLU config"
	@echo "    train-core"
	@echo "        Trains a new dialogue model using the story training data"
	@echo "    action-server"
	@echo "        Starts the server for custom action."
	@echo "    run-api"
	@echo "       This will load the assistant in your terminal for you to chat."


clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf docs/_build

train: train-nlu train-core action-server

trainer:
	docker build . -f docker/trainer.Dockerfile -t trainer:latest

train-nlu:
	python -m rasa_nlu.train -c nlu_config.yml --data data/intents/ -o models --fixed_model_name nlu --project current --verbose

train-core:
	python -m rasa_core.train -d domain.yml -s data/stories/ -o models/current/dialogue -c policies.yml

run-api:
	python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml --debug --enable_api

action-server:
	python -m rasa_core_sdk.endpoint --actions actions.actions

visualize:
	python -m rasa.core.visualize -s data/stories.md -d domain.yml -o story_graph.html