import RPi.GPIO as GPIO
import time

# Set up GPIO mode and pin
GPIO.setmode(GPIO.BCM)

PIR_GPIO = 4
LED_GPIO = 27

GPIO.setup(PIR_GPIO, GPIO.IN)
GPIO.setup(LED_GPIO, GPIO.OUT)

try:
    print("PIR Sensor Test (CTRL+C to exit)")
    time.sleep(2)  # Allow sensor to stabilize

    while True:
        if GPIO.input(PIR_GPIO):
            print("Motion Detected!")
            GPIO.output(LED_GPIO, GPIO.HIGH)
            time.sleep(5)
        else:
            print("No Motion")
            GPIO.output(LED_GPIO, GPIO.LOW)
        time.sleep(0.2)  # Check sensor every 0.2 second

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()  # Clean up GPIO on exit
