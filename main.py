import os
from dotenv import load_dotenv
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

load_dotenv()

# Configuration: set these in your environment or replace with your values
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # e.g., '123456:ABC-DEF...'
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')      # e.g., '987654321'
# File to store seen IDs
SEEN_FILE = 'seen_ids.json'


# URLs
events_list_url = (
    'https://graduatestudies.ju.edu.jo/ar/arabic/Lists/AcademicNews/School_AllAnn.aspx'
)
detail_url_template = (
    'https://graduatestudies.ju.edu.jo/ar/arabic/Lists/AcademicNews/School_DispAnn.aspx?id={}'
)


def load_seen_ids(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return set(json.load(f))
    return set()


def save_seen_ids(filepath, ids):
    with open(filepath, 'w') as f:
        json.dump(sorted(ids), f)


def fetch_current_ids():
    resp = requests.get(events_list_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    ids = set()
    # Find all anchors pointing to the detail page
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'School_DispAnn.aspx?id=' in href:
            # Extract the ID parameter
            try:
                part = href.split('id=')[1]
                ann_id = int(part.split('&')[0])
                ids.add(ann_id)
            except (IndexError, ValueError):
                continue
    return ids


def send_telegram_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        raise RuntimeError('Telegram bot token or chat ID not set')
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }
    resp = requests.post(url, data=payload)
    resp.raise_for_status()
    return resp.json()


def main():
    seen = load_seen_ids(SEEN_FILE)
    current = fetch_current_ids()

    new_ids = current - seen
    if not new_ids:
        print(f'No new announcements until {datetime.now()}')
        return

    for ann_id in sorted(new_ids):
        link = detail_url_template.format(ann_id)
        message = f'New announcement: <a href="{link}">{link}</a>'
        try:
            send_telegram_message(message)
            print(f'Sent notification for ID {ann_id}')
        except Exception as e:
            print(f'Failed to send notification for ID {ann_id}: {e}')

    # Update seen IDs
    save_seen_ids(SEEN_FILE, seen.union(new_ids))


if __name__ == '__main__':
    main()
