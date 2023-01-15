help:
	@echo "    unit-test"
	@echo "        Test for the embedding store without external dependencies."

unit-test:
	python -m pytest -m unit
