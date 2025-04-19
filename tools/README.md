# Discord Webhook Tool

A simple and efficient Python tool to send messages asynchronously to a Discord channel using a webhook URL. Designed for easy integration into asynchronous applications or use as a standalone utility.

**Author:** [Jakkraphop Pengchan](https://github.com/jakkph32)

**Repository:** [Open WebUI Utils](https://github.com/jakkph32/open-webui-utils)

**Version:** 0.0.2

## Description

This tool provides a Python class (`Tools`) that allows you to send messages to a specific Discord channel via its webhook URL. It leverages `aiohttp` for asynchronous HTTP requests, ensuring non-blocking operations suitable for modern async applications. Configuration is handled securely via an environment variable.

## Features

*   **Asynchronous:** Uses `aiohttp` for non-blocking message sending.
*   **Easy Configuration:** Configure the target webhook URL via the `DISCORD_WEBHOOK_URL` environment variable.
*   **Input Validation:** Uses `pydantic` to validate the webhook URL format on initialization.
*   **Message Length Handling:** Automatically truncates messages exceeding Discord's 2000-character limit and logs a warning.
*   **Session Management:** Efficiently manages `aiohttp.ClientSession`. Supports using an internally managed session (via `async with`) or an externally provided session.
*   **Error Handling:** Catches common HTTP and network errors, logs them, and returns `False` on failure.
*   **Clean & Reusable:** Designed as a class for easy integration and reuse.

## Configuration
Before running the tool, you **must** set the `DISCORD_WEBHOOK_URL` environment variable to your target Discord channel's webhook URL.


## Error Handling

* If the `DISCORD_WEBHOOK_URL` is missing or invalid, a `ValueError` is raised during `Tools` initialization.
* If sending the message fails (e.g., network issue, invalid webhook, Discord error), an error message is logged, and `send_message` returns `False`.
* Unexpected errors are caught, logged with a traceback, and `send_message` returns `False`.


## Contributing

Contributing
Contributions are welcome! Please feel free to submit issues or pull requests on the source repository (if applicable).


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
