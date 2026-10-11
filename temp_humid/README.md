# DHT22 temperature and humidity logger

Each run reads the sensor (up to 10 attempts) and then:

1. appends the reading to `<room>.csv` as `timestamp, temperature (°C), humidity (%)`;
2. POSTs it as JSON to `http://<WEBSERVER_IP>:<PORT>/api/update`.

If the server is unreachable, the reading is still saved to the CSV. If all 10 sensor reads fail, the error is written to `dht_error_<room>.csv`.

For installing it (venv, requirements, `.env`), see the [general setup](../README.md#general-setup).

## Wiring

| DHT22 pin | Raspberry Pi |
| --- | --- |
| VCC | 3.3V (physical pin 1) |
| DATA | GPIO17 (physical pin 11) |
| GND | GND (physical pin 6) |

A bare DHT22 needs a 10 kΩ pull-up resistor between DATA and VCC. Most breakout modules already include one. To use another pin, change `board.D17` in `dht.py`.

## Configuration (`.env`)

| Variable | Description |
| --- | --- |
| `WEBSERVER_IP` | IP address of the server that receives the readings |
| `PORT` | Port that server listens on |

## Server endpoint

The receiving server is **not** part of this repo. It needs to accept a `POST` to `/api/update` with a JSON body like this and reply with JSON:

```json
{
  "temperature": 22.4,
  "humidity": 48.0,
  "timestamp": "2026-10-11 14:30"
}
```

## Running it

```bash
venv/bin/python dht.py -r living_room
```

`-r` / `--room` sets the room name, which is used in the CSV file names (default: `default_room`).

To take a reading every 5 minutes, add this line with `crontab -e`, adjusting the paths:

```cron
*/5 * * * * cd /home/pi/temp_humid && venv/bin/python dht.py -r living_room 2>> cronerror.log
```

The `cd` makes the CSV and log files go into the script's folder. Without it, cron writes them to your home directory.
