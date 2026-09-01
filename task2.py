import network
import urequests
import time

# -------- SETTINGS --------
SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

BOT_TOKEN = "8966706947:AAFPWXNWpnEHPp7zni8qgcrAkxNPkhfP75M"
CHAT_ID = "-5289765450"

# -------- WIFI --------
wifi = network.WLAN(network.STA_IF)

# Reset the Wi-Fi interface first.
# This helps prevent: OSError: Wifi Internal State Error
wifi.active(False)
time.sleep(1)
wifi.active(True)

print("Connecting to WiFi...")

wifi.connect(SSID, PASSWORD)

# Do not wait forever if Wi-Fi cannot connect.
timeout = 20
start_time = time.time()

while not wifi.isconnected():
    if time.time() - start_time > timeout:
        raise RuntimeError("WiFi connection timeout. Check SSID/password or 2.4 GHz Wi-Fi.")

    print(".", end="")
    time.sleep(1)

print("\nWiFi connected")
print("ESP32 IP address:", wifi.ifconfig()[0])

# -------- TELEGRAM --------
URL = "https://api.telegram.org/bot{}/sendMessage".format(BOT_TOKEN)

data = {
    "chat_id": CHAT_ID,
    "text": "Hello World"
}

response = None

try:
    print("Sending Telegram message...")

    response = urequests.post(URL, json=data)

    result = response.json()
    print("Telegram response:", result)

    if result.get("ok"):
        print("Success: Hello World was sent to Telegram.")
    else:
        print("Telegram rejected the request.")
        print(result)

except Exception as e:
    print("Telegram error:", e)

finally:
    if response is not None:
        response.close()
