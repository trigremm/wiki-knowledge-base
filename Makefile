# Makefile
# fallback command
UTILS_DIR := asmo.d/utils
PY_UTILS_DIR := ${UTILS_DIR}/py_utils

.PHONY: add_file_path_comment black-format isort-format format f
add_file_path_comment:
	@python ${PY_UTILS_DIR}/add_file_path_comment.py .

black-format:
	black . --line-length 120

isort-format:
	isort . --line-length 120

format: add_file_path_comment black-format isort-format

f: format

%:
	@echo try to run command in other locations
	@$(MAKE) -C ${UTILS_DIR} $@ || echo 'no target found'
