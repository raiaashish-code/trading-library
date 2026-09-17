# Trading Library

A centralized library of trading/investing books and reference material, curated from a Telegram channel.

## Structure

```
books/               # ingested books (one subfolder per book/source)
telegram_export.py   # pulls documents from the Telegram channel into books/
requirements.txt      # dependencies for the export script
```

## Ingesting books from Telegram

`telegram_export.py` uses [Telethon](https://docs.telethon.dev/) to download document attachments (PDF, EPUB, etc.) posted in a Telegram channel into `books/`.

1. Get an API ID and hash from https://my.telegram.org (API development tools).
2. Set environment variables (do **not** commit these):
   - `TG_API_ID`
   - `TG_API_HASH`
   - `TG_CHANNEL` — channel username (e.g. `mychannel`) or numeric chat ID
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run:
   ```
   python telegram_export.py
   ```

The first run will prompt for a login code sent to your Telegram account (interactive), then cache a session file (`telegram_export.session`) locally for subsequent runs. The session file is gitignored — never commit it, it grants full account access.

## Publishing

This repo can be served directly:
- **GitHub Pages** — enable Pages (Settings → Pages → Deploy from branch) to browse `books/` at `https://<owner>.github.io/trading-library/`.
- **Raw file access** — any file is fetchable via `raw.githubusercontent.com/<owner>/trading-library/main/<path>`, so an external website/app can link or fetch directly.
- **GitHub API** — list/search files programmatically to drive a custom front end.

## License / attribution

Only add material you have the right to redistribute. If a book is sourced from a public/open-licensed repository (e.g. CC BY), keep its original license file and attribution alongside it in its `books/<name>/` folder.
