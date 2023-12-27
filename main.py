import os
import threading
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from bs4 import BeautifulSoup

from ufc import get_fighter
from pprint import pprint
from fighter import Fighter


def get_fighter_info1():
    try:
        info1 = get_fighter("Jon Jones")
        fighter1 = Fighter(
            info1["name"],
            info1["height"],
            info1["losses"],
            info1["wins"],
            info1["strikes"],
            info1["takedowns"],
            info1["weight_class"],
        )
        pprint(vars(fighter1))
    except BaseException as e:
        print("Fighter name is not valid")


def get_fighter_info2():
    try:
        info2 = get_fighter("Brandon Moreno")
        fighter2 = Fighter(
            info2["name"],
            info2["height"],
            info2["losses"],
            info2["wins"],
            info2["strikes"],
            info2["takedowns"],
            info2["weight_class"],
        )
        pprint(vars(fighter2))
    except BaseException as e:
        print("Fighter name is not valid")


def main_gui():
    root = tk.Tk()
    root.title("UFC Matchup Predictor")

    # Create and place widgets using grid
    label1 = tk.Label(root, text="Fighter 1")
    label1.grid(row=0, column=0)

    label2 = tk.Label(root, text="Fighter 2")
    label2.grid(row=0, column=1)

    input1 = tk.Entry(root, text="Enter fighter1 name")
    input1.grid(row=1, column=0, sticky="ew")

    input2 = tk.Entry(root, text="Enter fighter2 name")
    input2.grid(row=1, column=1, sticky="ew")

    button1 = tk.Button(root, text="Button")
    button1.grid(row=2, column=0, columnspan=2)  # Columnspan to span multiple columns

    # Run the main loop
    root.mainloop()


def get_image(url):
    response = requests.get(url, stream=True)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # fighter image from ufc.com
    img_url = soup.find("div", {"class": "hero-profile__image-wrap"}).find("img").get("src")
    
    image_response = requests.get(img_url)
    img = Image.open(BytesIO(image_response.content))
    img.save(os.path.join("image", "test.png"))

    # photo = ImageTk.PhotoImage(img)


def run():
    t1 = threading.Thread(target=get_fighter_info1)
    t2 = threading.Thread(target=get_fighter_info2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    # run()

    # main_gui()
    fighter_name = "chan-sung-jung"

    # get_image(f"https://www.ufc.com/athlete/islam-makhachev")
    get_image(f"https://www.ufc.com/athlete/{fighter_name}")
