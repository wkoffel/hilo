#!/usr/bin/env python
# -*- coding: utf-8 -*-

# first load environment files for necessary private variables
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# now import everything else
import time
import datetime
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import forecastio

forecastio_api_key = os.environ.get("FORECAST_IO_API_KEY")

# For home in Sudbury
lat = 42.3664429
lng = -71.4524137

lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_backlight(0)

# The actual work, doing the forecast
def show_forecast():
    dayToShow = 0
    if(datetime.datetime.now().hour > 17):
        dayToShow = 1
    
    lcd.show_cursor(True)
    lcd.blink(True)
    lcd.message("Fetching\nForecast")
    time.sleep(1.0) # Sleep a second to build suspense, API is fast!
    
    forecast = forecastio.load_forecast(forecastio_api_key, lat, lng)
    current = forecast.currently()
    temp = str(int(round(current.temperature)))
    byDay = forecast.daily()
    today = byDay.data[dayToShow]
    summary = today.summary
    line1 = today.time.strftime('%A')
    hi = str(int(round(today.temperatureMax)))
    lo = str(int(round(today.temperatureMin)))
    line2 = temp + "F L:" +lo + " H:" + hi

    lcd.clear()
    lcd.message(line1 + "\n" + line2)
    lcd.show_cursor(False)
    lcd.blink(False)
    time.sleep(5.0)
    lcd.set_backlight(0)
    lcd.clear()

buttons = ( (LCD.SELECT, 'Select', (1,1,1)),
            (LCD.LEFT,   'Left'  , (1,0,0)),
            (LCD.UP,     'Up'    , (0,0,1)),
            (LCD.DOWN,   'Down'  , (0,1,0)),
            (LCD.RIGHT,  'Right' , (0,1,1)) )

# And we trigger it from a simple button press
while True:
    for button in buttons:
        if lcd.is_pressed(button[0]):
            # Button is pressed, change the message and backlight.
            lcd.set_color(button[2][0], button[2][1], button[2][2])
            show_forecast()
