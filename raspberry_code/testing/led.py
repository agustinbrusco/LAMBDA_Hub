from machine import Pin
from time import sleep

led = Pin(25, Pin.OUT)


def flash_ten_times(led: Pin) -> None:
    for i in range(10):
        sleep(0.5)
        led.toggle()
    return None


flash_ten_times(led)
