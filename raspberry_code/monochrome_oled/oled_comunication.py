import sys
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep


def flash_pixel(oled, x, y, time_on):
    oled.pixel(x, y, 1)
    oled.show()
    sleep(time_on)
    oled.fill(0)
    oled.show()
    return None


def flash_rectangle(oled, x, y, lenght, height, time_on):
    oled.fill_rect(x, y, lenght, height, 1)
    oled.show()
    sleep(time_on)
    oled.fill(0)
    oled.show()
    return None


# Objeto i2c con el que nos vamos a comunicar
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
# 128 pixeles horizontales, 64 verticales
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()

keep_running = True
while keep_running:
    try:
        received_message = sys.stdin.readline().strip()
        command, *params = received_message.split()
        if command == "pixel":
            x, y, t = params
            x, y, t = int(x), int(y), float(t)
            flash_pixel(oled, x, y, t)
        if command == "rect":
            x, y, l, h, t = params
            x, y, l, h, t = int(x), int(y), int(l), int(h), float(t)
            flash_rectangle(oled, x, y, l, h, t)
    except Exception as e:
        oled.text(str(e), 0, 0)
        oled.show()
        keep_running = False
