from tkinter import *
from tkinter.ttk import *
from table_generator import generate_table
import pdf_to_jpg
import detect_square
from PIL import Image

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('500x900')

questions_number = IntVar()
questions_number.set(25)

answers_number = IntVar()
answers_number.set(4)

questions = []
question_values = []
question_nums = []


def add_radiobuttons(question, answers):
    global questions
    global question_nums
    global question_values
    questions = []
    question_values = []
    question_nums = []
    for i in range(question):
        questions.append([])
        v = IntVar()
        question_values.append(v)
        lb = Label(window, text=str(i))
        lb.grid(column=0, row=i + 3)
        question_nums.append(lb)
        for j in range(answers):
            rad = Radiobutton(window, text=chr(j + ord('A')), value=j, variable=v)
            rad.grid(column=j + 1, row=i + 3)
            questions[i].append(rad)


def update_questions():
    global questions
    global question_nums
    for i in question_nums:
        i.grid_forget()
    for i in questions:
        for j in i:
            j.grid_forget()
    add_radiobuttons(questions_number.get(), answers_number.get())


def generate_pdf():
    generate_table("output.pdf", answers_number.get(), questions_number.get())


def check_answers():
    RANDOM_PDF = 'data/pdf/chuj.pdf'
    RANDOM_JPG = 'data/jpg/Document.jpg'
    RANDOM_OUTPUT = 'data/out/Output-Random.jpg'
    x, y = generate_table("output.pdf", answers_number.get(), questions_number.get())
    answers = detect_square.find_squares(RANDOM_JPG, RANDOM_OUTPUT, x, y)
    pdf_to_jpg.convert(RANDOM_PDF, RANDOM_JPG)
    print(len(question_values))
    if len(answers) == len(question_values):
        correct = 0
        for i in range(len(answers)):
            print(str(answers[i]) + " " + str(question_values[i].get()))
            if answers[i] == question_values[i].get():
                correct += 1
        print(correct)
    else:
        print("Wrong number of questions")

    Image.open(RANDOM_OUTPUT).show()


spin = Spinbox(window, from_=0, to=100, width=5)

lbl = Label(window, text="Number of questions: ")
lbl.grid(column=0, row=0)

spin = Spinbox(window, from_=0, to=25, width=5, textvariable=questions_number, command=update_questions)
spin.grid(column=1, row=0)

lbl = Label(window, text="Number of answers: ")
lbl.grid(column=0, row=1)

spin = Spinbox(window, from_=2, to=6, width=5, textvariable=answers_number, command=update_questions)
spin.grid(column=1, row=1)


def clicked():
    print(answers_number.get())
    print(questions_number.get())


add_radiobuttons(questions_number.get(), answers_number.get())

btn = Button(window, text="Generate pdf", command=generate_pdf)
btn.grid(column=2, row=0)
btn = Button(window, text="Check answers", command=check_answers)
btn.grid(column=2, row=1)

window.mainloop()
