import serial
import re
import paho.mqtt.client as mqtt
import time

# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set('spotlight', 'tracker')  # Replace with your MQTT credentials
mqtt_client.connect("broker_ip", 1883, 60)  # Replace with your broker IP
mqtt_client.loop_start()

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")  # Debugging output

mqtt_client.on_message = on_message

def read_dwm1001_data(port="/dev/ttyACM0", baudrate=115200):
    """
    Reads serial data from the DWM1001 board and extracts anchor positions and distances.
    Publishes the extracted data to MQTT.
    """
    ser = serial.Serial(port, baudrate, timeout=1)
    
    print("Serial connection established.")  # Debugging output
    
    while True:
        print(f"Bytes available: {ser.in_waiting}")  # Debugging output
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Read from serial: {line}")  # Debugging output
            
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
                    
                    print(f"Anchors: {anchors}")  # Debugging output
                    print(f"Distances: {distances}")  # Debugging output
                    
                    # Publish to MQTT
                    mqtt_client.publish("dwm1001/anchors", str(anchors))
                    mqtt_client.publish("dwm1001/distances", str(distances))
                    print(f"Published anchors and distances to MQTT.")  # Debugging output
                    
                    return anchors, distances  # Return data for further processing

                except Exception as e:
                    print("Error parsing data:", e)

# Example usage
port = "/dev/ttyACM0"  # Change to the correct port (e.g., "/dev/ttyUSB0" on Linux)
anchors, distances = read_dwm1001_data(port)
