# This is script that run when device boot up or wake from sleep.
from time import sleep
from machine import Pin
from dual_relay import DualRelayController

led = Pin(25, Pin.OUT)
led.value(1)
sleep(1)
led.value(0)
rele_control = DualRelayController()
print(rele_control.rele_values())
