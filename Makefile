# Makefile
.PHONY: prompt
.PHONY: clean
.PHONY: add_file_path_comment prettier autoflake-format isort-format black-format ruff-check ruff-format format f

prompt:
	python asmo.d/utils/py_utils/collect_files_content.py -p backend -o prompt_backend.txt

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

add_file_path_comment:
	python asmo.d/utils/py_utils/add_file_path_comment.py -d .

prettier:
	@prettier --write .

autoflake-format:
	autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive .

isort-format:
	isort --force-single-line-imports .

black-format:
	black --line-length 120 .

ruff_check:
	@ruff check --fix . || echo 'ruff check failed'

ruff_format:
	@ruff format .

nginx_format:
	# pip install nginxfmt
	nginxfmt -i 4 -r .conf.d/* || true

format: clean add_file_path_comment prettier autoflake-format isort-format black-format # ruff_check ruff_format

f: format
