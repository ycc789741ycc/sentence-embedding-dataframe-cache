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
