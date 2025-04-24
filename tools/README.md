# Tools for Open WebUI

This directory serves as a collection of tools designed to enhance and extend the capabilities of the Open WebUI platform. Each tool provides specific functionality, enabling seamless integration and efficient operations within the Open WebUI ecosystem.

## Purpose

The `tools` directory is a centralized repository for various utilities and modules that can be used to create, manage, and streamline workflows in Open WebUI. These tools are written in Python and follow modern design principles, emphasizing performance, ease of use, and scalability.

## Available Tools

### 1. [Discord Webhook](tools/discord_webhook.py)
- **Description**: A tool to send notifications or messages to a Discord channel via a webhook.
- **Key Features**:
  - Asynchronous messaging using `aiohttp`.
  - Configured via `DISCORD_WEBHOOK_URL` environment variable.
  - Supports message validation and truncation for Discord's character limit.
- **Use Case**: Ideal for sending alerts, system notifications, or updates directly to Discord.

### 2. [Telegram Symphony](tools/telegram_symphony.py)
- **Description**: A tool to send messages to a Telegram chat using a bot token and chat ID.
- **Key Features**:
  - Asynchronous operations with `aiohttp`.
  - Configured via `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` environment variables.
  - Validates configurations and ensures compatibility with Telegram's API.
- **Use Case**: Suitable for broadcasting messages, updates, or notifications to Telegram users or groups.

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/jakkph32/open-webui-utils.git
   cd open-webui-utils/tools
   ```

2. Set the required environment variables for the tool you wish to use.

3. Import the tool in your Python project and call its methods. Examples are provided in each tool's script.

## Contribution

We welcome contributions to expand the `tools` collection! If you have a utility that could benefit the Open WebUI ecosystem, feel free to submit a pull request.

## Licensing

The tools in this directory are licensed under the MIT License. See the `LICENSE` file for more details.

## Author

Created and maintained by [Jakkraphop Pengchan](https://github.com/jakkph32). For more information or to report issues, visit the [repository](https://github.com/jakkph32/open-webui-utils).
