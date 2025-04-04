import time
import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext, PhotoImage, simpledialog
import threading
import pygame
from PIL import Image, ImageTk

#Some silly init stuff
pygame.mixer.init()
loop = True
snooze_time = 8
triggered_today = set()
alarm_sound1 = pygame.mixer.Sound("wake.mp3")

#Play alarm once i make the sounds lol
def play_alarm_sound():
    global loop
    if loop:
        alarm_sound1.play(loops=-1)

#Gets the current time
def check_clock():
    time_display.config(text=datetime.datetime.now().strftime("%I:%M %p"))
    root.after(1000, check_clock)

#Determines if the alarm should go off
def check_alarm():
    now = datetime.datetime.now().strftime("%H:%M")
    global loop
    for alarm in alarms:
        if alarm == now and alarm not in triggered_today and loop:
            log_message("ITS TIME BABY GIRL")
            play_alarm_sound()
            triggered_today.add(alarm)
    loop = True
    root.after(1000, check_alarm)

#Sets an alarm
def add_alarm():
    alarm = alarm_time.get().strip()
    if alarm and alarm not in alarms:
        alarms.append(alarm)
        update_alarm_list()
        alarm_time.set("")
    else:
        messagebox.showerror("Oopsies", "You fucked up not me")

#Modify an alarm if you so need be
def edit_alarm(index):
    new = tk.simpledialog.askstring("Edit Alarm", f"Edit alarm (current: {alarms[index]}):")
    if new:
        alarms[index] = new
        update_alarm_list()

#Can be called to stop the alarm if it's playing
def stop_alarm(message):
    alarm_sound1.stop()
    log_message(message)

#Pretty self explanatory I hope
def delete_alarm(index):
    del alarms[index]
    update_alarm_list()

#You know what snooze is
def snooze():
    global loop
    global snooze_time
    stop_alarm("You've defeated me for now, but I'll be back")
    root.after((snooze_time * 60000), play_alarm_sound)

#If you knew what snooze was, I'd be utterly dumbfounded if you couldn't deduce what this function does
def im_awake():
    global loop
    stop_alarm("Alright I hear ya, I really really do")
    loop = False

#The message function for the in-app text log
def log_message(message):
    log_box.config(state="normal")
    log_box.insert(tk.END, message + "\n")
    log_box.config(state="disabled")
    log_box.yview(tk.END)

#Is in charge of creating each alarm in the list once submitted via form
def update_alarm_list():
    for widget in alarm_list.winfo_children():
        widget.destroy()

    for index, alarm in enumerate(alarms):
        frame = tk.Frame(alarm_list)
        frame.pack(fill="x", pady=2)

        alarm_label = tk.Label(frame, text=alarm, font=("Arial", 12))
        alarm_label.pack(side=tk.LEFT, padx=5)

        #If you want to modify an alarm
        edit_btn = tk.Button(frame, text="✏", width=2, command=lambda i=index: edit_alarm(i))
        edit_btn.pack(side=tk.RIGHT, padx=2)

        #If you want to get rid of an alarm
        delete_btn = tk.Button(frame, text="❌", width=2, command=lambda i=index: delete_alarm(i))
        delete_btn.pack(side=tk.RIGHT, padx=2)

#The creating of the main frame and some of its settings
root = tk.Tk()
root.title("Alarm Clock")
root.config(bg="skyblue")
root.minsize(600, 600)
root.maxsize(900, 900)
root.geometry("400x400+650+150")

#Sets the icon when the app runs to the pic of evil jonesy (you can't escape him)
icon = PhotoImage(file="evil_jonesy.png")
root.iconphoto(False, icon)

#The left side of the app: The pic of evil jonesy, the list of alarms, and the field to add alarms
left_frame = tk.Frame(root, width=300, height=300, bg="skyblue")
left_frame.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)

#The frame for the picture of evil jonesy
evil_jonesy_frame = tk.Frame(left_frame, width=300, height=300)
evil_jonesy_frame.pack(padx=5, pady=5, side=tk.TOP)
tk.Label(evil_jonesy_frame, text="Evil Jonesy").pack(padx=5, pady=5)
#The original image was too large so I have to scale it down real quick
og_evil_jonesy = Image.open("evil_jonesy.png")
scaled_evil_jonesy = og_evil_jonesy.resize((200, 200), Image.Resampling.LANCZOS)
evil_jonesy_image = ImageTk.PhotoImage(scaled_evil_jonesy)
tk.Label(evil_jonesy_frame, image=evil_jonesy_image, width=200, height=200).pack()
tk.Label(evil_jonesy_frame, text="\"I'm watching you\"").pack(padx=5, pady=5)

#The frame that holds the list of alarms and the field to add alarms
alarm_frame = tk.Frame(left_frame, width=300, height=200)
alarm_frame.pack(fill="both",expand=True, anchor="w",padx=5, pady=5, side=tk.BOTTOM)
alarms = []

#Your list of alarms
alarm_list = tk.Frame(alarm_frame)
alarm_list.pack(fill="both", expand=True, pady=5)

#Where you add your alarms
alarm_form = tk.Frame(alarm_frame, width=300, height=500)
alarm_form.pack(padx=5, pady=5, side=tk.BOTTOM)
tk.Label(alarm_form, text="Set Alarm (HH:MM):").pack()
alarm_time = tk.StringVar()
tk.Entry(alarm_form, textvariable=alarm_time).pack()
tk.Button(alarm_form, text="Set Alarm", command=add_alarm).pack()

#The right frame contains the current time, the text output box, and the snooze & awake buttons
right_frame = tk.Frame(root, width=300, height=300, bg="skyblue")
right_frame.pack(padx=10,pady=10,side=tk.RIGHT)

#This alarm clock app would be a little silly if it didn't tell you the time
clock_frame = tk.Frame(right_frame, width=100, height=50, bg="skyblue")
clock_frame.pack(padx=5, pady=5)
time_display = tk.Label(clock_frame, text=datetime.datetime.now().strftime("%I:%M %p"), fg="black",bg="skyblue", font=("Helvetica", 40))
time_display.pack()
check_clock()

#The text output frame
text_output = tk.Frame(right_frame, width=300, height=10)
text_output.pack()
tk.Label(text_output, text="Output Log: ").pack()
log_box = scrolledtext.ScrolledText(text_output, width=100, height=25, state="disabled")
log_box.pack()

#Buttons!
snooze_frame = tk.Frame(right_frame, width=300, height=50, bg="red")
snooze_frame.pack(padx=5,pady=5)
snooze_button = tk.Button(snooze_frame, text="SNOOZE", font=("Helvetica", 30), command=snooze, bg="skyblue")
snooze_button.pack()
im_awake_frame = tk.Frame(right_frame, width=300, height=50, bg="red")
im_awake_frame.pack(padx=5,pady=5)
im_awake_button = tk.Button(im_awake_frame, text="I'M AWAKE", font=("Helvetica", 30), command=im_awake, bg="skyblue")
im_awake_button.pack()

#This needs to get called at least once to start so I guess it will go here
check_alarm()

#Allons-y!
root.mainloop()