import sys
from machine import Pin
from time import sleep

mem_0 = Pin(0, Pin.OUT)  # membrana externa, en 0 la mantiene cerrada
mem_1 = Pin(1, Pin.OUT)  # membrana interna, en 0 la mantiene abierta
# Arranca todo en 0 para el seteo manual
mem_0.value(0)
mem_1.value(0)
print(f"mem_0 = {mem_0.value()}")
print(f"mem_1 = {mem_1.value()}")
# Cuando quiero medir, abro la externa y al terminar, cierro la interna
recibiendo = True
while recibiendo:
    command = sys.stdin.readline().strip()
    if command != "":
        mem_0.value(1)
        print(f"mem_0 = {mem_0.value()}")
        # midiendo
        sleep(1)
        # terminamos
        mem_1.value(1)
        print(f"mem_1 = {mem_1.value()}")
        sleep(1)
        mem_0.value(0)
        print(f"mem_0 = {mem_0.value()}")
        mem_1.value(0)
        print(f"mem_1 = {mem_1.value()}")
