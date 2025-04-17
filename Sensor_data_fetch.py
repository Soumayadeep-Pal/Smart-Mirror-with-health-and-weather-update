import random
import threading
import time
import algorithm
import serial
import ast
hrate = "null"
h=0
tem = "null"
t=0
o2 = "null"
o=0
bmi="null"
b=0
def main():
    """Continuously updates a shared variable with a random value between 0 and 100."""
    global hrate
    global tem
    global o2
    global bmi
    global h
    global t
    global o
    global b
    ser = serial.Serial("COM7", 115200)
    while True:
        
        data = ser.readline().decode().strip()
        print(data)
        data = ast.literal_eval(data)
        # hrate=data.get("BPM","")
        # o2=data.get("Temp_F","")
        # tem=data.get("SpO2","")
        
        h=data['BPM']
        t=data['Temp_F']
        o=data['SpO2']
        b=data['BMI']
        
        # h=(random.randint(50, 110))
        hrate = str(h)+" BPM"
        # t=(random.uniform(90, 110))
        tem = str("%.2f"%t)+" °F"
        # o=(random.randint(80, 100))
        o2 = str(o)+" %"
        # b=(random.randint(10,40))
        bmi=str(b)+" kg/m2"
        time.sleep(1)  # Update every second (adjust as needed)

# Start the update thread in the background
update_thread = threading.Thread(target=main)
update_thread.daemon = True  # Set as daemon to avoid blocking program exit
update_thread.start()

