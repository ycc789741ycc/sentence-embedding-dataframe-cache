help:
	@echo "    unit-test"
	@echo "        Test for the embedding store without external dependencies."
	@echo "    integration-test"
	@echo "        Test for the embedding store with external dependencies."
	@echo "    start-jina-embedding"
	@echo "        Serve the embedding model base on the jina service."
	@echo "    stop-jina-embedding"
	@echo "        Stop the embedding model base on the jina service."

start-jina-embedding:
	docker-compose -f embedding_models/jina/docker-compose.yml up -d

stop-jina-embedding:
	docker-compose -f embedding_models/jina/docker-compose.yml down

unit-test:
	python -m pytest -m unit

integration-test:
	python -m pytest -m integration

release:
	PYTHONPATH=. python scripts/release.py

build:
	rm -R -f dist/
	poetry version $(BUILD_VERSION)
	poetry build
	@if [ "$(shell uname -s)" == "Darwin" ]; then gtar -xvf dist/*.tar.gz --wildcards --no-anchored '*/setup.py' --strip=1;\
	else tar -xvf dist/*.tar.gz --wildcards --no-anchored '*/setup.py' --strip=1;\
	fi
	poetry export -f requirements.txt --output requirements.txt

pypi-upload:
	twine upload dist/*

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf .mypy_cache/
	rm -rf dist/
	rm -rf docs/build
	rm -rf docs/.docusaurus
	rm -rf .pytest_cache/
	rm -rf ./**/__pycache__/

doc-gen-rst:
	sphinx-apidoc -o doc/source embestore
