import os
import threading
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from bs4 import BeautifulSoup

from ufc import get_fighter
from pprint import pprint
from src.fighter import Fighter
from src.misc import *


def get_fighter_info1():
    try:
        info1 = get_fighter("Jon Jones")
        fighter1 = Fighter(
            info1["name"],
            info1["age"],
            info1["height"],
            info1["losses"],
            info1["wins"],
            info1["strikes"],
            info1["takedowns"],
            info1["weight_class"],
            info1["fights"],
        )
        pprint(vars(fighter1))
    except BaseException as e:
        print(e)
        print("Fighter name is not valid")


def get_fighter_info2():
    try:
        info2 = get_fighter("Brandon Moreno")
        fighter2 = Fighter(
            info2["name"],
            info2["age"],
            info2["height"],
            info2["losses"],
            info2["wins"],
            info2["strikes"],
            info2["takedowns"],
            info2["weight_class"],
            info2["fights"],
        )
        pprint(vars(fighter2))
        # pprint(info2)
    except BaseException as e:
        print(e)
        print("Fighter name is not valid")


def main_gui():
    root = tk.Tk()
    root.title("UFC Matchup Predictor")

    label1 = tk.Label(root, text="Fighter 1")
    label1.grid(row=0, column=0, padx=20, pady=10)

    label2 = tk.Label(root, text="Fighter 2")
    label2.grid(row=0, column=1, padx=20, pady=10)

    # fighter name user inputs
    input1 = tk.Entry(root, text="Enter fighter1 name")
    input1.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

    input2 = tk.Entry(root, text="Enter fighter2 name")
    input2.grid(row=1, column=1, sticky="ew", padx=20, pady=10)

    # fighter name labels
    fighter_name_label1 = tk.Label(root, text="Fighter 1", font=("Arial", 36))
    fighter_name_label1.grid(row=3, column=0, sticky="ew", pady=(20, 0))

    fighter_name_label2 = tk.Label(root, text="Fighter 2", font=("Arial", 36))
    fighter_name_label2.grid(row=3, column=1, sticky="ew", pady=(20, 0))

    root.rowconfigure(4, minsize=500)
    root.columnconfigure(0, minsize=400)
    root.columnconfigure(1, minsize=400)

    # fighter images
    img1 = Image.open("./image/default2.png")
    img1 = img1.resize((250, 386))
    img_tk1 = ImageTk.PhotoImage(img1)
    panel1 = tk.Label(root, image=img_tk1)
    panel1.grid(row=4, column=0)

    img2 = Image.open("./image/test.png")
    img2 = img2.resize((250, 386))
    img_tk2 = ImageTk.PhotoImage(img2)
    panel2 = tk.Label(root, image=img_tk2)
    panel2.grid(row=4, column=1)

    # lock in buttons
    button1 = tk.Button(
        root,
        text="Lock In Fighter 1",
        command=lambda: update_fighter(
            "chan-sung-jung", "test1.png", fighter_name_label1
        ),
    )
    button1.grid(row=2, column=0)

    button2 = tk.Button(
        root,
        text="Lock In Fighter 2",
        command=lambda: update_fighter("jon-jones", "test2.png", fighter_name_label2),
    )
    button2.grid(row=2, column=1)

    analyze_button = tk.Button(
        root,
        text="Start Analyzing",
    )
    analyze_button.grid(row=5, column=0, columnspan=2, padx=25, pady=25)

    # Run the main loop
    root.mainloop()


def update_fighter(fighter_name, image_name, label):
    url = f"https://www.ufc.com/athlete/{fighter_name}"

    try:
        response = requests.get(url, stream=True)
        soup = BeautifulSoup(response.content, "html.parser")

        # fighter image from ufc.com
        img_url = (
            soup.find("div", {"class": "hero-profile__image-wrap"})
            .find("img")
            .get("src")
        )

        image_response = requests.get(img_url)
        img = Image.open(BytesIO(image_response.content))

        image_path = os.path.join("image", image_name)
        img.save(image_path)

        label.config(text=query_to_name(fighter_name))

        # return image_path
    except:
        print("image unable to retrieve")
        # return os.path.join("image", "default.jpg")

    # photo = ImageTk.PhotoImage(img)


def run():
    t1 = threading.Thread(target=get_fighter_info1)
    t2 = threading.Thread(target=get_fighter_info2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def analyze_outcome(fighter1, fighter2):
    pass


if __name__ == "__main__":
    # run()

    main_gui()

    # get_image(f"islam-makhachev", "test.png")
