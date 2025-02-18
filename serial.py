import serial
import re

def read_dwm1001_data(port="/dev/ttyUSB0", baudrate=115200):
    """
    Reads serial data from the DWM1001 board and extracts anchor positions and distances.
    """
    ser = serial.Serial(port, baudrate, timeout=1)
    
    while True:
        line = ser.readline().decode('utf-8').strip()
        
        if "ANCHORS:" in line:
            try:
                data_str = line.split("ANCHORS:")[1]
                anchor_entries = data_str.split(";")[:-1]  # Remove empty last entry
                
                anchors = []
                distances = []
                
                for entry in anchor_entries:
                    x, y, z, d = map(int, entry.split(","))
                    anchors.append((x, y, z))
                    distances.append(d)
                
                print(f"Anchors: {anchors}")
                print(f"Distances: {distances}")

                return anchors, distances  # Return data for further processing

            except Exception as e:
                print("Error parsing data:", e)

# Example usage
port = "COM3"  # Change to the correct port (e.g., "/dev/ttyUSB0" on Linux)
anchors, distances = read_dwm1001_data(port)
