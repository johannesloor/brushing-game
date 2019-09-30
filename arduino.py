import serial
from pyfirmata import Arduino, util

"""Arduino
SDA -> A4, SCL -> A5"""
ser = serial.Serial('/dev/cu.usbmodem1411')

class ArduinoData:
    """
    This class holds all the input from the arduino
    """
    def __init__(self):
        self.acc = ["x", "y", "z"]
        self.gyr = ["x", "y", "z"]


def set_Arduino_data():
    arduino = ArduinoData()

    for x in range(6):
        arduinoData = ser.readline().decode("utf-8").strip('\n').strip('\r')
        try:
            arduinoData = int(arduinoData)

        except ValueError:
            arduinoData = 0

        if (x < 3):
            arduino.gyr[x] = arduinoData
        else:
            arduino.acc[x-3] = arduinoData
    return arduino
