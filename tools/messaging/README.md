# Open WebUI Utilities - Messaging Tools

This repository contains tools to send notifications or messages to Discord and Telegram services. These utilities are designed to work seamlessly with the Open WebUI platform.

## Tools Overview

### 1. Discord Webhook (`discord_webhook.py`)

The `discord_webhook.py` tool enables you to send messages to a specified Discord channel using a webhook URL configured via an environment variable.

#### Key Features:
- **Asynchronous Messaging**: Built on `aiohttp` for high-performance asynchronous operations.
- **Environment Configuration**: Uses `DISCORD_WEBHOOK_URL` for webhook configuration.
- **Validation**: Ensures the webhook URL is valid and conforms to Discord's standards.
- **Error Handling**: Comprehensive logging for failed messages or invalid configurations.
- **Message Truncation**: Automatically truncates messages exceeding Discord's 2000-character limit.

#### Environment Variables:
- `DISCORD_WEBHOOK_URL`: The webhook URL for the target Discord channel.

#### Usage Example:
```python
import asyncio
from tools.discord_webhook import Tools

async def main():
    async with Tools() as discord_tool:
        success = await discord_tool.send_message("Hello Discord!")
        print(f"Message sent successfully: {success}")

if __name__ == "__main__":
    asyncio.run(main())
```

#### Installation and Setup:
1. Set the environment variable `DISCORD_WEBHOOK_URL` with your Discord webhook URL.
   ```bash
   export DISCORD_WEBHOOK_URL="your_discord_webhook_url"
   ```
2. Use the example code above to integrate this tool into your application.

---

### 2. Telegram Symphony (`telegram_symphony.py`)

The `telegram_symphony.py` tool enables you to send notifications or messages to a Telegram chat using a bot token and chat ID.

#### Key Features:
- **Asynchronous Messaging**: Utilizes `aiohttp` for effective asynchronous operations.
- **Environment Configuration**: Uses `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` for setup.
- **Validation**: Ensures valid bot token and chat ID configurations.
- **Error Handling**: Logs detailed errors for failed message deliveries or invalid configurations.
- **Message Truncation**: Automatically truncates messages exceeding Telegram's 4096-character limit.

#### Environment Variables:
- `TELEGRAM_BOT_TOKEN`: The bot token for your Telegram bot.
- `TELEGRAM_CHAT_ID`: The chat ID of the target Telegram chat.

#### Usage Example:
```python
import asyncio
from tools.telegram_symphony import Tools

async def main():
    async with Tools() as telegram_tool:
        success = await telegram_tool.send_telegram_message("Hello Telegram!")
        print(f"Message sent successfully: {success}")

if __name__ == "__main__":
    asyncio.run(main())
```

#### Installation and Setup:
1. Set the environment variables `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
   export TELEGRAM_CHAT_ID="your_telegram_chat_id"
   ```
2. Use the example code above to integrate this tool into your application.

---

## Licensing

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

Created by [Jakkraphop Pengchan](https://github.com/jakkph32). For more information or contributions, visit the [GitHub repository](https://github.com/jakkph32/open-webui-utils).
