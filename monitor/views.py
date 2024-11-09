import minimalmodbus
import serial
import threading
import time
from django.shortcuts import render
from django.http import JsonResponse
from .models import VesselReading

# Global variables
max_vessel_no = 5
last_error = None

# Function to read Modbus data and update the database
def read_modbus_data():
    global last_error
    port = 'COM5'
    connected = False
    instrument = None

    # Attempt to establish a connection
    while not connected:
        try:
            instrument = minimalmodbus.Instrument(port=port, slaveaddress=1)
            instrument.serial.baudrate = 9600
            instrument.serial.bytesize = 8
            instrument.serial.parity = serial.PARITY_NONE
            instrument.serial.stopbits = 1
            connected = True
        except Exception as e:
            last_error = f"Could not connect to the device via {port}: {str(e)}"
            time.sleep(5)  # Wait before retrying

    # Start reading data
    while connected:
        try:
            for vessel_no in range(max_vessel_no):
                instrument.slaveaddress = vessel_no + 1
                level = instrument.read_register(vessel_no)
                # Save to the database
                save_to_database(vessel_no + 1, level)

            # Wait for 5 seconds before reading again
            time.sleep(5)

        except Exception as e:
            last_error = f"Unexpected error: {str(e)}"
            time.sleep(5)

    if instrument is not None:
        try:
            instrument.serial.close()
        except Exception as e:
            last_error = f"Error closing port: {str(e)}"

# Function to save readings to the database
def save_to_database(device_id, level):
    reading = VesselReading(device_id=device_id, level=level)
    reading.save()

# Function to fetch the latest vessel readings as JSON
def get_vessel_readings(request):
    latest_readings = {}

    # Fetch the latest data for each vessel from the database
    for device_id in range(1, max_vessel_no + 1):
        latest_reading = VesselReading.objects.filter(device_id=device_id).order_by('-timestamp').first()
        latest_readings[device_id] = latest_reading.level if latest_reading else None

    # Return the data as JSON, including the last error message
    return JsonResponse({'readings': latest_readings, 'error': last_error})

# View to render the dashboard
def vessel_dashboard(request):
    # Dictionary to store the latest readings for each vessel
    latest_readings = {}
    vessel_positions = []
    
    # Fetch the latest readings for each vessel from the database
    for device_id in range(1, max_vessel_no + 1):
        latest_reading = VesselReading.objects.filter(device_id=device_id).order_by('-timestamp').first()
        latest_readings[device_id] = latest_reading.level if latest_reading else None
    
    # Precompute the left position for each vessel and get their corresponding level
    for index, device_id in enumerate(range(1, max_vessel_no + 1)):
        left_position = 176 + index * 40  # Calculate left position (you can adjust this as needed)
        level = latest_readings.get(device_id, None)
        vessel_positions.append({
            'device_id': device_id, 
            'left_position': left_position, 
            'level': level
        })

    # Fetch the latest error message to display (if any)
    error_message = last_error

    # Pass the data to the template
    return render(request, 'monitor/vessel_data.html', {
        'vessel_positions': vessel_positions,
        'max_vessel_no': max_vessel_no,  # pass the max vessel count for potential usage in the template
        'error_message': error_message  # pass the error message to the template
    })

# Start the background task when the server starts
def start_background_task():
    thread = threading.Thread(target=read_modbus_data)
    thread.daemon = True
    thread.start()
