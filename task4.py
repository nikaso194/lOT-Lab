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

# ---------- HARDWARE ----------
sensor = dht.DHT11(Pin(33))
relay = Pin(2, Pin.OUT)

# Relay active-LOW:
# relay.value(0) = ON
# relay.value(1) = OFF
relay.value(1)

# ---------- SETTINGS ----------
THRESHOLD = 28
last_id = 0
auto_off_sent = False

# ---------- WIFI CONNECT ----------
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wifi.isconnected():
    time.sleep(1)

print("WiFi connected")


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


def get_relay_status():
    if relay.value() == 0:
        return "ON"
    else:
        return "OFF"


while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        print(
            "Temperature: {} C | Humidity: {} % | Relay: {}"
            .format(temp, hum, get_relay_status())
        )

        # ---------- READ TELEGRAM COMMANDS ----------
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
            text = message.get("text", "").strip().lower()

            if chat_id == CHAT_ID:

                if text == "/status":
                    reply = (
                        "Temperature: {} C\n"
                        "Humidity: {} %\n"
                        "Relay: {}"
                    ).format(
                        temp,
                        hum,
                        get_relay_status()
                    )

                    send_message(reply)

                elif text == "/on":
                    relay.value(0)
                    auto_off_sent = False
                    send_message("Relay ON")

                elif text == "/off":
                    relay.value(1)
                    send_message("Relay OFF")

        # ---------- TEMPERATURE CONDITIONS ----------
        # T >= 27 C and relay is OFF:
        # Send alert every 5 seconds until /on is received.
        if temp >= THRESHOLD and relay.value() == 1:
            send_message(
                "ALERT!\n"
                "Temperature: {} C\n"
                "Temperature is at or above {} C.\n"
                "Relay is OFF.\n"
                "Send /on to turn relay ON."
                .format(temp, THRESHOLD)
            )

        # T < 27 C:
        # Turn relay OFF automatically and send one AUTO-OFF notice.
        elif temp < THRESHOLD:
            if relay.value() == 0:
                relay.value(1)

                if not auto_off_sent:
                    send_message(
                        "AUTO-OFF\n"
                        "Temperature: {} C\n"
                        "Temperature is below {} C.\n"
                        "Relay turned OFF automatically."
                        .format(temp, THRESHOLD)
                    )

                    auto_off_sent = True

            else:
                auto_off_sent = False

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
