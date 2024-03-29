import serial
from pyfirmata import Arduino, util

"""Arduino
SDA -> A4, SCL -> A5"""
ser = serial.Serial('/dev/cu.usbserial-AK06G3AO')

class ArduinoData:
    """
    This class holds all the input from the arduino
    """
    def __init__(self):
        self.acc = [0,0,0]
        self.gyr = [0,0,0]
        self.force = 0

def set_Arduino_data():
    arduino = ArduinoData()
    acc_list = ["AcX", "AcY", "AcZ"]
    gyr_list = ["GyX", "GyY", "GyZ"]

    for x in range(8):
        arduinoData = ser.readline()
        if x != 0: #Skip first read beacouse of slowness in Arduino
            arduinoData = arduinoData.decode("utf-8").strip('\n').strip('\r')
            type = arduinoData[0:3]
            try:
                arduinoDataFloat = float(arduinoData[3:])
            except ValueError:
                arduinoDataFloat = 0

            if type in acc_list:
                index = acc_list.index(type)
                arduino.acc[index] = arduinoDataFloat
            if type in gyr_list:
                index = gyr_list.index(type)
                arduino.gyr[index] = arduinoDataFloat
            if type == "For":
                arduino.force = arduinoDataFloat
    return arduino
