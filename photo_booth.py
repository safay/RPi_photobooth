#!/usr/bin/python

# ensure this script runs at startup to run headless with booth setup
# Raspberry Pi script by Scott Fay, December 2013
# include list of dependencies here
# add in future: reset button (another script running in the background), error handling for out-of-paper, out-of-toner

import RPi.GPIO as GPIO, time, os, subprocess


# set up GPIO
GPIO.setmode(GPIO.BCM)
SWITCH = 24
RESET = 25
PRINT_LED = 22
POSE_LED = 18
BUTTON_LED = 23
GPIO.setup(RESET, GPIO.IN)
GPIO.setup(SWITCH, GPIO.IN)
GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.setup(PRINT_LED, GPIO.OUT)

GPIO.output(BUTTON_LED, True)
GPIO.output(PRINT_LED, False)
GPIO.output(POSE_LED, False)

# main photobooth loop
while True:
  if (GPIO.input(SWITCH)):
    snap = 0
    while snap < 4:  # start 4 photo sequence
      print("pose!")
      GPIO.output(BUTTON_LED, False)
      GPIO.output(POSE_LED, True)
      time.sleep(1.5)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.4)
        GPIO.output(POSE_LED, True)
        time.sleep(0.4)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.1)
        GPIO.output(POSE_LED, True)
        time.sleep(0.1)
      GPIO.output(POSE_LED, False)
      print("SNAP")
      gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename /home/pi/photobooth_images/photobooth%H%M%S.jpg", stderr=subprocess.STDOUT, shell=True) # take the photo, save with timestamp in name to distinguish uniques
      print(gpout)
      # checks to see if photo was taken successfully; keeps trying if not
      if "ERROR" not in gpout: 
        snap += 1
      GPIO.output(POSE_LED, False)
      time.sleep(0.5)
    print("please wait while your photos print...")
    GPIO.output(PRINT_LED, True)
    # build image and send to printer
    subprocess.call("sudo /home/pi/scripts/photobooth/assemble_and_print", shell=True)
    # pause needed so print queue doesn't get overwhelmed
    time.sleep(160)
    print("ready for next round!")
    GPIO.output(PRINT_LED, False)
    GPIO.output(BUTTON_LED, True)
