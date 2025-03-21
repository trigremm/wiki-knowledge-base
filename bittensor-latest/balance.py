import bittensor

wallet = bittensor.wallet(name='dojo_test_98', hotkey="dojo_test_98_hotkey")
subtensor = bittensor.subtensor()

# Check TAO balance
balance = subtensor.get_balance(wallet.coldkeypub.ss58_address)
print(f"Wallet TAO Balance: {balance}")

# Check stake in netuid 98
netuid = 98
stake = subtensor.get_stake_for_hotkey(netuid=netuid, hotkey_ss58=wallet.hotkey.ss58_address)
print(f"Stake in netuid {netuid}: {stake}")
