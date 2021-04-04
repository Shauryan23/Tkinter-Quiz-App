from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import sqlite3

game_score = 0
questions_attempted = 1
player_name = ""
score_txt=""

#***************************************** DATABASE DATABASE DATABASE *****************************************#

conn = sqlite3.connect('Database.db')

c = conn.cursor()

c.execute("""CREATE TABLE QuizData(
            name text,
            score number
            )
            """)

def get_player_name(player_name):
    c.execute("SELECT * FROM QuizData WHERE name=:name", {'name':player_name})
    return c.fetchone()

def insert_player(player_name, game_score):
    with conn:
        c.execute("INSERT INTO quizData VALUES (:name, :score)", {'name': player_name, 'score': game_score})

def update_score(player_name, game_score):
    with conn:
        c.execute("""UPDATE QuizData SET score = :score
                    WHERE name = :name""",
                  {'name': player_name, 'score': game_score})

#***************************************** DATABASE DATABASE DATABASE *****************************************#

def show_frame(frame):
    frame.tkraise()
    
def submit_form():
    global player_name, questions_attempted, game_score
    player_name = input_name.get().split()[0]
    player_name = player_name.lower()
    frame3.tkraise()
    button = Button(frame3, image=next_btn, cursor = "hand2", borderwidth=0, bg="black", command=lambda: var.set(1))
    button.place(x=700, y= 600)
    for question in questions:
        mylabel = Label(frame3, text=question, anchor=CENTER, font =("times new roman", 18, "bold"), bg= "black", fg= "white", wraplength= 800)
        mylabel.place(x=485 , y=150)
        for value,key in solutions.items():
            if question == value:
                for answer in answers:
                    if key in answer:
                        random.shuffle(answer)
                        option1 = answer[0]
                        option2 = answer[1]
                        option3 = answer[2]
                        option4 = answer[3]
                        myoptionlabel = Label(frame3, bg="black")
                        myoptionlabel.place(x=700, y=300)
                        Radiobutton(myoptionlabel, text=option1, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option1, selectcolor="#000000").pack(pady=5, anchor="w")
                        Radiobutton(myoptionlabel, text=option2, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option2, selectcolor="#000000").pack(pady=5, anchor="w")
                        Radiobutton(myoptionlabel, text=option3, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option3, selectcolor="#000000").pack(pady=5, anchor="w")
                        Radiobutton(myoptionlabel, text=option4, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option4, selectcolor="#000000").pack(pady=5, anchor="w")
                        button.wait_variable(var)
                        selected_option = var2.get()
                        if selected_option == key:
                            game_score += 1
                        questions_attempted += 1
                        if questions_attempted == 4:
                            button.destroy()
                            button = Button(frame3, image=finish_btn, cursor = "hand2", borderwidth=0, bg="black", command=lambda: var.set(1))
                            button.place(x=700, y= 600)
                        mylabel.destroy()
                        myoptionlabel.destroy()
    button.destroy()
    data_handling()
    messagebox.showinfo("    Quiz Game", "Quiz Has Finished\n{} you have scored {} out of 5".format(player_name, game_score))
    show_frame(frame4)

def data_handling():
    global player_name
    if(get_player_name(player_name) == None):
        insert_player(player_name, game_score)
    else:
        fetched_player = get_player_name(player_name)
        if(fetched_player[1] < game_score):
            update_score(player_name, game_score)

def load_highscores(frame):
    frame.tkraise()
    c.execute("""SELECT * FROM 'QuizData'
            ORDER BY score DESC
            LIMIT 0, 4;""")
    highscores = c.fetchall()

    const_txt = "NAME" + "\t\t\t\t" + "SCORE"

    txt_label = Label(frame5, font =("Courier New", 20,"bold"), text=const_txt, pady=25, bg="#f8f8f8")
    txt_label.place(x=475, y=75)
    
    disty = 225

    for x in range(0, 4):
        curr_player = highscores[x][0]
        curr_score = highscores[x][1]
        
        username_to_load_label = Label(frame5, font =("Courier New", 18,"bold"), text=curr_player, pady=10, bg="#f8f8f8")
        username_to_load_label.place(x=475, y=disty)
        
        userscore_to_load_label = Label(frame5, font =("Courier New", 18,"bold"), text=str(curr_score), pady=10, bg="#f8f8f8")
        userscore_to_load_label.place(x=1000, y=disty)

        disty += 60

window = Tk()

window.state('zoomed')

window.title("    Quiz Game")

window.iconbitmap('images\quiz.ico')

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
frame1 = Frame(window)
frame2 = Frame(window)
frame3 = Frame(window)
frame4 = Frame(window)
frame5 = Frame(window)

for frame in (frame1, frame2, frame3, frame4, frame5):
    frame.grid(row=0,column=0,sticky='nsew')

#============================================== FRAME 1 ==================================================#

bg_img = PhotoImage(file="images/bghome.png")
my_label =  Label(frame1, image=bg_img)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

