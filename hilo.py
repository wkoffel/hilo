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

# Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 21
lcd_d7        = 22
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
			   lcd_columns, lcd_rows, lcd_backlight, invert_polarity=False)
lcd.set_backlight(0)
lcd.clear()

# pin to actually fetch forecast and display
forecast_pin = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(forecast_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Now the actual work, doing the forecast
def show_forecast():
    dayToShow = 0
    if(datetime.datetime.now().hour > 17):
        dayToShow = 1
    
    lcd.set_backlight(1)
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

# And we trigger it from a simple button press
while True:
    input_state = GPIO.input(forecast_pin)
    if input_state == False:
        show_forecast()
