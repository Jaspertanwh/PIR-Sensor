import RPi.GPIO as GPIO
import os
import configparser
import time
import requests
import threading

# Get the full path to the configuration file
config_file_path = os.path.join("/home/pi/sensor", "config.ini")

# Initialize and read the configparser
config = configparser.ConfigParser()
config.read(config_file_path)

# Access configuration settings
PIR_GPIO_1 = config.getint("Settings", "PIR_GPIO_1")
PIR_GPIO_2 = config.getint("Settings", "PIR_GPIO_2")
LED_GPIO_1 = config.getint("Settings", "LED_GPIO_1")
LED_GPIO_2 = config.getint("Settings", "LED_GPIO_2")

system_id = config.get("Settings", "system_id")
company_id = config.get("Settings", "company_id")
site_id = config.getint("Settings", "site_id")
user_id = config.getint("Settings", "user_id")
sensor_id_1 = config.getint("Settings", "sensor_id_1")
sensor_id_2 = config.getint("Settings", "sensor_id_2")

# Initialize and read the configparser
config = configparser.ConfigParser()
config.read(config_file_path)

# Setup GPIO
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins
GPIO.setup(PIR_GPIO_1, GPIO.IN)
GPIO.setup(PIR_GPIO_2, GPIO.IN)
GPIO.setup(LED_GPIO_1, GPIO.OUT)
GPIO.setup(LED_GPIO_2, GPIO.OUT)


GPIO.output(LED_GPIO_1, GPIO.HIGH)
GPIO.output(LED_GPIO_2, GPIO.HIGH)
time.sleep(2)  # Keep LED on for 2 seconds
GPIO.output(LED_GPIO_1, GPIO.LOW)
GPIO.output(LED_GPIO_2, GPIO.LOW)


def sendAlertToSGEMS(sensor_id):
    if system_id not in ["sgems", "sgemsuat"]:
        baseURL = f"http://{system_id}"
    else:
        baseURL = f"https://{system_id}.logicsmartsoln.com"

    url = f"{baseURL}/{company_id}/api/recording/uploadSensorData"

    payload = {
        "site_id": site_id,
        "sensor_id": sensor_id,
        "user_id": user_id,
        "sensor_value": "1",
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(
            "Lift Emergency Sensor Log has been sent to SGEMS Portal and SGEMS Notifier"
        )
        return True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False


# Function to control LED for a given PIR sensor
def monitor_pir(pir_pin, led_pin, sensor_id):
    while True:
        if GPIO.input(pir_pin):
            print(f"Motion Detected by PIR {pir_pin}!")
            GPIO.output(led_pin, GPIO.HIGH)
            sendAlertToSGEMS(sensor_id)
            time.sleep(2)  # Keep LED on for 5 seconds
            GPIO.output(led_pin, GPIO.LOW)
        time.sleep(0.2)  # Check sensor every 0.2 second


try:
    print("PIR Sensor Test (CTRL+C to exit)")
    time.sleep(2)  # Allow sensors to stabilize

    # Create and start threads for both PIR sensors
    pir_1_thread = threading.Thread(target=monitor_pir, args=(PIR_GPIO_1, LED_GPIO_1,sensor_id_1))
    pir_2_thread = threading.Thread(target=monitor_pir, args=(PIR_GPIO_2, LED_GPIO_2,sensor_id_2))

    pir_1_thread.start()
    pir_2_thread.start()

    # Keep the main program running
    pir_1_thread.join()
    pir_2_thread.join()

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()  # Clean up GPIO on exit
