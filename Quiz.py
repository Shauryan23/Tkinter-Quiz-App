from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random # For randomizing the sequence in which questions are asked and their options are displayed
import sqlite3 # For maintaining the data of playername and their scores, adding questions & options in database

game_score = 0
player_name = ""
questions_attempted = 1 # For keeping count of questions diplayed(it'll be used to diplay FINISH BUTTON on the final question)
qualifying_score = 3
errors = None # For Error Checking while uploading question & options in database

#*********************** TIMER **************************#

time_in_sec = 20 # Total Time for Quiz

def timer():
    global time_in_sec, mylabel, button, myoptionlabel
    if(time_in_sec>0):
        minutes, seconds = divmod(time_in_sec, 60)
        time_left = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        timer_label.config(text=time_left)
        time_in_sec -= 1
        timer_label.after(1000, timer)
    else:
        mylabel.destroy()
        button.destroy()
        myoptionlabel.destroy()
        completed_session()
        
#*********************** TIMER **************************#

#************** DATABASE DATABASE DATABASE **************#

conn = sqlite3.connect('Database.db')

c = conn.cursor()

# c.execute("""CREATE TABLE QuizData(
#             name text,
#             score number
#             )
#             """)

# This function will be used later to Check If the player already exists in database
def get_player_name(player_name):
    c.execute("SELECT * FROM QuizData WHERE name=:name", {'name':player_name})
    return c.fetchone()

# This function is used to add player to the database with score
def insert_player(player_name, game_score):
    with conn:
        c.execute("INSERT INTO quizData VALUES (:name, :score)", {'name': player_name, 'score': game_score})

# This function is used to update the score of the player if he exists in the database already
def update_score(player_name, game_score):
    with conn:
        c.execute("""UPDATE QuizData SET score = :score
                    WHERE name = :name""",
                  {'name': player_name, 'score': game_score})

# To Create Table for User Added Questions and Options
# c.execute("""CREATE TABLE QuestionsData(
#             questions text,
#             options text,
#             correct_option text
#             )
#             """)

# To Add Question & Options in Database
def insert_question_options(question, options, correct_option):
    with conn:
        c.execute("INSERT INTO QuestionsData VALUES (:db_question, :db_options, :db_correct_option)", {'db_question':question, 'db_options':options, 'db_correct_option':correct_option})

# To load Questions & Options from Database
def load_questions_options():
    with conn:
        c.execute("SELECT * FROM QuestionsData")
        return c.fetchall()

#************** DATABASE DATABASE DATABASE **************#

# Function To Raise The Chosen Frame
def show_frame(frame):
    frame.tkraise()

# To Extract Player Details, Start Timer And Load Questions 
def submit_form():
    global player_name
    load_questions_options_curr_session()
    player_name = input_name.get().split()[0]
    player_name = player_name.lower()
    frame3.tkraise()
    timer()
    load_questions()

# To Extract Questions & Options From Database And append it to the Lists & Dictionary respectively
def load_questions_options_curr_session():
    global questions, solutions, answers
    curr_session = load_questions_options()
    for curr_data in curr_session:
        curr_question = curr_data[0]
        curr_options = eval(curr_data[1])       
        curr_correct_option = curr_data[2]
        
        if(curr_question not in questions):
            questions.append(curr_question)
            answers.append(curr_options)
            solutions[curr_question] = curr_correct_option
    
