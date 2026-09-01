import network
import urequests
import time
from machine import Pin
import dht

# ---------- WIFI ----------
SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

# ---------- TELEGRAM ----------
BOT_TOKEN = "8966706947:AAFPWXNWpnEHPp7zni8qgcrAkxNPkhfP75M"
CHAT_ID = "-5289765450"

URL_SEND = "https://api.telegram.org/bot{}/sendMessage".format(BOT_TOKEN)
URL_UPDATES = "https://api.telegram.org/bot{}/getUpdates".format(BOT_TOKEN)

# ---------- DHT11 ----------
sensor = dht.DHT11(Pin(33))

# ---------- RELAY ----------
relay = Pin(2, Pin.OUT)
relay.value(1)

last_id = 0

# ---------- WIFI CONNECT ----------
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wifi.isconnected():
    time.sleep(1)

print("WiFi connected")


# ---------- SEND MESSAGE ----------
def send_message(message):
    response = None

    try:
        response = urequests.post(URL_SEND, json={
            "chat_id": CHAT_ID,
            "text": message
        })

        print("Sent:", message)

    except Exception as e:
        print("Send error:", e)

    finally:
        if response is not None:
            response.close()


# ---------- MAIN LOOP ----------
while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        response = urequests.get(
            URL_UPDATES + "?offset={}".format(last_id + 1)
        )

        updates = response.json()["result"]
        response.close()

        for update in updates:
            last_id = update["update_id"]

            message = update.get("message")

            if message is None:
                continue

            chat_id = str(message["chat"]["id"])
            text = message.get("text", "").lower()

            if chat_id == CHAT_ID:

                if text == "/status":
                    if relay.value() == 0:
                        relay_status = "ON"
                    else:
                        relay_status = "OFF"

                    reply = (
                        "Temperature: {} C\n"
                        "Humidity: {} %\n"
                        "Relay: {}"
                    ).format(temp, hum, relay_status)

                    send_message(reply)

                elif text == "/on":
                    relay.value(0)
                    send_message("Relay ON")

                elif text == "/off":
                    relay.value(1)
                    send_message("Relay OFF")

    except Exception as e:
        print("Error:", e)

    time.sleep(2)
