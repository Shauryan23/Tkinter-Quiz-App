from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import random

def submit_form():
    player_name = input_name.get()
    frame3.tkraise()
    for question in questions:
        mylabel = Label(frame3, text=question)
        mylabel.pack()
        for value,key in solutions.items():
            if question == value:
                for answer in answers:
                    if key in answer:
                        random.shuffle(answer)
                        option1 = answer[0]
                        option2 = answer[1]
                        option3 = answer[2]
                        option4 = answer[3]
                        myoptionlabel = Label(frame3)
                        myoptionlabel.pack(side=BOTTOM)
                        rb1 = Radiobutton(myoptionlabel, text=option1, variable=var2, value=option1)
                        rb1.pack()
                        rb2 = Radiobutton(myoptionlabel, text=option2, variable=var2, value=option2)
                        rb2.pack()
                        rb3 = Radiobutton(myoptionlabel, text=option3, variable=var2, value=option3)
                        rb3.pack()
                        rb4 = Radiobutton(myoptionlabel, text=option4, variable=var2, value=option4)
                        rb4.pack()
                        button.wait_variable(var)
                        mylabel.destroy()
                        myoptionlabel.destroy()
                        
    
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

#============================================== FRAME 3 ==================================================#

input_answer = StringVar()
var = IntVar()
var2 = StringVar()
var2.set(' ')
questions_attempted = 1

questions = ["The ratio of width of our National flag to its length is",
             "The words 'Satyameva Jayate' inscribed below the base plate of the emblem of India are taken from",
             "'Kathakali' is a folk dance prevalent in which state",
             "The last Mahakumbh of the 20th century was held at"]

solutions = {"The ratio of width of our National flag to its length is": "2:3",
             "The words 'Satyameva Jayate' inscribed below the base plate of the emblem of India are taken from": "Mundak Upanishad",
             "'Kathakali' is a folk dance prevalent in which state": "Karnataka",
             "The last Mahakumbh of the 20th century was held at": "Haridwar"}

answers = [["3:5", "2:3", "2:4", "3:4"],["Rigveda", "Satpath Brahmana", "Mundak Upanishad", "Ramayana"],
            ["Karnataka", "Orissa", "Kerala", "Manipur"],["Nasik", "Ujjain", "Allahabad", "Haridwar"]]

random.shuffle(questions)

button = Button(frame3, text="Next", command=lambda: var.set(1))
button.place(x=150, y=150)


show_frame(frame1)

window.mainloop()