# Main Quiz Logic
def load_questions():
    global game_score, mylabel, button, myoptionlabel, time_in_sec, questions_attempted
    button = Button(frame3, image=next_btn, cursor = "hand2", borderwidth=0, bg="black", command=lambda: var.set(1)) # Next Button
    button.place(x=700, y= 600)
    random.shuffle(questions) # Shuffling Questions Sequence
    curr_sesh_questions = questions[0:4] # To load Only 4 Questions For Current Session
    for question in curr_sesh_questions:
        mylabel = Label(frame3, text=question, anchor=CENTER, font =("times new roman", 18, "bold"), bg= "black", fg= "white", wraplength= 800)
        mylabel.place(x=485, y=225)
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
                        myoptionlabel.place(x=700, y=330)
                        # RadioButtons For 4 Options 
                        Radiobutton(myoptionlabel, text=option1, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option1, selectcolor="#000000").pack(pady=5, anchor="w")
                        Radiobutton(myoptionlabel, text=option2, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option2, selectcolor="#000000").pack(pady=5, anchor="w")
                        Radiobutton(myoptionlabel, text=option3, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option3, selectcolor="#000000").pack(pady=5, anchor="w")
                        Radiobutton(myoptionlabel, text=option4, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option4, selectcolor="#000000").pack(pady=5, anchor="w")
                        button.wait_variable(var)
                        selected_option = var2.get()
                        if selected_option == key: # To Check If Right Option Is Selected
                            game_score += 1
                        questions_attempted += 1
                        if questions_attempted == 4: # To Check If it's the Last Question
                            # Destroy Previous Next Button And Create a New Button with Finish Text
                            button.destroy() 
                            button = Button(frame3, image=finish_btn, cursor = "hand2", borderwidth=0, bg="black", command=lambda: var.set(1))
                            button.place(x=700, y= 600)
                        mylabel.destroy()
                        myoptionlabel.destroy()
    button.destroy()
    time_in_sec = 0 # To Stop The Timer and Resume The Application Execution Process From Else Part Of The Timer

def completed_session():
    data_handling() # To Push All Data To The Database
    messagebox.showinfo("    Quiz Game", "Quiz Has Finished\n{} you have scored {} out of 4".format(player_name, game_score))
    global ok_btn, qualify_mssg, qualify_fail_mssg 
    # To Check If Player Has Passed or Failed The Quiz
    if(game_score >= qualifying_score):
        top = Toplevel()
        top.geometry("1250x780")
        qualify_mssg_label = Label(top, image=qualify_mssg)
        qualify_mssg_label.pack()
        ok_button = Button(top, image=okbtn, cursor="hand2", borderwidth=0, bg="#000000", command=top.destroy)
        ok_button.place(x=545, y=675)
    else:
        top = Toplevel()
        top.geometry("1250x780")
        qualify_mssg_label = Label(top, image=qualify_fail_mssg, bg="#4e62d2")
        qualify_mssg_label.pack()
        ok_button = Button(top, image=okbtn, cursor="hand2", borderwidth=0, bg="#000000", command=top.destroy) #, bg="#436fd2"
    show_frame(frame4)

def data_handling():
    global player_name
    # To Check If Player Already Exists in Database If Not Then Insert The Player 
    if(get_player_name(player_name) == None):
        insert_player(player_name, game_score)
    # If Player Already Exists Then Update His New Score If it is Greater Than The Previously In Database
    else:
        fetched_player = get_player_name(player_name)
        if(fetched_player[1] < game_score):
            update_score(player_name, game_score)

# To Load Top 3 Players From Database
def load_highscores(frame):
    frame.tkraise()
    c.execute("""SELECT * FROM 'QuizData'
            ORDER BY score DESC
            LIMIT 0, 3;""")
    highscores = c.fetchall()

    const_txt = "NAME" + "\t\t\t\t" + "SCORE"
    txt_label = Label(frame5, font =("Courier New", 20,"bold"), text=const_txt, pady=25, bg="#f8f8f8")
    txt_label.place(x=475, y=75)
    
    disty = 225 # This Variable Increments Accordingly To Place The Name & Score Label

    for x in range(0, 3):
        curr_player = highscores[x][0]
        curr_score = highscores[x][1]
        
        username_to_load_label = Label(frame5, font =("Courier New", 18,"bold"), text=curr_player, pady=10, bg="#f8f8f8")
        username_to_load_label.place(x=475, y=disty)
        
        userscore_to_load_label = Label(frame5, font =("Courier New", 18,"bold"), text=str(curr_score), pady=10, bg="#f8f8f8")
        userscore_to_load_label.place(x=1000, y=disty)

        disty += 90

