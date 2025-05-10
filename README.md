# Graduate Studies Announcements Telegram Bot

A simple Python-based bot that periodically scrapes the The University of Jordan Graduate Studies announcements page and sends new announcement links to a Telegram chat. It utilizes a cronjob to run automatically every 2 minutes by default

---

## Features

* Scrapes the “All Announcements” page for new items (by announcement ID).
* Sends detailed announcement links via Telegram Bot API.
* Persists seen IDs in a local JSON file to avoid duplicate notifications.
* Configurable via `.env` for tokens and chat IDs.
* Easily scheduled via `cron` (macOS/Linux).

---

## Prerequisites

* Python 3.8+
* `pip` package manager
* A Telegram account to create a bot and obtain chat IDs.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ju-announcements-bot.git
   cd ju-announcements-bot
   ```

2. **Create and activate a virtual environment (optional but recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

1. **Create a Telegram Bot**

   * Open [@BotFather](https://t.me/BotFather) in Telegram.
   * Send `/newbot` and follow prompts to name your bot.
   * BotFather will reply with an **API Token** (e.g. `123456:ABC-DEF...`).

2. **Obtain your Chat ID**

   * Add your bot to a group or message it directly.
   * Use the Bot API to fetch updates:

     ```bash
     curl "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
     ```
   * In the JSON response, look for `chat` → `id` (this is your Chat ID).

3. **Create a `.env` file** in the project root:

   ```dotenv
   TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
   TELEGRAM_CHAT_ID=987654321
   ```

   * **Never** commit your real `.env` to GitHub.

---

## Usage

Run the scraper script manually:

```bash
python main.py
```

You should see console output indicating whether new announcements were found or notifications sent.

---

## Scheduling with `cron` (every 2 minutes)

1. Open your crontab for editing:

   ```bash
   crontab -e
   ```

2. Add the following line (adjust paths as needed):

   ```cron
   */2 * * * * /usr/bin/env/python3 /path/to/main.py >> /path/to/scrape_and_notify.log 2>&1
   ```

3. Save and exit. Your bot will now check for new announcements every 2 minutes.

---

## License

This project is released under the MIT License. Feel free to use and modify it as you like.
