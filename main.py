from tkinter import *
import pandas as pd
import random

BG_COLOR = "#B1DDC6"
get_word = {}

try:
    df = pd.read_csv("to_learn.csv")
    df_dic = df.to_dict(orient="records")
except FileNotFoundError:
    df = pd.read_csv("french_words.csv")
    df_dic = df.to_dict(orient="records")


window = Tk()
window.title("Flash Card")
window.minsize(width=800, height=650)
window.config(bg=BG_COLOR, pady=50, padx=50)


img_right = PhotoImage(file="right.png")
img_wrong = PhotoImage(file="wrong.png")
img_card_front = PhotoImage(file="card_front.png")
img_card_back = PhotoImage(file="card_back.png")


def card_back():
    canvas.itemconfig(title, fill="white", text="English")
    canvas.itemconfig(word, fill="white", text=get_word["English"])
    canvas.itemconfig(canvas_bg, image=img_card_back)


def next_word():
    global get_word, card_flip
    window.after_cancel(card_flip)
    get_word = random.choice(df_dic)
    get_word_fr = get_word["French"]
    canvas.itemconfig(title, text="French", fill="#000")
    canvas.itemconfig(word, text=get_word_fr, fill="#000")
    canvas.itemconfig(canvas_bg, image=img_card_front)
    card_flip = window.after(3000, func=card_back)


def delete_word():
    df_dic.remove(get_word)
    # print(len(df_dic))
    to_learn_df = pd.DataFrame(df_dic)
    to_learn_df.to_csv("to_learn.csv")
    next_word()


canvas = Canvas(width=800, height=560, highlightthickness=0, bg=BG_COLOR)
canvas_bg = canvas.create_image(400, 280, image=img_card_front)
canvas.grid(row=0, column=0, columnspan=2)

right_btn = Button(image=img_right, highlightbackground=BG_COLOR, command=delete_word)
right_btn.grid(row=1, column=1)

wrong_btn = Button(image=img_wrong, highlightbackground=BG_COLOR, command=next_word)
wrong_btn.grid(row=1, column=0)

title = canvas.create_text(400, 100, text="", font=("Futura", 30, "italic"))
word = canvas.create_text(400, 250, text="", font=("Futura", 60, "italic"))

card_flip = window.after(3000, func=card_back)

next_word()
window.mainloop()
