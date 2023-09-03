import serial

serial_conection = serial.Serial("/dev/ttyACM0", 115200)

try:
    while True:
        message = input()
        encoded_message = (message + "\n").encode()
        serial_conection.write(encoded_message)

except KeyboardInterrupt:
    if serial_conection is not None:
        serial_conection.close()
