import sys
import serial

serial_conection = serial.Serial("/dev/ttyACM0", 115200)

try:
    t = float(sys.argv[1])
except ValueError:
    raise TypeError(f"{sys.argv[1]} is not a valid first parameter for sleep time.")

try:
    message = f"toggle {t}"
    encoded_message = (message + "\n").encode()
    serial_conection.write(encoded_message)

except KeyboardInterrupt:
    if serial_conection is not None:
        serial_conection.close()
