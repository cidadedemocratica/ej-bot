.PHONY: all clean actions

clean:
	rm -rf graph.html results/ models/* *.db*

install:
	pip install --upgrade pip && \
	pip install -r ../requirements.txt && \
	pip install -r ../x-requirements.txt

# NLU
train-nlu:
	rasa train nlu -vv

# CORE
train:
	rasa train -vv

# TESTS
test:
	rasa test --out results/

test-actions:
	python -m pytest

test-nlu:
	rasa test nlu --nlu data/nlu.yml --cross-validation

test-core:
	rasa test core --fail-on-prediction-errors --out results/results-core-test

# VALIDACAO
validate:
	rasa data validate -vv

# MENSAGEIROS
shell:
	rasa shell -m models/ -vv --endpoints endpoints.yml --port 5006

api:
	rasa run -m models/ -vv --endpoints endpoints.yml --enable-api --port 5006

# ACTIONS
actions:
	rasa run actions --actions actions -vv