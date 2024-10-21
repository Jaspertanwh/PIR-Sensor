import RPi.GPIO as GPIO
import time
import threading

# Set up GPIO mode and pins
GPIO.setmode(GPIO.BCM)

PIR_GPIO_1 = 14  # First PIR sensor
PIR_GPIO_2 = 15  # Second PIR sensor
LED_GPIO_1 = 17  # LED for first PIR sensor
LED_GPIO_2 = 0  # LED for second PIR sensor

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


# Function to control LED for a given PIR sensor
def monitor_pir(pir_pin, led_pin):
    while True:
        if GPIO.input(pir_pin):
            print(f"Motion Detected by PIR {pir_pin}!")
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(2)  # Keep LED on for 5 seconds
            GPIO.output(led_pin, GPIO.LOW)
        time.sleep(0.2)  # Check sensor every 0.2 second


try:
    print("PIR Sensor Test (CTRL+C to exit)")
    time.sleep(2)  # Allow sensors to stabilize

    # Create and start threads for both PIR sensors
    pir_1_thread = threading.Thread(target=monitor_pir, args=(PIR_GPIO_1, LED_GPIO_1))
    pir_2_thread = threading.Thread(target=monitor_pir, args=(PIR_GPIO_2, LED_GPIO_2))

    pir_1_thread.start()
    pir_2_thread.start()

    # Keep the main program running
    pir_1_thread.join()
    pir_2_thread.join()

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()  # Clean up GPIO on exit
