"""
id: discord_webhook
title: Discord Webhook
description: Sends messages or notifications to a specified Discord channel using a Webhook URL configured via the DISCORD_WEBHOOK_URL environment variable.
author: Jakkraphop Pengchan
author_url: https://github.com/jakkph32
git_url: https://github.com/jakkph32/open-webui-utils
funding_url: https://github.com/jakkph32/open-webui-utils
version: 0.0.2
tags: [discord, webhook, notification, messaging]
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
    A tool to send messages to Discord via a webhook, managing aiohttp sessions
    and handling configuration through environment variables.
    """

    class Valves(BaseModel):
        """Configuration model for validating the webhook URL."""

        WEBHOOK_URL: str = Field(
            default=os.environ.get("DISCORD_WEBHOOK_URL", ""),
            description="The URL of the Discord webhook to send messages to.",
        )

        @validator("WEBHOOK_URL")
        def validate_webhook_url(cls, v):
            if not v:
                raise ValueError(
                    "DISCORD_WEBHOOK_URL environment variable must be set."
                )
            if not v.startswith("https://discord.com/api/webhooks/"):
                logging.warning(
                    "Webhook URL does not look like a standard Discord webhook URL."
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

    async def send_message(self, message_content: str) -> bool:
        """
        Sends a message to the configured Discord webhook URL.

        Args:
            message_content (str): The content of the message to send.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        try:
            # Webhook URL is validated during __init__ via Valves
            await self._ensure_session()

            # Truncate message if it exceeds Discord's limit
            if len(message_content) > 2000:
                logging.warning(
                    "Message content exceeds Discord limit (2000 characters). Truncating."
                )
                message_content = message_content[:2000]

            data = {"content": message_content}
            async with self.session.post(
                self.valves.WEBHOOK_URL, json=data
            ) as response:
                if response.status == 204:
                    logging.info("Message successfully sent to Discord.")
                    return True
                else:
                    # Log detailed error including status and response body
                    error_message = f"Failed to send message. Status: {response.status}, Response: {await response.text()}"
                    logging.error(error_message)
                    return False
        except aiohttp.ClientError as e:
            logging.error(f"AIOHTTP client error occurred: {e}")
            return False
        except Exception as e:
            # Log unexpected errors with stack trace
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


# --- Example Usage (Optional: Keep for demonstration or remove for deployment) ---
# This section demonstrates how to use the Tools class.
# It requires the 'DISCORD_WEBHOOK_URL' environment variable to be set.


async def main():
    """Example function demonstrating tool usage."""
    # Ensure the environment variable is set for the example to run
    if not os.environ.get("DISCORD_WEBHOOK_URL"):
        print("Error: DISCORD_WEBHOOK_URL environment variable not set.")
        print(
            "Please set it to run the example: export DISCORD_WEBHOOK_URL='your_webhook_url_here'"
        )
        return

    # Example 1: Using the tool as a context manager (recommended for simple cases)
    print("--- Example 1: Using async with (manages session internally) ---")
    try:
        async with Tools() as discord_tool:
            success = await discord_tool.send_message("Hello from async with!")
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
            discord_tool_external = Tools(session=external_session)
            success1 = await discord_tool_external.send_message(
                "First message with external session."
            )
            print(f"Message 1 sent successfully: {success1}")

            # Reuse the same tool instance (and the external session)
            success2 = await discord_tool_external.send_message(
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
