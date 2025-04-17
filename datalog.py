import csv
import random
import time
import file1
from datetime import datetime
import threading
def algo(heart_rate,body_temp,blood_o2,bmi):
    
    """for running purpose"""
    heart_cond=""
    if(heart_rate<60): heart_cond="Bradycardia: indicate underlying heart conditions in other disease" 
    elif(heart_rate>=60 and heart_rate<100): heart_cond ="normal condition"
    elif(heart_rate>=100 and heart_rate<150): heart_cond ="exercise, stress, anxiety, dehydration, fever"
    else : heart_cond="tracycardia: indicate serious medical conditions"
    temp_cond=""
    if(body_temp<95): temp_cond="Critical hypothermia: Shivering, slurred speech, confusion, weak pulse, shallow breathing, loss of consciousness, organ failure, towards death"
    elif(body_temp>=95 and body_temp<96.8): temp_cond="mild hypothermia: Shivering, fatigue, confusion, slurred speech, poor coordination"
    elif(body_temp>=96.8 and body_temp<98.6): temp_cond="normal condition"
    elif(body_temp>=98.6 and body_temp<100.4): temp_cond="mild fever: sweating, flushed skin, headache, muscle aches, fatigue"
    elif(body_temp>=100.4 and body_temp<102.2): temp_cond="moderate fever:Worsening of mild fever symptoms, dehydration, confusion, hallucinations"
    elif(body_temp>=102.2 and body_temp<105.8): temp_cond="high fever: Seizures, delirium, organ damage, potential for heat stroke"
    else : temp_cond="Hyperpyrexia: Rapid, weak pulse, hot, dry skin, confusion, seizures, organ failure, towards death"
    o2_cond=""
    if(blood_o2>=95 and blood_o2<=100): o2_cond="normal condition"
    elif(blood_o2>=90 and blood_o2<=94): o2_cond="Mildly low oxygen saturation: cause of concern"
    elif(blood_o2>=85 and blood_o2<=89): o2_cond="Moderately low oxygen saturation:  indicate significant hypoxia"
    elif(blood_o2<85): o2_cond="serious health complications and requires immediate medical attention."
    bmi_cond=""
    if(bmi<18.5): bmi_cond="Underweight"
    elif(bmi>=18.5 and bmi<25): bmi_cond="Healthy Weight"
    elif(bmi>=25 and bmi<30): bmi_cond="overWeight"
    elif(bmi>=30 and bmi<35): bmi_cond="obesity: class 1"
    elif(bmi>=35 and bmi<40): bmi_cond="obesity: class 2"
    elif(bmi>=40): bmi_cond="obesity: class 3"
    return [heart_cond,temp_cond,o2_cond,bmi_cond]
def generate_data(i):
  now = datetime.now()
  date=now.strftime("%Y-%m-%d")
  time=now.strftime("%H:%M:%S")
  heart_rate=file1.h
  body_temp=file1.t
  blood_o2=file1.o
  bmi=file1.b
  data=algo(heart_rate,body_temp,blood_o2,bmi)
  return [i,date,time
          ,heart_rate, data[0]
          ,body_temp, data[1]
          ,blood_o2, data[2]
          ,bmi, data[3]]

def generate_data2(i):
  
  heart_rate=file1.h
  body_temp=file1.t
  blood_o2=file1.o
  bmi=file1.b
  data=algo(heart_rate,body_temp,blood_o2,bmi)
  return [heart_rate, data[0]
          ,body_temp, data[1]
          ,blood_o2, data[2]
          ,bmi, data[3]]

def write_to_csv(filename, data):
  """Writes data to a CSV file."""
  with open(filename, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(data)

def main():
    filename = "dataset.csv"
    i=-1
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
         i=i+1
    while True:
        i=i+1
        data = generate_data(i)
        write_to_csv(filename, data)
        # print(f"Wrote data to {filename}: {data}")
        time.sleep(8)  # Adjust the sleep time as needed
        
update_thread = threading.Thread(target=main)
update_thread.daemon = True  # Set as daemon to avoid blocking program exit
update_thread.start()