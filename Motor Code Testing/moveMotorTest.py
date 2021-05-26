import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(8, GPIO.OUT) # enable rotation pin

pwm = GPIO.PWM(8, 100) # pulse width modulation

def reprintMenu():
    print("MENU")
    print("1 - Turn On")
    print("2 - Turn Off")
    print("3 - Exit")
    print("4 - Half Circle")
    print("5 - 50%")
    print("6 - 25%")
    print("7 - 100%")

reprintMenu()

while True:
    check = int(input("Option: "))

    if check == 1:
        print("Turning On...")
        GPIO.output(8, False)
    elif check == 2:
        print("Turning Off...")
        GPIO.output(8, True)
    elif check == 3:
        print("Exiting...")
        GPIO.output(8, True)
        GPIO.cleanup()
        exit()
    elif check == 4:
        GPIO.output(8,False)
        time.sleep(0.65)
        GPIO.output(8,True)
    elif check == 5:
        pwm.ChangeDutyCycle(50)
    elif check == 6:
        pwm.ChangeDutyCycle(75)
    elif check == 7:
        pwm.ChangeDutyCycle(0)
    else:
        print("Not an option.")

