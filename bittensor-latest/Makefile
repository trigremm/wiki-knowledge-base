venv:
	@echo 'for zsh:'
	@echo 'uv venv --python 3.10 .venv_bt && source .venv_bt/bin/activate && pip install -r requirements.txt'
	@echo 'source .venv_bt/bin/activate'
	@echo ''
	@echo 'for fish:'
	@echo 'uv venv --python 3.10 .venv_bt && source .venv_bt/bin/activate.fish && pip install -r requirements.txt'

install:
	uv pip install bittensor
	uv pip install bittensor-cli

balance:
	btcli wallet balance --wallet.name dojo_test_98 --wallet.hotkey dojo_test_98_hotkey
	btcli wallet balance --wallet.name dojo_test_98 --wallet.hotkey dojo_test_98_hotkey --subtensor.network test
	btcli wallet balance --subtensor.network test --wallet.name dojo_test_98

