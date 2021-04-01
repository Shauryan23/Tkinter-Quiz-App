from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk


def submit_form():
    player_name = input_name.get()
    frame3.tkraise()
    
def show_frame(frame):
    frame.tkraise()
    
window = tk.Tk()

window.state('zoomed')

window.title("    Quiz Game")

window.iconbitmap('images\quiz.ico')

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
frame1 = tk.Frame(window)
frame2 = tk.Frame(window)
frame3 = tk.Frame(window)

for frame in (frame1, frame2, frame3):
    frame.grid(row=0,column=0,sticky='nsew')

#================== Frame 1 ========================#

bg_img = tk.PhotoImage(file="images/bghome.png")
my_label =  tk.Label(frame1, image=bg_img)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

start_btn = tk.PhotoImage(file='images/bgFormplay.png')
play_button = tk.Button(frame1, image=start_btn, borderwidth=0, bg="#5f4bd1", command=lambda:show_frame(frame2))
play_button.pack(side="bottom", pady=50)

exit_btn = tk.PhotoImage(file='images/exitForm.png')
exit_button = tk.Button(frame1, image=exit_btn, borderwidth=0, bg="#683ed2", command=window.destroy)
exit_button.pack(padx=30, pady=30, anchor="ne")

#==================# Frame 2 #========================#
# #4a66d3
bg2_img = tk.PhotoImage(file='images/bgbgbg.png')
my_label2 = tk.Label(frame2, image=bg2_img)
my_label2.place(x=0, y=0, relwidth=1, relheight=1)

form = tk.PhotoImage(file="images/bgForm3.png")
form_label = tk.Label(frame2, image=form)
form_label.place(x=475, y=170, width=135, height=180)

title = tk.Label (frame2, text= "Player Details", font= ("times new roman", 20,"bold"), bg="#3683d1", fg="#ffffff").place(x=725, y=50)

# First Row
name = tk.Label (frame2, text= "Player Name", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff").place(x=650, y=175)
input_name = tk.Entry(frame2, font= ("times new roman", 14),bg="#8319d3", fg="#ffffff")
input_name.place(x=650, y=205, width=270)

form_exit_btn = tk.PhotoImage(file="images/exitForm.png")
form_exit_button = tk.Button(frame2, image=form_exit_btn, borderwidth=0, bg="#683ed2", command=lambda:show_frame(frame1))
form_exit_button.pack(padx=30, pady=30, anchor="ne")

# Second Row
mail = tk.Label (frame2, text= "Email Id", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff").place(x=650, y=260)
txt_mail = tk.Entry (frame2, font= ("times new roman", 14),bg="#8319d3", fg="#ffffff").place(x=650, y=290, width=270)

# Third Row
contact = tk.Label (frame2, text= "Contact Number", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff").place(x=650, y=345)
txt_contact = tk.Entry (frame2, font= ("times new roman", 14),bg="#8319d3", fg="#ffffff").place(x=650, y=375, width=270)

# Fourth Row
Stream = tk.Label (frame2, text= "Stream", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff").place(x=650, y=430)

combo_stream = ttk.Combobox (frame2, font=("times new roman", 14), state='readonly', justify=CENTER)
combo_stream['values'] = ("Select your Stream", "Comps", "IT", "Extc", "Mechanical", "Civil")
combo_stream.place(x=650, y=460, width=270)
combo_stream.current(0)

form_start_btn = tk.PhotoImage(file="images/bgFormplay.png")

form_start_button = tk.Button(frame2, image=form_start_btn, borderwidth=0, bg="#5f4bd1", command=submit_form)
form_start_button.pack(side="bottom", pady=50)

#================== Frame 3 code
frame3_title=  tk.Label(frame3, text='Page 3',font='times 35', bg='green')
frame3_title.pack(fill='both', expand=True)

frame3_btn = tk.Button(frame3, text='Enter',command=lambda:show_frame(frame1))
frame3_btn.pack(fill='x',ipady=15)

show_frame(frame1)

window.mainloop()

