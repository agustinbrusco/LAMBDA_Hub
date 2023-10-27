import sys
import serial

serial_conection = serial.Serial("/dev/ttyACM0", 115200)

axis = sys.argv[1]
if axis not in ["col", "row"]:
    raise ValueError(
        f"{sys.argv[1]} is not a valid oled axis. Expected values are 'row' or 'col'."
    )
try:
    t = float(sys.argv[2])
except ValueError:
    raise TypeError(f"{sys.argv[2]} is not a valid first parameter for sleep time.")

try:
    # Fila de oled = columna CCD
    message = f"toggle{axis} {t}"
    encoded_message = (message + "\n").encode()
    serial_conection.write(encoded_message)

except KeyboardInterrupt:
    if serial_conection is not None:
        serial_conection.close()
