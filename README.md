# lOT-Lab
Overall Project
This project uses an ESP32, a DHT11 temperature/humidity sensor, a relay module, Wi-Fi, and a Telegram bot.
The DHT11 measures the surrounding temperature and humidity. The ESP32 processes the sensor readings and controls the relay. Telegram provides a remote interface where the user can check the sensor status and turn the relay on or off.
The project was completed progressively from Task 1 to Task 4. Each task added a new function to the system, beginning with basic sensor reading and ending with automatic temperature-based relay control.

Task 1 — Sensor Read and Print
Function
Task 1 tests the DHT11 sensor and confirms that the ESP32 can read temperature and humidity correctly.
The DHT11 is connected to GPIO33. The ESP32 reads the sensor every five seconds and prints the results in the Thonny Shell.
Example output:
text
Temperature: 28 C
Humidity: 70 %
What was implemented
Initialized the DHT11 sensor using GPIO33.
Used sensor.measure() to obtain a new reading.
Read the temperature using sensor.temperature().
Read the humidity using sensor.humidity().
Printed the values to the serial monitor.
Added a five-second delay between readings.
Purpose
This task verifies that the sensor is correctly wired and functioning before adding Telegram and relay features.
Screenshot evidence
Insert your screenshot here:
text
[Insert Task 1 Thonny sensor-output screenshot here]

Task 2 — Telegram Message Sending
Function
Task 2 connects the ESP32 to Wi-Fi and sends a test message to a Telegram group using the Telegram Bot API.
The ESP32 uses the Wi-Fi network to access Telegram’s online API. A test message such as Hello World is sent to the configured Telegram chat.
What was implemented
Connected the ESP32 to the configured Wi-Fi network.
Created the Telegram bot URL using the bot token.
Used the Telegram sendMessage method.
Sent the message to the configured chat ID.
Used urequests.post() to send the message.
Printed the result in the Thonny Shell.
Example Telegram message:
text
Hello World
Purpose
This task verifies that the ESP32 has internet access and can communicate with Telegram before receiving commands.
Screenshot evidence
Insert your screenshot here:
text
[Insert Task 2 Telegram “Hello World” screenshot here]

Task 3 — Telegram Commands
Function
Task 3 adds remote control through Telegram. The user can send commands to the bot, and the ESP32 responds accordingly.
The system supports three commands:
/status
/on
/off
/status
The ESP32 reads the current DHT11 values and sends a reply containing:
Current temperature.
Current humidity.
Current relay state.
Example:
text
Temperature: 28 C
Humidity: 70 %
Relay: OFF
/on
When the user sends /on:
The ESP32 activates the relay.
The bot replies with Relay ON.
/off
When the user sends /off:
The ESP32 deactivates the relay.
The bot replies with Relay OFF.
What was implemented
Used Telegram getUpdates to receive messages.
Used an update ID to avoid processing the same message repeatedly.
Checked that the message came from the configured chat ID.
Compared the received text with /status, /on, and /off.
Controlled the relay connected to GPIO2.
Returned the sensor and relay information through Telegram.
Purpose
This task converts the project from a local sensor system into a remotely controlled IoT system.
Screenshot evidence
Insert your screenshot here:
text
[Insert Task 3 Telegram commands screenshot here]
The screenshot should show:
text
/status
/on
/off
and the corresponding bot replies.

Task 4 — Automatic Temperature Control
Function
Task 4 adds automatic temperature-based behavior using a threshold of 27 °C.
The ESP32 checks the temperature every five seconds and decides whether to send an alert or turn off the relay automatically.
Temperature below 27 °C
When the temperature is below 27 °C:
The bot sends no high-temperature alerts.
If the relay is on, the ESP32 turns it off automatically.
The bot sends one AUTO-OFF notification.
The same AUTO-OFF notification is not repeated continuously.
Example:
text
AUTO-OFF
Temperature: 26 C
Temperature is below 27 C.
Relay turned OFF automatically.
Temperature at least 27 °C
When the temperature is 27 °C or higher and the relay is off:
The bot sends a high-temperature alert.
The alert is sent once every five seconds.
Alerts continue until the user sends /on.
Example:
text
ALERT!
Temperature: 28 C
Temperature is at or above 27 C.
Relay is OFF.
Send /on to turn relay ON.
After /on
When the user sends /on:
The relay turns on.
Repeated high-temperature alerts stop.
The user can continue using /status to check the system.
What was implemented
Set the temperature threshold to 27 °C.
Checked whether the temperature was below or above the threshold.
Sent alerts every five-second loop when appropriate.
Turned the relay off automatically below 27 °C.
Used a state variable to send only one AUTO-OFF notification.
Kept manual Telegram control with /status, /on, and /off.
Purpose
This task completes the automatic IoT control system. The ESP32 can now monitor the environment, notify the user, and control the relay without requiring constant manual input.
Screenshot or video evidence
Insert your evidence here:
text
[Insert Task 4 alert screenshot here]
[Insert Task 4 AUTO-OFF screenshot here]
[Insert Task 4 demonstration-video link here]
The demonstration should show:
Temperature below 27 °C.
No alert while below the threshold.
Temperature rising to at least 27 °C.
Repeated alerts while the relay is off.
/on being sent.
Alerts stopping after /on.
Temperature dropping below 27 °C.
Automatic relay shutdown.
One-time AUTO-OFF notification.

Overall System Operation
The final system follows this process:
The ESP32 starts and initializes the DHT11 and relay.
The ESP32 connects to Wi-Fi.
The DHT11 measures temperature and humidity.
The ESP32 checks for Telegram commands.
/status returns the current readings and relay state.
/on turns the relay on.
/off turns the relay off.
The ESP32 checks whether the temperature is below or above 27 °C.
If the temperature is at least 27 °C and the relay is off, Telegram alerts are sent every five seconds.
If the temperature falls below 27 °C, the relay turns off automatically and one AUTO-OFF notice is sent.
The process repeats continuously.
