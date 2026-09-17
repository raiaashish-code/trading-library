"""
Export document attachments (books) from a Telegram channel into books/.

Usage:
    pip install -r requirements.txt
    export TG_API_ID=...
    export TG_API_HASH=...
    export TG_CHANNEL=...       # username or numeric chat id
    python telegram_export.py

First run is interactive (Telegram will send a login code to your account).
After that, a local session file caches the login for reuse.
"""

import asyncio
import os
import re
from pathlib import Path

from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeFilename

BOOKS_DIR = Path("books")
SESSION_NAME = "telegram_export"

DOCUMENT_EXTENSIONS = {".pdf", ".epub", ".mobi", ".azw3", ".djvu", ".txt", ".md"}


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^\w\s.\-]", "", name).strip()
    return re.sub(r"\s+", "_", name)


def get_filename(message) -> str | None:
    if not message.document:
        return None
    for attr in message.document.attributes:
        if isinstance(attr, DocumentAttributeFilename):
            return attr.file_name
    return None


async def main() -> None:
    api_id = os.environ["TG_API_ID"]
    api_hash = os.environ["TG_API_HASH"]
    channel = os.environ["TG_CHANNEL"]

    BOOKS_DIR.mkdir(exist_ok=True)

    client = TelegramClient(SESSION_NAME, api_id, api_hash)
    await client.start()

    entity = await client.get_entity(channel)

    downloaded = 0
    async for message in client.iter_messages(entity):
        filename = get_filename(message)
        if not filename:
            continue
        ext = Path(filename).suffix.lower()
        if ext not in DOCUMENT_EXTENSIONS:
            continue

        safe_name = sanitize_filename(filename)
        dest = BOOKS_DIR / safe_name
        if dest.exists():
            continue

        print(f"Downloading {filename} -> {dest}")
        await client.download_media(message, file=str(dest))
        downloaded += 1

    print(f"Done. Downloaded {downloaded} new file(s) into {BOOKS_DIR}/")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
