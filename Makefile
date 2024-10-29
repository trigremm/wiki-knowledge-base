# fallback command
BONUS_PATH = ./bonus.d
DC_PATH = ./dc.d

format:
	python -m isort ./ --line-width 120 --quiet
	python -m black ./ --line-length 120 --quiet

f: format

%:
	@echo try to run command in other locations
	$(MAKE) -C ${BONUS_PATH} $@ || $(MAKE) -C ${DC_PATH} $@ || echo 'no target found'