# To Reinitialize All The Values & Jump To HomePage
def refresh_session():
    global player_name, game_score, time_in_sec, input_name
    questions_attempted = 1
    input_name.delete(0, 'end')
    txt_mail.delete(0, 'end')
    txt_contact.delete(0, 'end')
    var2.set(' ')
    game_score = 0
    time_in_sec = 20
    show_frame(frame1)

# To Add Questions & Options In The Database
def add_questions():
    global input_question, input_options, input_correct_option, my_canvas, submit_btn
    top3 = Toplevel()
    top3.geometry("1100x650")
    my_canvas = Canvas(top3)
    my_canvas.pack(fill="both", expand=True)
    my_canvas.create_image(0, 0, image=add_questions_bg, anchor="nw")
    my_canvas.create_text(153, 70, text= "Add Question :", font= ("Helvetica", 18,"bold"), fill="#ffffff", anchor="nw")
    input_question = Entry(top3)
    my_canvas.create_window(150, 100, window=input_question, width=750, anchor="nw")
    input_question.config(font= ("Helvetica", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5, highlightbackground="#74159d", highlightcolor="#74159d")
    # Options
    my_canvas.create_text(153, 180, text= "Enter Options :", font= ("Helvetica", 18,"bold"), fill="#ffffff", anchor="nw")
    input_options = Entry(top3)
    input_options.config( font= ("Helvetica", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5, highlightbackground="#74159d", highlightcolor="#74159d")
    my_canvas.create_window(150, 210, window=input_options, width=750, anchor="nw")
    # Guide
    my_canvas.create_text(153, 255, text= "**Enter 4 Options Above", font= ("Helvetica", 10,"bold"), fill="#e31313", anchor="nw")
    my_canvas.create_text(153, 273, text= "**Enter Comma Seperated values", font= ("Helvetica", 10,"bold"), fill="#e31313", anchor="nw")
    # Correct Answers
    my_canvas.create_text(153, 330, text= "Correct Option :", font= ("Helvetica", 18,"bold"), fill="#ffffff", anchor="nw")
    input_correct_option = Entry(top3)
    input_correct_option.config( font= ("Helvetica", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5, highlightbackground="#74159d", highlightcolor="#74159d")
    my_canvas.create_window(153, 360, window=input_correct_option,width=750, anchor="nw")
    my_canvas.create_text(153, 405, text= "*ENTER THE CORRECT ANSWER ABOVE(Note: It Must Be Present In The Enter Options Row **CASE SENSITIVE ", font= ("Helvetica", 10,"bold"), fill="#e31313", anchor="nw")
    # Submit Button
    submit_btn = Button(my_canvas, image=submit_btn_img, border=0, relief=FLAT, bg="#5f4bd1", cursor="hand2", command=handle_questions_options)
    submit_btn_window = my_canvas.create_window(450, 540, anchor="nw", window=submit_btn)
    # Exit Button
    form_exit_button = Button(my_canvas, image=form_exit_btn, cursor = "hand2", borderwidth=0, bg="#683ed2", command=top3.destroy)
    exit_btn_window = my_canvas.create_window(1025, 10, anchor="nw", window=form_exit_button)

# To Extract Questions & Options From Entrybox
def handle_questions_options():
    global get_question, get_options, get_correct_option, my_canvas, submit_btn, err_var
    get_question = input_question.get()
    get_options = input_options.get().split(",")
    get_correct_option = input_correct_option.get()
    # To Remove Whitespaces if any from options
    for option in get_options:
        formatted_option = option.strip()
        formatted_options_list.append(formatted_option)
    get_correct_option = get_correct_option.strip()

    # Error Checking Function Call
    validate_questions_options_data()

# Function Which Runs In Loop For Error Checking
def loop_check():
    global submit_btn, errors, err_var, get_options, get_correct_option, get_question
    while(errors):
        submit_btn.wait_variable(err_var)
        handle_questions_options()
    
    # Converting List Consisting Of Options Into String To Push it Into The Database
    get_options = repr(get_options)
    
    # Adding Data To Database
    insert_question_options(get_question, get_options, get_correct_option)
    
    # Question Added Successfully Message
    success_mssg_label = Label(my_canvas, text="Question Added Successfully!!!", bg="#5f4bd1", fg="#08ff08", font= ("Helvetica", 30,"bold"), anchor="nw")
    success_mssg_label.place(x=250, y=460)
    success_mssg_label.after(5000, success_mssg_label.destroy)

# Function To Check For Errors If Present
def validate_questions_options_data():
    global get_options, get_correct_option, err_var, errors

    # Function Which Sets Error Value To True & Enters The Loop
    def error_validator():
        global errors
        err_var.set(1)
        errors = True
        top2.destroy()
        loop_check()

    # TO Check if Only 4 Options are Present 
    if(len(get_options) != 4):
        top2 = Toplevel()
        top2.geometry("750x325")
        error_canvas = Canvas(top2)
        error_canvas.pack(fill="both", expand=True)
        error_canvas.create_image(50, 60, image=error_img, anchor="nw")
        error_canvas.create_text(120, 70, text= "Please Add Correct Number Of Options As Instructed", font= ("Helvetica", 18,"bold"), fill="#e31313", anchor="nw")
        ok_button = Button(error_canvas, image=ok_btn, cursor = "hand2", borderwidth=0, command=error_validator)
        ok_btn_window = error_canvas.create_window(315, 220, anchor="nw", window=ok_button)
    
    # To Check if Correct Option is Present in Both Rows
    elif(get_correct_option not in formatted_options_list):
        top2 = Toplevel()
        top2.geometry("925x325")
        error_canvas = Canvas(top2)
        error_canvas.pack(fill="both", expand=True)
        error_canvas.create_image(50, 60, image=error_img, anchor="nw")
        error_canvas.create_text(120, 70, text= "Please Check If Correct Option Is Present In Both The Input Rows", font= ("Helvetica", 18,"bold"), fill="#e31313", anchor="nw")
        ok_button = Button(error_canvas, image=ok_btn, cursor = "hand2", borderwidth=0, command=error_validator)
        ok_btn_window = error_canvas.create_window(375, 220, anchor="nw", window=ok_button)
    
    # Setting Errors Value to False And Entering The Loop
    else:
        errors = False
        loop_check()

window = Tk()

window.state('zoomed')

window.title("    Quiz Game")

window.iconbitmap('images/MultiUse Images/quiz.ico')

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

bg_img = PhotoImage(file="images/Home Page/bghome.png")
my_label =  Label(frame1, image=bg_img)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

start_btn = PhotoImage(file='images/Home Page/bgFormplay.png')
play_button = Button(frame1, image=start_btn, cursor = "hand2", borderwidth=0, bg="#5f4bd1", command=lambda:show_frame(frame2))
play_button.pack(side="bottom", pady=50)

exit_btn = PhotoImage(file='images/MultiUse Images/exitForm.png')
exit_button = Button(frame1, image=exit_btn, cursor = "hand2", borderwidth=0, bg="#683ed2", command=window.destroy)
exit_button.pack(padx=30, pady=30, anchor="ne")

add_questions_btn = PhotoImage(file="images/AddQuestions Page/addQuestionsbtn.png")
add_questions_button = Button(frame1, image=add_questions_btn, cursor = "hand2", borderwidth=0, bg="#9400d4", command=add_questions)
add_questions_button.place(x=1253, y=705)

error_img = PhotoImage(file="images/AddQuestions Page/error2.png")
ok_btn = PhotoImage(file="images/AddQuestions Page/okbtn.png")

#============================================== FRAME 2 ==================================================#

bg2_img = PhotoImage(file='images/UserDetails Page/bgbgbg.png')
my_label2 = Label(frame2, image=bg2_img)
my_label2.place(x=0, y=0, relwidth=1, relheight=1)

form = PhotoImage(file="images/UserDetails Page/bgForm3.png")
form_label = Label(frame2, image=form)
form_label.place(x=475, y=170, width=135, height=180)

title = Label (frame2, text= "Player Details", font= ("times new roman", 20,"bold"), bg="#3683d1", fg="#ffffff").place(x=725, y=50)

# First Row
name = Label (frame2, text= "Player Name", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff").place(x=650, y=175)
input_name = Entry(frame2, font= ("times new roman", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5)
input_name.config(highlightbackground="#74159d", highlightcolor="#74159d")
input_name.place(x=650, y=205, width=270)

form_exit_btn = PhotoImage(file="images/MultiUse Images/exitForm.png")
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

form_start_button = Button(frame2, image=start_btn, cursor = "hand2", borderwidth=0, bg="#5f4bd1", command=submit_form)
form_start_button.pack(side="bottom", pady=50)

#============================================== FRAME 3 ==================================================#

quiz_bg_img = PhotoImage(file="images/Quiz Page/finalquizbg.png")
img_label = Label(frame3, image=quiz_bg_img)
img_label.place(x=0, y=0, relheight=1,relwidth=1)

# NEXT BUTTON & FINISH BUTTON
next_btn = PhotoImage(file="images/Quiz Page/nextF3.png")
finish_btn = PhotoImage(file="images/Quiz Page/finishF2.png")

# Label for Questions
mylabel = Label()

# Label for Options
myoptionlabel = Label()

# Button for Next/Finish
button = Button()

# Label for Timer
timer_label = Label(frame3, font="times 50", fg="#FFFFFF", bg="#000000")
timer_label.place(x=1200, y=80)

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

#============================================== FRAME 4 ==================================================#

score_bg_img = PhotoImage(file="images/Last Page/quizscorebg.png")

score_img_label = Label(frame4, image=score_bg_img, width=1920)
score_img_label.place(x=0, y=0, relheight=1,relwidth=1)

bact_to_home_btn = PhotoImage(file="images/Last Page/PlayAgain.png")
bact_to_home_button = Button(frame4, image=bact_to_home_btn, bg="#f8f8f8", cursor = "hand2", borderwidth=0, command=refresh_session)
bact_to_home_button.place(x=500 , y=50)

view_highscore_btn = PhotoImage(file="images/Last Page/Highscore2.png")
view_highscore_button = Button(frame4, image=view_highscore_btn, bg="#f8f8f8", cursor = "hand2", borderwidth=0, command=lambda:load_highscores(frame5))
view_highscore_button.place(x=500 , y=400)

#============================================== FRAME 5 ==================================================#

last_page_bg_label = Label(frame5, image=score_bg_img, width=1920)
last_page_bg_label.place(x=0, y=0, relheight=1,relwidth=1)

highscore_exit_btn = PhotoImage(file="images/Last Page/bg1exit.png")
highscore_exit_button = Button(frame5, image=highscore_exit_btn, cursor = "hand2", borderwidth=0, bg="white", command=refresh_session)
highscore_exit_button.pack(padx=30, pady=30, anchor="ne")

#============================================== FRAME 6 ==================================================#

okbtn = PhotoImage(file="images/QualifyingMessage Page/okbtn2.png")
qualify_mssg = PhotoImage(file="images/QualifyingMessage Page/qualify_mssg2.png")
qualify_fail_mssg = PhotoImage(file="images/QualifyingMessage Page/qualify_failmssg2.png")

#============================================== ADD QUESTION CANVAS ==================================================#
add_questions_bg = PhotoImage(file="images/AddQuestions Page/addQuestionbg.png")
submit_btn_img = PhotoImage(file="images/AddQuestions Page/submitbtn.png")

submit_btn = Button()

my_canvas = Canvas(width=1100, height=650)

get_question = ""
get_options = ""
get_correct_option = ""

input_question = Entry()
input_options = Entry()
input_correct_option = Entry()

formatted_options_list = []

err_var = IntVar()

show_frame(frame1)

window.mainloop()

conn.close()