# fallback command
ASMO_PATH := asmo.d/utils

black-format:
	black . --line-length 120

isort-format:
	isort . --line-length 120

format: black-format isort-format

f: format

%:
	@echo try to run command in other locations
	@$(MAKE) -C ${ASMO_PATH} $@ || echo 'no target found'