start_btn = PhotoImage(file='images/bgFormplay.png')
play_button = Button(frame1, image=start_btn, cursor = "hand2", borderwidth=0, bg="#5f4bd1", command=lambda:show_frame(frame2))
play_button.pack(side="bottom", pady=50)

exit_btn = PhotoImage(file='images/exitForm.png')
exit_button = Button(frame1, image=exit_btn, cursor = "hand2", borderwidth=0, bg="#683ed2", command=window.destroy)
exit_button.pack(padx=30, pady=30, anchor="ne")

#============================================== FRAME 2 ==================================================#

bg2_img = PhotoImage(file='images/bgbgbg.png')
my_label2 = Label(frame2, image=bg2_img)
my_label2.place(x=0, y=0, relwidth=1, relheight=1)

form = PhotoImage(file="images/bgForm3.png")
form_label = Label(frame2, image=form)
form_label.place(x=475, y=170, width=135, height=180)

title = Label (frame2, text= "Player Details", font= ("times new roman", 20,"bold"), bg="#3683d1", fg="#ffffff").place(x=725, y=50)

# First Row
name = Label (frame2, text= "Player Name", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff").place(x=650, y=175)
input_name = Entry(frame2, font= ("times new roman", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5)
input_name.config(highlightbackground="#74159d", highlightcolor="#74159d")
input_name.place(x=650, y=205, width=270)

form_exit_btn = PhotoImage(file="images/exitForm.png")
form_exit_button = Button(frame2, image=form_exit_btn, cursor = "hand2", borderwidth=0, bg="#683ed2", command=lambda:show_frame(frame1))
form_exit_button.pack(padx=30, pady=30, anchor="ne")

# Second Row
mail = Label (frame2, text= "Email Id", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff").place(x=650, y=260)
txt_mail = Entry (frame2, font= ("times new roman", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5)
txt_mail.config(highlightbackground="#74159d", highlightcolor="#74159d")
txt_mail.place(x=650, y=290, width=270)

# Third Row
contact = Label (frame2, text= "Contact Number", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff").place(x=650, y=345)
txt_contact = Entry (frame2, font= ("times new roman", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5)
txt_contact.config(highlightbackground="#74159d", highlightcolor="#74159d")
txt_contact.place(x=650, y=375, width=270)

# Fourth Row
Stream = Label (frame2, text= "Stream", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff", highlightthickness=5).place(x=650, y=430)

combo_stream = ttk.Combobox (frame2, font=("times new roman", 14), state='readonly', justify=CENTER)
combo_stream['values'] = ("Select your Stream", "Comps", "IT", "Extc", "Mechanical", "Civil")
combo_stream.place(x=650, y=460, width=270)
combo_stream.current(0)

form_start_btn = PhotoImage(file="images/bgFormplay.png")

form_start_button = Button(frame2, image=form_start_btn, cursor = "hand2", borderwidth=0, bg="#5f4bd1", command=submit_form)
form_start_button.pack(side="bottom", pady=50)

#============================================== FRAME 3 ==================================================#

quiz_bg_img = PhotoImage(file="images/finalquizbg.png")
img_label = Label(frame3, image=quiz_bg_img)
img_label.place(x=0, y=0, relheight=1,relwidth=1)

# NEXT BUTTON & FINISH BUTTON
next_btn = PhotoImage(file="images/nextF3.png")
finish_btn = PhotoImage(file="images/finishF2.png")

input_answer = StringVar()
var = IntVar()
var2 = StringVar()
var2.set(' ')

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

#============================================== FRAME 4 ==================================================#

score_bg_img = PhotoImage(file="images/quizscorebg.png")

score_img_label = Label(frame4, image=score_bg_img, width=1920)
score_img_label.place(x=0, y=0, relheight=1,relwidth=1)

bact_to_home_btn = PhotoImage(file="images/backtohome.png")
bact_to_home_button = Button(frame4, image=bact_to_home_btn, cursor = "hand2", borderwidth=0, command=lambda:show_frame(frame1))
bact_to_home_button.place(x=700 , y=250)

view_highscore_btn = PhotoImage(file="images/Highscore.png")
view_highscore_button = Button(frame4, image=view_highscore_btn, cursor = "hand2", borderwidth=0, command=lambda:load_highscores(frame5))
view_highscore_button.place(x=700 , y=475)

#============================================== FRAME 5 ==================================================#

last_page_bg = PhotoImage(file="images/quizscorebg.png")
last_page_bg_label = Label(frame5, image=last_page_bg, width=1920)
last_page_bg_label.place(x=0, y=0, relheight=1,relwidth=1)

highscore_exit_btn = PhotoImage(file="images/bg1exit.png")
highscore_exit_button = Button(frame5, image=highscore_exit_btn, cursor = "hand2", borderwidth=0, bg="white", command=lambda:show_frame(frame1))
highscore_exit_button.pack(padx=30, pady=30, anchor="ne")

show_frame(frame1)

window.mainloop()

conn.close()