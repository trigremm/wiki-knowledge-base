# Makefile
# fallback command
UTILS_DIR := asmo.d/utils
PY_UTILS_DIR := ${UTILS_DIR}/py_utils

.PHONY: add_file_path_comment black-format isort-format format f

prettier:
	@prettier --write .

ruff_check:
	@ruff check --fix . || echo 'ruff check failed'

ruff_format:
	@ruff format .

add_file_path_comment:
	@python ${PY_UTILS_DIR}/add_file_path_comment.py .

black-format:
	@black . --line-length 120

isort-format:
	@isort . --line-length 120

format: add_file_path_comment prettier ruff_check ruff_format

f: format

prompt:
	@bash asmo.d/utils/bash_utils/generate_prompt.sh -p ./

%:
	@echo try to run command in other locations
	@$(MAKE) -C ${UTILS_DIR} $@ || echo 'no target found'
