"""
id: telegram_symphony
title: Telegram Symphony
description: Effortlessly send Telegram notifications with Telegram Symphony! This high-performance tool, built on aiohttp and validated by Pydantic, delivers messages with unmatched speed and reliability. Featuring robust error handling and intelligent session management.
author: Jakkraphop Pengchan
author_url: https://github.com/jakkph32
git_url: https://github.com/jakkph32/open-webui-utils
funding_url: https://github.com/jakkph32/open-webui-utils
version: 0.0.1
tags: [telegram, bot, notification, messaging, asynchronous, aiohttp, pydantic]
license: MIT
type: tool
"""

import os
import logging
import aiohttp
from typing import Optional
from pydantic import BaseModel, Field, validator

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Tools:
    """
    A tool to send messages to Telegram via a bot, managing aiohttp sessions
    and handling configuration through environment variables.
    """

    class Valves(BaseModel):
        """Configuration model for validating the bot token and chat ID."""

        TELEGRAM_BOT_TOKEN: str = Field(
            default=os.environ.get("TELEGRAM_BOT_TOKEN", ""),
            description="The Telegram bot token.",
        )
        TELEGRAM_CHAT_ID: str = Field(
            default=os.environ.get("TELEGRAM_CHAT_ID", ""),
            description="The Telegram chat ID to send messages to.",
        )

        @validator("TELEGRAM_BOT_TOKEN")
        def validate_bot_token(cls, v):
            if not v:
                raise ValueError("TELEGRAM_BOT_TOKEN environment variable must be set.")
            return v

        @validator("TELEGRAM_CHAT_ID")
        def validate_chat_id(cls, v):
            if not v:
                raise ValueError("TELEGRAM_CHAT_ID environment variable must be set.")
            try:
                int(v)
            except ValueError:
                raise ValueError(
                    "TELEGRAM_CHAT_ID must be a valid integer representing the chat ID."
                )
            return v

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        """
        Initializes the Tools class, optionally using an external aiohttp session.

        Args:
            session (Optional[aiohttp.ClientSession]): An existing aiohttp client session.
                If provided, the tool uses this session and won't close it.
                If None, a new session is created internally and managed by this instance.
        """
        self.valves = self.Valves()  # Validate and load config on init
        if session:
            self.session = session
            self._session_externally_managed = True
        else:
            self.session = None  # Session will be created lazily
            self._session_externally_managed = False

    async def _ensure_session(self):
        """Ensures an active aiohttp session exists, creating one if necessary."""
        if self.session is None or self.session.closed:
            if self._session_externally_managed:
                # Cannot recreate an externally managed session if it's closed.
                raise RuntimeError(
                    "External aiohttp session is closed or was not provided."
                )
            else:
                self.session = aiohttp.ClientSession()
                self._session_externally_managed = False
                logging.debug("Created new internal aiohttp session.")

    async def send_telegram_message(self, message_content: str) -> bool:
        """
        Sends a message to the configured Telegram chat.

        Args:
            message_content (str): The content of the message to send.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        try:
            await self._ensure_session()

            # Telegram message limit
            if len(message_content) > 4096:  # Telegram's limit is 4096
                logging.warning(
                    "Message content exceeds Telegram limit (4096 characters). Truncating."
                )
                message_content = message_content[:4096]

            url = (f"https://api.telegram.org/bot{self.valves.TELEGRAM_BOT_TOKEN}/sendMessage")
            data = {
                "chat_id": self.valves.TELEGRAM_CHAT_ID,
                "text": message_content,
            }

            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    response_json = await response.json()
                    if response_json.get("ok"):
                        logging.info("Message successfully sent to Telegram.")
                        return True
                    else:
                        error_message = f"Failed to send message. Telegram API returned error: {response_json.get('description', 'Unknown error')}"
                        logging.error(error_message)
                        return False
                else:
                    error_message = f"Failed to send message. Status: {response.status}, Response: {await response.text()}"
                    logging.error(error_message)
                    return False
        except aiohttp.ClientError as e:
            logging.error(f"AIOHTTP client error occurred: {e}")
            return False
        except Exception as e:
            logging.exception(
                f"An unexpected error occurred while sending the message: {e}"
            )
            return False

    async def close(self):
        """
        Closes the internally managed aiohttp session, if applicable.
        Does nothing if the session was provided externally.
        """
        if (
            not self._session_externally_managed
            and self.session
            and not self.session.closed
        ):
            await self.session.close()
            logging.debug("Closed internal aiohttp session.")

    async def __aenter__(self):
        """Enters the asynchronous context manager, ensuring a session exists."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exits the asynchronous context manager, closing the internal session if necessary."""
        await self.close()


# --- Example Usage (Optional) ---
# This section demonstrates how to use the Tools class.
# It requires the 'TELEGRAM_BOT_TOKEN' and 'TELEGRAM_CHAT_ID' environment variables to be set.


async def main():
    """Example function demonstrating tool usage."""
    # Check for required environment variables
    if not os.environ.get("TELEGRAM_BOT_TOKEN") or not os.environ.get(
        "TELEGRAM_CHAT_ID"
    ):
        print(
            "Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables must be set."
        )
        print(
            "Please set them to run the example: export TELEGRAM_BOT_TOKEN='your_bot_token' && export TELEGRAM_CHAT_ID='your_chat_id'"
        )
        return

    # Example 1: Using the tool as a context manager
    print("--- Example 1: Using async with (manages session internally) ---")
    try:
        async with Tools() as telegram_tool:
            success = await telegram_tool.send_telegram_message("Hello from async with!")
            print(f"Message sent successfully: {success}")
            # Session is automatically created and closed here.
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("\n--- Example 2: Managing session externally ---")
    # Create a single session to potentially reuse across multiple requests or tools
    async with aiohttp.ClientSession() as external_session:
        try:
            # Pass the existing session to the tool
            telegram_tool_external = Tools(session=external_session)
            success1 = await telegram_tool_external.send_telegram_message(
                "First message with external session."
            )
            print(f"Message 1 sent successfully: {success1}")

            # Reuse the same tool instance (and the external session)
            success2 = await telegram_tool_external.send_telegram_message(
                "Second message with the same external session."
            )
            print(f"Message 2 sent successfully: {success2}")

            # The tool instance will *not* close the external session when done.
            # Closing is handled by the 'async with aiohttp.ClientSession()' block.

        except ValueError as e:
            print(f"Configuration Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    print("External session closed by its context manager.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
