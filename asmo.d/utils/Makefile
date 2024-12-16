# bonus.d/Makefile
CURRENT_DIR := "asmo.d/utils"
BASH_UTILD_DIR := "${CURRENT_DIR}/bash_utils"
PY_UTILD_DIR := "${CURRENT_DIR}/py_utils"

build_tree:
	@echo bash ${BASH_UTILD_DIR}/build_tree.sh ./

prompt:
	@echo bash ${BASH_UTILD_DIR}/generate_prompt.sh -p ./ -o asmo.d/prompt_backend.txt

add_file_path_comment:
	@echo python ${PY_UTILD_DIR}/add_file_path_comment.py ./

generate_howto_deploy:
	@echo python ${PY_UTILD_DIR}/generate_howto_deploy.py -w www.url.to.site -r https://github.com/path/to/repo

generate_password:
	@echo python ${PY_UTILD_DIR}/generate_password.py
