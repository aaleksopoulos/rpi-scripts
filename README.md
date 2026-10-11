# Raspberry Pi scripts

Small Python scripts I run on a Raspberry Pi at home.

| Folder | What it does |
| --- | --- |
| [`telegram_bot/`](telegram_bot/) | Telegram bot that wakes a PC on the local network (Wake-on-LAN) |
| [`temp_humid/`](temp_humid/) | Reads a DHT22 temperature/humidity sensor, logs to CSV and sends readings to a web server |

Each folder is self-contained, with its own README, `requirements.txt` and `.env.example`.

## General setup

You need Python 3.10 or newer (Raspberry Pi OS Bookworm or later). Give each script its own virtual environment:

```bash
cd telegram_bot            # or any other project folder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # then edit .env with your own values
```

The variables each script needs, and how to run it, are in that folder's README.

## License

[MIT](LICENSE)
