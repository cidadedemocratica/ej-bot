
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

# NLU
train-nlu:
	rasa train nlu -vv

# CORE
train-core:
	rasa train -vv

trainer:
	docker build . -f docker/trainer.Dockerfile -t trainer:latest


run-api:
	rasa run -m models/ -vv --endpoints endpoints.yml --enable-api --port 5055

action-server:
	rasa run actions --actions actions -vv

visualize:
	python -m rasa.core.visualize -s data/stories.md -d domain.yml -o story_graph.html