import tkinter as tk
import time
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
from datetime import datetime
from pytz import utc
import requests
from PIL import Image, ImageTk
import math
import sys
import random
import os
import ast
import serial
import file1
import response_data
import datalog2
import threading

def date_time():
    now = datetime.now()
    time2 = now.strftime("%H:%M %S")
    date2 = now.strftime("%a %d, %b, %Y")
    tk.Label(root, text=time2, fg="#66ffff", bg="black", font=("Arial Rounded MT Bold", 24)).place(x=15, y=15)
    tk.Label(root, text=date2, fg="#ff99cc", bg="black", font=("Agency FB", 20,"bold")).place(x=20, y=60)
    root.after(1000, date_time) 

def text_para(word):
    words = word.split()
    wrapped_text = ""
    current_line_length = 0
    max_line_length = 80
    for word in words:
        if current_line_length + len(word) > max_line_length:
            wrapped_text += "\n\n"
            current_line_length = 0
        wrapped_text += word + " "
        current_line_length += len(word) + 1
    return wrapped_text.strip()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Now...")
        
        # Display "Speak Now..." text on canvas
        prompt_text = canvas.create_text(screen_width//2, screen_height//6, text="Speak now...", 
                                         font=("calibri", 20, "bold"), fill="#FFF3D6", anchor="s")
        canvas.update()

        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            text = "a"
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            text = "a"

        # Remove "Speak Now..." text
        canvas.delete(prompt_text)
        return text

def speech(response):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(response)
    engine.runAndWait()

def location():
    latitude = 22.6767
    longitude = 88.3791
    return latitude, longitude

def api_call(parameter):
    api_key = "API KEY"
    lat, lon = location()
    url = f"http://api.openweathermap.org/data/2.5/{parameter}?lat={lat}&lon={lon}&appid={api_key}"
    return requests.get(url)

def create_widget(parent, icon_path=None):
    frame = tk.Frame(parent, bg="black")
    img = Image.open(icon_path)
    img = img.resize((50, 50)) 
    img = ImageTk.PhotoImage(img)
    icon_label = tk.Label(frame, image=img, bg="black")
    icon_label.image = img
    icon_label.grid(row=0, column=0, padx=5)
    return frame

def gradient(val, x, y, li, font_style, gap):
    start_color = sc
    end_color = ec
    length = len(val)
    r_step = (end_color[0] - start_color[0]) / length
    g_step = (end_color[1] - start_color[1]) / length
    b_step = (end_color[2] - start_color[2]) / length
    current_x = x
    for i, char in enumerate(val): 
        r = int(start_color[0] + i * r_step)
        g = int(start_color[1] + i * g_step)
        b = int(start_color[2] + i * b_step)
        text_id = canvas.create_text(current_x, y, text=char, fill=f"#{r:02x}{g:02x}{b:02x}", font=font_style)
        li.append(text_id)
        current_x += gap

def weather():
    info = api_call("weather").json()
    info2 = api_call("air_pollution").json()
    font_style = ("Agency FB", 24)
    mappings = [
        (weather, 'old_text1', str(int(info['main']['temp'] - 273)) + " °C", 160),
        (weather, 'old_text2', str(info['main']['humidity']) + " %", 240),
        (weather, 'old_text3', str(info['clouds']['all']) + " %", 320),
        (weather, 'old_text4', str(math.ceil(info['wind']['speed'] * 3.6)) + " km/h", 400),
        (weather, 'old_text5', str(info['main']['pressure']) + " hpa", 480),
        (weather, 'old_text6', {1:"good",2:"satisfactory",3:"modrate",4:"poor",5:"very poor"}.get(info2["list"][0]["main"]["aqi"]), 560),
        (weather, 'old_text7', str((datetime.utcfromtimestamp(((info['sys']['sunrise']) + (info['timezone']))).time())), 640),
        (weather, 'old_text8', str((datetime.utcfromtimestamp(((info['sys']['sunset']) + (info['timezone']))).time())), 720),
        (weather, 'old_text9', info['weather'][0]['description'], 800),
    ]
    for attr, name, text, y in mappings:
        if hasattr(attr, name):
            for item_id in getattr(attr, name):
                canvas.delete(item_id)
        li = []
        setattr(attr, name, li)
        gradient(text, 100, y, li, font_style, 13)
    root.after(20000, weather)

