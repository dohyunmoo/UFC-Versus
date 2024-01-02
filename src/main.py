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
settings_open = False

metrics = {
    "weight-class": 100,
    "age": 80,
    "technics": 60,
    "height": 40,
    "UFC-experience": 20,
}


def get_fighter_info(fighter_name):
    info = get_fighter(fighter_name)
    if fighter_name.lower() != info["name"].lower():
        print(f"{fighter_name.lower()} : {info['name'].lower()}")
        print("Fighter name is not valid2")
        raise Exception
    else:
        fighter = Fighter(
            info["name"],
            info["age"],
            info["height"],
            info["losses"],
            info["wins"],
            info["strikes"],
            info["takedowns"],
            info["weight_class"],
            info["fights"],
        )
        return fighter


def main_gui():
    root = tk.Tk()
    root.title("UFC Matchup Predictor")
    root.option_add("*Font", ("Calibri"))

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
    default_img = Image.open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("image", "default.png"),
        )
    )
    default_img = default_img.resize((250, 386))
    default_img_tk = ImageTk.PhotoImage(default_img)
    panel1 = tk.Label(root, image=default_img_tk)
    panel1.grid(row=5, column=0)

    panel2 = tk.Label(root, image=default_img_tk)
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
    analyze_button.grid(row=6, column=1, columnspan=2, pady=25)

    settings_button = tk.Button(
        root,
        text="Settings",
        command=lambda: open_settings(root),
    )
    settings_button.grid(row=6, column=0, padx=25, pady=25)

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


def open_settings(root):
    global settings_open
    global metrics

    if not settings_open:
        settings_window = tk.Toplevel(root)
        settings_window.title("Settings")

        settings_title = tk.Label(
            settings_window, text="Analysis Criteria", font=("Calibri", 24)
        )
        settings_title.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=20
        )

        current_label = tk.Label(settings_window, text="Current Value")
        current_label.grid(row=1, column=1)

        new_label = tk.Label(settings_window, text="New Value")
        new_label.grid(row=1, column=2)

        weight_class_label = tk.Label(settings_window, text="Weight Class: ")
        weight_class_label.grid(row=2, column=0)

        weight_current_class_label = tk.Label(
            settings_window, text=str(metrics["weight-class"])
        )
        weight_current_class_label.grid(row=2, column=1)

        weight_class_input = tk.Entry(settings_window)
        weight_class_input.grid(row=2, column=2, padx=10, pady=15)

        age_label = tk.Label(settings_window, text="Age: ")
        age_label.grid(row=3, column=0)

        age_current_label = tk.Label(settings_window, text=str(metrics["age"]))
        age_current_label.grid(row=3, column=1)

        age_input = tk.Entry(settings_window)
        age_input.grid(row=3, column=2, padx=10, pady=15)

        technics_label = tk.Label(settings_window, text="Technics: ")
        technics_label.grid(row=4, column=0)

        technics_current_label = tk.Label(
            settings_window, text=str(metrics["technics"])
        )
        technics_current_label.grid(row=4, column=1)

        technics_input = tk.Entry(settings_window)
        technics_input.grid(row=4, column=2, padx=10, pady=15)

        height_label = tk.Label(settings_window, text="Height: ")
        height_label.grid(row=5, column=0)

        height_current_label = tk.Label(settings_window, text=str(metrics["height"]))
        height_current_label.grid(row=5, column=1)

        height_input = tk.Entry(settings_window)
        height_input.grid(row=5, column=2, padx=10, pady=15)

        experience_label = tk.Label(settings_window, text="UFC Fight Experience: ")
        experience_label.grid(row=6, column=0)

        experience_current_label = tk.Label(
            settings_window, text=str(metrics["UFC-experience"])
        )
        experience_current_label.grid(row=6, column=1)

        experience_input = tk.Entry(settings_window)
        experience_input.grid(row=6, column=2, padx=10, pady=15)

        save_button = tk.Button(
            settings_window,
            text="Save",
            command=lambda: on_settings_close(settings_window),
        )
        save_button.grid(row=7, column=0, columnspan=3, pady=20)

        settings_open = True

        settings_window.protocol(
            "WM_DELETE_WINDOW", lambda: on_settings_close(settings_window)
        )
    else:
        print("Settings open already")

def save_metrics():
    pass


def on_settings_close(window):
    global settings_open
    settings_open = False

    window.destroy()


if __name__ == "__main__":
    main_gui()
