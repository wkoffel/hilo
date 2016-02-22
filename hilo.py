#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Example using a character LCD connected to a Raspberry Pi or BeagleBone Black.
import time

import Adafruit_CharLCD as LCD

import RPi.GPIO as GPIO
import forecastio

forecastio_api_key = ""

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


forecast = forecastio.load_forecast(forecastio_api_key, lat, lng)
byDay = forecast.daily()
print byDay.summary
print byDay.icon

for dailyData in byDay.data:
    print dailyData.time.strftime('%l:%M%p %Z on %b %d, %Y')
    print dailyData.summary
    print dailyData.temperatureMin
    print dailyData.temperatureMax
    print "\n"



message = "Hello Will\nReady To Serve"

lcd.set_backlight(1)
lcd.show_cursor(True)
lcd.blink(True)
lcd.message(message)
time.sleep(5.0)
lcd.blink(False)
lcd.show_cursor(False)
lcd.clear()
lcd.set_backlight(0)


# Stop blinking and showing cursor.
#lcd.show_cursor(False)
#lcd.blink(False)

# Demo scrolling message right/left.
#lcd.clear()
#message = 'Scroll'
#lcd.message(message)
#print range(lcd_columns-len(message))
#for i in range(lcd_columns-len(message)):
#	time.sleep(0.5)
#	lcd.move_right()
#for i in range(lcd_columns-len(message)):
#	time.sleep(0.5)
#	lcd.move_left()

# Demo turning backlight off and on.
#lcd.clear()
#lcd.message('Flash backlight\nin 5 seconds...')
#time.sleep(5.0)
# Turn backlight off.
#lcd.set_backlight(0)
#time.sleep(2.0)
# Change message.
#lcd.clear()
#lcd.message('Goodbye!')
# Turn backlight on.
#lcd.set_backlight(1)
