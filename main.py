from tkinter import *
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

#* ----------------------------------------------------- READ CSV FILE -----------------------------------------

try:
    df = pd.read_csv("./data/words_to_learn.csv") # read the Chinese and English words that has been learned by the user from the csv
except FileNotFoundError:
    df = pd.read_csv("./data/english-chinese.csv") # read the csv file
finally: # if the code in "try" block is failed or succeed, get the data from `english-chinese.csv`
    to_learn = df.to_dict(orient="records") # convert the dataframe into a well formatted dictionary in a list, orient = 'dict', list, 'series', 'split', 'records', 'index'
    
# print(data_dict)

#* ------------------------------------------------ UPDATE GUI WHEN BUTTON IS CLICKED ----------------------------------
random_word_dict = {}


def next_card():
    global random_word_dict
    # window.after_cancel(flip_card_timer) # cancel the timer loop when user press the button, means start over the timer countdown
    if len(to_learn) != 0: # check if there is still some more words need to learn
        random_word_dict = choice(to_learn) # random pick a pair of word from the data dictionary
        canvas.itemconfig(card_color, image=front_image) # change to front card
        canvas.itemconfig(canvas_title, text="English", fill="black") # change the title to "English" and text color to black
        canvas.itemconfig(canvas_word, text=random_word_dict["English"], fill="black") # change to next English word from the random picked dictionary
        # flip_card_timer = window.after(3000, func=flip_card) # start the timer countdown to flip the card
    else: # if no more word need to learn
        canvas.itemconfig(canvas_title, text="", fill="black") # change the title to "English" and text color to black
        canvas.itemconfig(canvas_word, text="You've learned all the words! Congratulation!", fill="black", width=770) # change to next English word from the random picked dictionary
        wrong_button.config(state=DISABLED)
        flip_card_button.config(state=DISABLED)
        right_button.config(state=DISABLED)
        

    
def flip_card():
    canvas.itemconfig(card_color, image=back_image) # change to back card
    canvas.itemconfig(canvas_title, text="Chinese", fill="white") # change the title to "Chinese" and text color to black
    canvas.itemconfig(canvas_word, text=random_word_dict["Chinese"], fill="white") # change to next Chinese word from the random picked dictionary, pair of English word

    
def right_button():
    to_learn.remove(random_word_dict)
    data = pd.DataFrame(to_learn) # convert the current data list into a dataframe, with index
    # print(data)
    # English Chinese
    # 0      abandon      放弃
    # 1      ability      能力
    # ...        ...     ...
    # 2995  yourself     你自己
    # 2996     youth      青年
    
    next_card()

    data.to_csv("./data/words_to_learn.csv", index=False)


#* ----------------------------------------------------- UI SETUP -----------------------------------------
window = Tk()
window.title("English to Chinese Flash Card Application")
window.config(padx = 50, pady = 50, bg = BACKGROUND_COLOR)
# flip_card_timer = window.after(3000, func=flip_card) # start the timer when user first run the program to flip the card

front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_color = canvas.create_image(400, 263, image=front_image)
canvas_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=3)

wrong_button_img = PhotoImage(file="./images/wrong.png",)
wrong_button = Button(image=wrong_button_img, command=next_card)
wrong_button.grid(row=1, column=0)

flip_card_image = PhotoImage(file="./images/see_translation.png")
flip_card_button = Button(image=flip_card_image, command=flip_card, bg=BACKGROUND_COLOR, highlightthickness=0)
flip_card_button.grid(row=1, column=1)

right_button_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_img, command=right_button)
right_button.grid(row=1, column=2)

next_card() # generate a random word when run the program

window.mainloop()