def sensor_data():
    font_style = ("Agency FB", 24)
    values = [(file1.hrate, 'old_text10', 160), (file1.tem, 'old_text11', 240),
              (file1.o2, 'old_text12', 320), (file1.bmi, 'old_text13', 400)]
    for val, name, y in values:
        if hasattr(sensor_data, name):
            for item_id in getattr(sensor_data, name):
                canvas.delete(item_id)
        li = []
        setattr(sensor_data, name, li)
        gradient(val, 1400, y, li, font_style, 13)
    root.after(1000, sensor_data)

def icon():
    icons = [
        "image\\-temp.png", "image\\humidity.png", "image\\cloudy-day.png", "image\\wind1.png",
        "image\\pressure.png", "image\\-air-quality.png", "image\\sunrise.png", "image\\sunset.png",
        "image\\cloud-info.png", "image\\heart-rate.png", "image\\medical.png",
        "image\\oxygen-saturation.png", "image\\healthy.png"
    ]
    positions = [(15, 140), (15, 220), (15, 300), (15, 380), (15, 460), (15, 540),
                 (15, 620), (15, 700), (15, 780), (1315, 140), (1315, 220), (1315, 300), (1315, 380)]
    for icon_path, pos in zip(icons, positions):
        create_widget(root, icon_path).place(x=pos[0], y=pos[1])

def history():
    genai.configure(api_key="API KEY") 
    generation_config = {"temperature": 0.9, "top_p": 0.95, "top_k": 40, "max_output_tokens": 8192, "response_mime_type": "text/plain"}
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp", generation_config=generation_config)
    chat_session = model.start_chat(history=[])
    chat_session.send_message(response_data.response1)
    chat_session.send_message(response_data.algo)
    return chat_session

def handle_gemini_interaction(chat_session, text_item):
    while True:
        try:
            # Check if hrate is valid (and numeric)
            hrate_val = float(file1.h)
        except ValueError:
            hrate_val = 0

        if hrate_val > 0:
            chat_session.send_message(f"{response_data.age} {response_data.body_temperature} {file1.tem} {response_data.bmi} {file1.hrate} {response_data.blood_o2} {file1.o2} {response_data.bmi} {file1.bmi}{response_data.response2}")
            
            text = listen()

            if text in ["shutdown", "shut down"] or "shut down" in text:
                response = chat_session.send_message(text)
                threading.Thread(target=speech, args=(response.text.replace("*", ""),), daemon=True).start()
                sys.exit(0)

            elif text == "restart":
                screen()

            elif text == 'a':
                canvas.itemconfig(text_item, text=response_data.uc, fill="#9EF5FF")
                canvas.coords(text_item, screen_width/2, screen_height//6)
                for _ in range(screen_height//6):
                    canvas.move(text_item, 0, -1)
                    canvas.update()
                    time.sleep(0.01)

            else:
                response = chat_session.send_message(text)
                response_text = response.text.replace("*", "")
                wrapped_text = text_para(response_text)

                word_count = len(response_text.split())
                estimated_speech_duration = word_count / 2.5  # seconds

                scroll_steps = screen_height
                delay_per_step = estimated_speech_duration / scroll_steps

                threading.Thread(target=speech, args=(response_text,), daemon=True).start()

                canvas.itemconfig(text_item, text=wrapped_text)
                canvas.coords(text_item, screen_width/2, screen_height)
                for _ in range(scroll_steps):
                    canvas.move(text_item, 0, -1)
                    canvas.update()
                    time.sleep(delay_per_step)
        else:
            print("Waiting for valid heart rate...")
            time.sleep(1)


def screen():
    chat_session = history()
    text_item = canvas.create_text(screen_width//2, screen_height, text=response_data.intro1, font=("calibri", 20), fill="#FFF3D6", anchor="s")
    for _ in range(screen_height):
        canvas.move(text_item, 0, -1)
        canvas.update()
        time.sleep(0.01)
    thread = threading.Thread(target=handle_gemini_interaction, args=(chat_session, text_item), daemon=True)
    thread.start()

# Root setup
root = tk.Tk()
root.attributes('-fullscreen', True)
root.config(bg="black")
canvas = tk.Canvas(root, bg="black")
canvas.pack(expand=True, fill="both")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print(screen_height)
sc = (0, 255, 255)
ec = (255, 0, 102)

# Start
try:
    date_time()
    icon()
    weather()
    sensor_data()
    screen()
    root.mainloop()
except Exception as e:
    print(f"Error interacting with Gemini API: {e}")
    root.destroy()
