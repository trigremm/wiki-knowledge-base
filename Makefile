# fallback command
ASMO_PATH := asmo.d

%:
	@echo try to run command in other locations
	@$(MAKE) -C ${ASMO_PATH} $@ || echo 'no target found'
