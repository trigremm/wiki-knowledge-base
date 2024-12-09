UTILS_DIR := utils

# fallback commands
%:
	@echo try to run command in other locations
	$(MAKE) -C $(UTILS_DIR) $@ || echo 'no target found'
