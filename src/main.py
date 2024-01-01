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


fighter1, fighter2 = None, None


def get_fighter_info(fighter_name):
    info1 = get_fighter(fighter_name)
    if fighter_name.lower() != info1["name"].lower():
        print(f"{fighter_name.lower()} : {info1['name'].lower()}")
        print("Fighter name is not valid2")
        raise Exception
    else:
        fighter = Fighter(
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
        return fighter


def main_gui():
    root = tk.Tk()
    root.title("UFC Matchup Predictor")

    label1 = tk.Label(root, text="Fighter 1")
    label1.grid(row=0, column=0, padx=20, pady=10)

    label2 = tk.Label(root, text="Fighter 2")
    label2.grid(row=0, column=2, padx=20, pady=10)

    # fighter name user inputs
    input1 = tk.Entry(root, text="Enter fighter1 name")
    input1.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

    input2 = tk.Entry(root, text="Enter fighter2 name")
    input2.grid(row=1, column=2, sticky="ew", padx=20, pady=10)

    status_label1 = tk.Label(root, text="")
    status_label1.grid(row=2, column=0, padx=20, pady=3)
    status_label2 = tk.Label(root, text="")
    status_label2.grid(row=2, column=2, padx=20, pady=3)

    # fighter name labels
    fighter_name_label1 = tk.Label(root, text="Fighter 1", font=("Arial", 36))
    fighter_name_label1.grid(row=4, column=0, sticky="ew", pady=(20, 0))

    fighter_name_label2 = tk.Label(root, text="Fighter 2", font=("Arial", 36))
    fighter_name_label2.grid(row=4, column=2, sticky="ew", pady=(20, 0))

    vs_label = tk.Label(root, text="VS", font=("Arial", 60))
    vs_label.grid(row=4, column=1, sticky="ew", padx=25, pady=(20, 0))

    root.rowconfigure(5, minsize=500)
    root.columnconfigure(0, minsize=400)
    root.columnconfigure(2, minsize=400)

    # fighter images
    img1 = Image.open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("image", "default.png"),
        )
    )
    img1 = img1.resize((250, 386))
    img_tk1 = ImageTk.PhotoImage(img1)
    panel1 = tk.Label(root, image=img_tk1)
    panel1.grid(row=5, column=0)

    img2 = Image.open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("image", "default.png"),
        )
    )
    img2 = img2.resize((250, 386))
    img_tk2 = ImageTk.PhotoImage(img2)
    panel2 = tk.Label(root, image=img_tk2)
    panel2.grid(row=5, column=2)

    # lock in buttons
    button1 = tk.Button(
        root,
        text="Lock In Fighter 1",
        command=lambda: update_fighter(
            name_to_query(input1.get()),
            "fighter1.png",
            fighter_name_label1,
            panel1,
            1,
            status_label1,
        ),
    )
    button1.grid(row=3, column=0)

    button2 = tk.Button(
        root,
        text="Lock In Fighter 2",
        command=lambda: update_fighter(
            name_to_query(input2.get()),
            "fighter2.png",
            fighter_name_label2,
            panel2,
            2,
            status_label2,
        ),
    )
    button2.grid(row=3, column=2)

    analyze_button = tk.Button(
        root,
        text="Start Analyzing",
        command=analyze_outcome,
    )
    analyze_button.grid(row=6, column=0, columnspan=3, padx=25, pady=25)

    # Run the main loop
    root.mainloop()


def update_fighter(fighter_name, image_name, label, img_label, num, status_label):
    url = f"https://www.ufc.com/athlete/{fighter_name}"

    try:
        if num == 1:
            global fighter1
            fighter1 = get_fighter_info(query_to_name(fighter_name))
        else:
            global fighter2
            fighter2 = get_fighter_info(query_to_name(fighter_name))
    except:
        print("loading fighter info failed")
        status_label.config(
            text="Fighter info not found / Invalid fighter name", fg="red"
        )
        return

    status_label.config(text="")

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

        image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("image", image_name),
        )
        img.save(image_path)

        label.config(text=query_to_name(fighter_name))

        new_img = Image.open(image_path)
        new_img = new_img.resize((250, 386))
        new_img_tk = ImageTk.PhotoImage(new_img)

        img_label.config(image=new_img_tk)
        img_label.image = new_img_tk

        os.remove(image_path)

    except Exception as e:
        print("image unable to retrieve")
        label.config(text=query_to_name(fighter_name))

        default_image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("image", "default.png"),
        )

        new_img = Image.open(default_image_path)
        new_img = new_img.resize((250, 386))
        new_img_tk = ImageTk.PhotoImage(new_img)

        img_label.config(image=new_img_tk)
        img_label.image = new_img_tk


def analyze_outcome():
    global fighter1
    global fighter2

    if fighter1 == None or fighter2 == None:
        print("Two fighters need to be loaded in order to start analyzing")
        return

    pprint(vars(fighter1))
    pprint(vars(fighter2))


if __name__ == "__main__":
    main_gui()
