# Project: Automatic Cat Feeder
# Date Due: April.3.2020
# Class: TPJ655
# Teacher: Benjamine Shefler
# Authors: Rittin Shingari (Main Programmer), Colin Robbins (Hardware and Coding Check)
# Purpose: To monitor cat food, feed the cat at the correct time and send notifications
#          to the owner to let them know when to refill the food.

# FLASK IMPORTS
from flask import Flask, request, render_template
import requests
from threading import Thread

# RASPBERRY PI IMPORTS
from datetime import datetime
import RPi.GPIO as GPIO
import time

# PYGAME IMPORTS (Used to play sound)
import pygame

# Basic Flask initialization
app = Flask(__name__,
            static_folder="static",
            template_folder="templates")


# variables used to open the files which have the saved data of
# the feed time and the cat name
f = open("feedtime.txt", "r+")
f1 = open("catname.txt", "r")

# GPIO initialization for the Raspberry Pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Enable Motor Rotational Pins
GPIO.setup(8, GPIO.OUT)   # enable rotation pin
GPIO.output(8, True)

# Function used to check the sensor input
def sensor():
    # Set percentage as 0% to begin
    percent = 0.0
    try:
        # Initialize Sensor Pins
        PIN_TRIGGER = 7
        PIN_ECHO = 11

        # Enable and setup GPIO pins to scan for distance
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        # Initial Distance variables and holder variables
        distance = [0.0]*5
        temp_distance = 0.0
        # Let the user know the sensor has settle time
        print("Waiting for sensor to settle")

        time.sleep(2)

        print("Calculating distance")
        # For loop to check and find average for increased accuracy.
        for i in range(5):
            time.sleep(2)
            GPIO.output(PIN_TRIGGER, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            while GPIO.input(PIN_ECHO) == 0:
                pulse_start_time = time.time()
            while GPIO.input(PIN_ECHO) == 1:
                pulse_end_time = time.time()

            pulse_duration = pulse_end_time - pulse_start_time
            distance[i] = round(pulse_duration * 17150, 2)
            temp_distance += distance[i]

        # Calculate average distance and return as a percentage.
        print("Distance:", temp_distance/5, "cm")
        temp_distance = temp_distance/5
        percent = (1 - (temp_distance / 18)) * 100

    except:
        print("Error occured")

    # Check to see if the % upon load is less then 20%, if so then send a notification to the user.
    try:
        if percent < 20.0:
            r = requests.post(
                'https://maker.ifttt.com/trigger/lowFood/with/key/mFJcPs0GfZCjSl6uFLKED3PYPvbt3zrJ6zRgrDR9ZvS',
                params={
                    "value1": str(percent)
                })
            print(r.text)
    except Exception:
        print("Error with webhooks")
    return round(percent, 2)

# LOAD Login Page upon initalization
@app.route('/')
def login():
    return render_template('login.html')

# LOAD main after user and password are put in correctly
@app.route('/main')
def main():
    f = open("feedtime.txt", "r")
    f1 = open("catname.txt", "r")
    obj = FeedTimeThread()
    obj.start()
    return render_template('main.html', foodValue=sensor(), feedTime=f.read(), cat_name=f1.read())

# Used to change cat name in file, modifiations are made with Javascript
@app.route("/CatName")
def CatName():
    return "nothing"

# Run the motor and initialize the chime to let the cat know food has been dispensed.
@app.route('/feedNow')
def feedNow():
    print("Feeding Now!")
    GPIO.output(8, False)
    time.sleep(0.80)
    GPIO.output(8, True)
    pygame.mixer.init()
    pygame.mixer.music.load("chime.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    percentReturned = sensor()
    return "nothing"

# Used to check and see if the cat name and feed time have been set
# if not prepares for it to be set.
@app.route("/feedTime", methods=['POST'])
def feedTime():
    if request.method == 'POST':
        time = request.form['time']
        cat = request.form['cat']
        f = open("feedtime.txt", "r")
        f1 = open("catname.txt", "r")

        if cat == "" and time != "":
            text_file = open("feedtime.txt", "w")
            text_file.write(time)
            print("time changed")
            obj = FeedTimeThread()
            obj.start()
            return render_template('main.html', foodValue=sensor(), feedTime=time, cat_name=f1.read())
        elif cat != "" and time == "":
            txt_file = open("catname.txt", "w")
            txt_file.write(cat)
            print("cat name changed")
            return render_template('main.html', foodValue=sensor(), feedTime=f.read(), cat_name=cat)
        else:
            text_file = open("feedtime.txt", "w")
            text_file.write(time)
            txt_file = open("catname.txt", "w")
            txt_file.write(cat)
            print("cat name and time changed")
            obj = FeedTimeThread()
            obj.start()
            return render_template('main.html', foodValue=sensor(), feedTime=time, cat_name=cat)

# Multithread running at all times to ensure that if time has been set it will feed at set time
class FeedTimeThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.running = True

    def run(self):

        while self.running:
            t = time.localtime()
            current_time = time.strftime("%H:%M", t)
            f = open("feedtime.txt", "r")
            time.sleep(1)
            if current_time == f.read():
                feedNow()
                break
            else:
                continue

    def stop(self):
        self.running = False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
