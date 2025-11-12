# Telegram notification
-include .env.tg

send-tg-notification:
	@if [ -z "$(TELEGRAM_BOT_TOKEN)" ] || [ -z "$(TELEGRAM_CHAT_ID)" ]; then \
		echo "Skipping Telegram notification: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set."; \
	else \
		echo "Sending Telegram notification..."; \
		curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
			-d "chat_id=${TELEGRAM_CHAT_ID}" \
			-d "text=✅🔧 Here could be your message! 🔧✅" \
			-d "parse_mode=Markdown" \
			-d "disable_notification=true"; \
	fi
