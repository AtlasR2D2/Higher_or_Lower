import random
from flask import Flask
from bs4 import BeautifulSoup
from selenium import webdriver
import time

app = Flask(__name__)

WINNING_NUMBER = 0
MIN_NUMBER = 0
MAX_NUMBER = 9

PUPPY_URL = "https://giphy.com/search/puppy"
puppy_gif = ""

def initialise_puppy_gifs():
    # First check to see whether puppy gifs already on file
    try:
        with open("puppy_gifs.txt","r") as puppy_file:
            gifs = puppy_file.read().splitlines()
    except IOError:
        chrome_driver_path = r'chromedriver.exe'
        driver = webdriver.Chrome(executable_path=chrome_driver_path)
        driver.get(url=PUPPY_URL)
        time.sleep(2)
        html_text = driver.page_source
        soup = BeautifulSoup(html_text, "html.parser")
        gifs = [img["src"] for img in soup.find_all(name="img", class_="giphy-gif-img") if img["src"][-3:] == "gif"]
        with open("puppy_gifs.txt", "w") as puppy_file:
            for gif in gifs:
                puppy_file.write(f"{gif}\n")
        driver.quit()
    return gifs

puppy_gifs = initialise_puppy_gifs()

def make_attribute(function, attribute, color):
    return f"<{attribute} style='color: {color}'>{function()}</{attribute}>"


def make_bold_black(function):
    def wrapper(*args,**kwargs):
        attribute = "b"
        return make_attribute(function, attribute, "black")
    return wrapper

def make_bold_red(function):
    def wrapper(*args, **kwargs):
        attribute = "b"
        return make_attribute(function, attribute, "red")
    return wrapper

def make_bold_orange(function):
    def wrapper(*args, **kwargs):
        attribute = "b"
        return make_attribute(function, attribute, "orange")
    return wrapper

def make_bold_green(function):
    def wrapper(*args, **kwargs):
        attribute = "b"
        return make_attribute(function, attribute, "green")
    return wrapper



@app.route('/')
@make_bold_black
def game_start():
    global WINNING_NUMBER
    random.seed()
    WINNING_NUMBER = random.randint(0, 9)
    print(f"WINNING_NUMBER: {WINNING_NUMBER}")
    return f'<h1>Guess a number between {MIN_NUMBER} and {MAX_NUMBER}</h1>' \
           '<br>' \
           '<img src="https://i.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.webp" width=250>'

@make_bold_red
def invalid_answer_too_big():
    return f'<h1>Number bigger than MAX_NUMBER: {MAX_NUMBER}.<br>Number must be within allowable range {MIN_NUMBER} to {MAX_NUMBER}.<br>Try again!</h1>' \
           f'<br>' \
           f'<img src="{puppy_gif}">'

@make_bold_red
def invalid_answer_too_small():
    return f'<h1>Number smaller than MIN_NUMBER: {MIN_NUMBER}.<br>Number must be within allowable range {MIN_NUMBER} to {MAX_NUMBER}.<br>Try again!</h1>' \
           f'<br>' \
           f'<img src="{puppy_gif}">'

@make_bold_orange
def wrong_answer_too_big():
    return f'<h1>Too high, try again!</h1>' \
           f'<br>' \
           f'<img src="{puppy_gif}">'

@make_bold_orange
def wrong_answer_too_small():
    return f'<h1>Too low, try again!</h1>' \
           f'<br>' \
           f'<img src="{puppy_gif}">'

@make_bold_green
def correct_answer():
    return f'<h1>You found me!</h1>' \
           f'<br>' \
           f'<img src="{puppy_gif}">'

@app.route("/<int:number>")
# @make_bold
def reveal_outcome(number):
    global puppy_gif
    if number != WINNING_NUMBER:
        random.seed()
        puppy_gif = puppy_gifs[random.randint(1, len(puppy_gifs) - 1)]
        if number > MAX_NUMBER:
            return invalid_answer_too_big()
        elif number < MIN_NUMBER:
            return invalid_answer_too_small()
        elif number > WINNING_NUMBER:
            return wrong_answer_too_big()
        else:
            return wrong_answer_too_small()
    else:
        puppy_gif = puppy_gifs[0]
        return correct_answer()



# @app.route("/bye")
# @make_bold
# @make_emphasis
# @make_underline
# def bye():
#     return "Bye!"

# @app.route("/username/<name>/<int:number>")
# def greet(name, number):
#     return f"Hello {name}, you are {number} times annoying today!"

if __name__ == "__main__":
    app.run(debug=True)