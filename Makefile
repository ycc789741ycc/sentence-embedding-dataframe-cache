help:
	@echo "    unit-test"
	@echo "        Test for the embedding store without external dependencies."
	@echo "    integration-test"
	@echo "        Test for the embedding store with external dependencies."
	@echo "    serve-jina-embedding"
	@echo "        Serve the embedding model base on the jina service."
	@echo "    stop-jina-embedding"
	@echo "        Stop the embedding model base on the jina service."

serve-jina-embedding:
	docker-compose -f embedding_models/jina/docker-compose.yml up -d

stop-jina-embedding:
	docker-compose -f embedding_models/jina/docker-compose.yml down

unit-test:
	python -m pytest -m unit

integration-test:
	python -m pytest -m integration

release:
	PYTHONPATH=. python scripts/release.py

build-and-push-package:
	$(MAKE) build-package
	$(MAKE) push-package

build-package:
	rm -R -f dist/
	poetry version $(BUILD_VERSION)
	poetry build
	tar -xvf dist/*.tar.gz --wildcards --no-anchored '*/setup.py' --strip=1
	poetry export -f requirements.txt --output requirements.txt

push-package:
	poetry publish
