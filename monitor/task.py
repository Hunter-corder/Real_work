import minimalmodbus
import serial
import time
from .models import VesselReading

def read_modbus_data():
    port = 'COM5'  # Adjust this to your port
    instrument = minimalmodbus.Instrument(port, 1)
    instrument.serial.baudrate = 9600

    while True:
        for vessel_no in range(5):  # Assuming max 5 vessels
            instrument.slaveaddress = vessel_no + 1
            try:
                level = instrument.read_register(vessel_no)
                VesselReading.objects.create(device_id=vessel_no + 1, level=level)
            except Exception as e:
                print(f"Error reading data from device {vessel_no + 1}: {e}")
        
        time.sleep(5)  # Adjust the sleep time as needed
