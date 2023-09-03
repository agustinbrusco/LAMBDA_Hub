import sys
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep

# Objeto i2c con el que nos vamos a comunicar
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
# 128 pixeles horizontales, 64 verticales
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()

while True:
    command = sys.stdin.readline().strip()
    if command != "":
        oled.fill(1)
        oled.show()
        sleep(5)
        oled.fill(0)
        oled.show()
