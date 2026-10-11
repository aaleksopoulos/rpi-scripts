# Wake-on-LAN Telegram bot

Send `/wake` to the bot and the Pi sends a Wake-on-LAN magic packet to your PC. Only the Telegram user set in `USER_ID` can wake the PC; anyone else gets a refusal. The bot uses polling, so you don't need to open any ports on your router.

The bot's replies are in Greek; edit the strings in `rpi_wol.py` to change them.

For installing it (venv, requirements, `.env`), see the [general setup](../README.md#general-setup).

## Commands

| Command | Action |
| --- | --- |
| `/start` | Short greeting |
| `/wake` | Sends the magic packet (authorised user only) |

## Configuration (`.env`)

| Variable | Description |
| --- | --- |
| `API_TOKEN` | Bot token from [@BotFather](https://t.me/BotFather) |
| `USER_ID` | Your numeric Telegram user ID |
| `PC_MAC` | MAC address of the PC to wake, e.g. `AA:BB:CC:DD:EE:FF` |

To find your user ID, start the bot with `USER_ID=0` and send it `/wake`. The bot prints `user_id <number>`; put that number in `.env` and restart the bot.

## Requirements for Wake-on-LAN

- Wake-on-LAN is enabled in the PC's BIOS/UEFI and in its network adapter settings.
- The PC is connected by Ethernet, on the same network as the Pi.
- The packet is broadcast to `255.255.255.255`, port 9.

## Running it

```bash
venv/bin/python rpi_wol.py
```

To keep it running and start it at boot, use a systemd service. Create `/etc/systemd/system/wol-bot.service`, adjusting the user and paths:

```ini
[Unit]
Description=Wake-on-LAN Telegram bot
After=network-online.target
Wants=network-online.target

[Service]
User=pi
WorkingDirectory=/home/pi/telegram_bot
ExecStart=/home/pi/telegram_bot/venv/bin/python rpi_wol.py
Environment=PYTHONUNBUFFERED=1
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now wol-bot
journalctl -u wol-bot -f      # follow the logs
```
