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
    if (
        fighter_name.lower() != info["name"].lower()
        and fighter_name.lower() != info["nickname"].lower()
    ):
        print(f"{fighter_name.lower()} : {info['name'].lower()}")
        print("Fighter name is not valid2")
        raise Exception
    else:
        fighter = Fighter(
            info["name"],
            info["nickname"],
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

    rows = {
        "title": 0,
        "subtitle": 1,
        "input": 2,
        "status": 3,
        "input-button": 4,
        "fighter-name": 5,
        "fighter-nickname": 6,
        "fighter-image": 7,
        "actions-error": 8,
        "actions": 9,
    }

    title = tk.Label(root, text="UFC Matchup Predictor", font=("Calibri", 48))
    title.grid(row=rows["title"], column=0, columnspan=3, pady=10)

    label1 = tk.Label(root, text="Fighter 1")
    label1.grid(row=rows["subtitle"], column=0, padx=20, pady=5)

    label2 = tk.Label(root, text="Fighter 2")
    label2.grid(row=rows["subtitle"], column=2, padx=20, pady=5)

    # fighter name user inputs
    input1 = tk.Entry(root, text="Enter fighter1 name")
    input1.grid(row=rows["input"], column=0, sticky="ew", padx=20, pady=5)

    input2 = tk.Entry(root, text="Enter fighter2 name")
    input2.grid(row=rows["input"], column=2, sticky="ew", padx=20, pady=5)

    status_label1 = tk.Label(root, text="")
    status_label1.grid(row=rows["status"], column=0, padx=20, pady=3)
    status_label2 = tk.Label(root, text="")
    status_label2.grid(row=rows["status"], column=2, padx=20, pady=3)

    # fighter name labels
    fighter_name_label1 = tk.Label(root, text="Fighter 1", font=("Calibri", 40))
    fighter_name_label1.grid(
        row=rows["fighter-name"], column=0, sticky="ew", pady=(10, 0)
    )

    fighter_name_label2 = tk.Label(root, text="Fighter 2", font=("Calibri", 40))
    fighter_name_label2.grid(
        row=rows["fighter-name"], column=2, sticky="ew", pady=(10, 0)
    )

    vs_label = tk.Label(root, text="VS", font=("Arial", 60))
    vs_label.grid(
        row=rows["fighter-name"], column=1, sticky="ew", padx=25, pady=(20, 0)
    )

    fighter_nickname_label1 = tk.Label(root, text='"nickname"', font=("Arial", 16))
    fighter_nickname_label1.grid(
        row=rows["fighter-nickname"], column=0, sticky="ew", pady=(0, 0)
    )

    fighter_nickname_label2 = tk.Label(root, text='"nickname"', font=("Arial", 16))
    fighter_nickname_label2.grid(
        row=rows["fighter-nickname"], column=2, sticky="ew", pady=(0, 0)
    )

    root.rowconfigure(rows["fighter-image"], minsize=500)
    root.columnconfigure(0, minsize=400)
    root.columnconfigure(2, minsize=400)

    # fighter images
    default_img = Image.open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("image", "default.png"),
        )
    )
    default_img = default_img.resize(image_ratio)
    default_img_tk = ImageTk.PhotoImage(default_img)
    panel1 = tk.Label(root, image=default_img_tk)
    panel1.grid(row=rows["fighter-image"], column=0)

    panel2 = tk.Label(root, image=default_img_tk)
    panel2.grid(row=rows["fighter-image"], column=2)

    # lock in buttons
    button1 = tk.Button(
        root,
        text="Lock In Fighter 1",
        command=lambda: update_fighter(
            name_to_query(input1.get()),
            "fighter1.png",
            fighter_name_label1,
            fighter_nickname_label1,
            panel1,
            1,
            status_label1,
        ),
    )
    button1.grid(row=rows["input-button"], column=0)

    button2 = tk.Button(
        root,
        text="Lock In Fighter 2",
        command=lambda: update_fighter(
            name_to_query(input2.get()),
            "fighter2.png",
            fighter_name_label2,
            fighter_nickname_label2,
            panel2,
            2,
            status_label2,
        ),
    )
    button2.grid(row=rows["input-button"], column=2)

    analysis_error_label = tk.Label(root, text="")
    analysis_error_label.grid(
        row=rows["actions-error"], column=0, columnspan=3, sticky="ew", pady=5
    )

    analyze_button = tk.Button(
        root,
        text="Start Analyzing",
        command=lambda: setup_analysis(analysis_error_label),
    )
    analyze_button.grid(
        row=rows["actions"], column=1, columnspan=2, sticky="w", pady=(0, 20)
    )

    settings_button = tk.Button(
        root,
        text="Settings",
        command=lambda: open_settings(root),
    )
    settings_button.grid(row=rows["actions"], column=0, padx=25, pady=(0, 20))

    # Run the main loop
    root.mainloop()


def update_fighter(
    fighter_name,
    image_name,
    fighter_name_label,
    fighter_nickname_label,
    img_label,
    num,
    status_label,
):
    try:
        if num == 1:
            global fighter1
            fighter1 = get_fighter_info(query_to_name(fighter_name))
            query_name = (name_to_query(fighter1.name), 1)
        else:
            global fighter2
            fighter2 = get_fighter_info(query_to_name(fighter_name))
            query_name = (name_to_query(fighter2.name), 2)
    except:
        print("loading fighter info failed")
        status_label.config(
            text="Fighter info not found / Invalid fighter name", fg="red"
        )
        return

    status_label.config(text="")

    print(query_name)

    url = f"https://www.ufc.com/athlete/{query_name[0]}"

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

        if query_name[1] == 1:
            fighter_name_label.config(text=fighter1.name)
            fighter_nickname_label.config(text=f'"{fighter1.nickname}"')
        elif query_name[1] == 2:
            fighter_name_label.config(text=fighter2.name)
            fighter_nickname_label.config(text=f'"{fighter2.nickname}"')

        new_img = Image.open(image_path)
        new_img = new_img.resize(image_ratio)
        new_img_tk = ImageTk.PhotoImage(new_img)

        img_label.config(image=new_img_tk)
        img_label.image = new_img_tk

        os.remove(image_path)

    except Exception as e:
        print(f"image unable to retrieve with msg: {e}")

        if query_name[1] == 1:
            fighter_name_label.config(text=fighter1.name)
            fighter_nickname_label.config(text=f'"{fighter1.nickname}"')
        elif query_name[1] == 2:
            fighter_name_label.config(text=fighter2.name)
            fighter_nickname_label.config(text=f'"{fighter2.nickname}"')

        default_image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("image", "default.png"),
        )

        new_img = Image.open(default_image_path)
        new_img = new_img.resize(image_ratio)
        new_img_tk = ImageTk.PhotoImage(new_img)

        img_label.config(image=new_img_tk)
        img_label.image = new_img_tk


def setup_analysis(error_status_label):
    global fighter1
    global fighter2
    global settings_open
    global metrics

    if fighter1 == None or fighter2 == None:
        print("Two fighters need to be loaded in order to start analyzing")
        error_status_label.config(
            text="Two fighters need to be loaded in order to start analyzing", fg="red"
        )
        return

    if settings_open:
        print("Please close the settings page to start the analysis")
        error_status_label.config(
            text="Please close the settings page to start the analysis", fg="red"
        )
        return

    # Analysis Criteria
    result_fighter1 = {
        "weight-class-score": -1,
        "age-score": 1,
        "technics-score": -1,
        "height-score": 1,
        "UFC-experience-score": 1,
    }
    result_fighter2 = {
        "weight-class-score": -1,
        "age-score": 1,
        "technics-score": -1,
        "height-score": 1,
        "UFC-experience-score": 1,
    }

    total_weight = sum(metrics.values())

    weight_class_scores = {
        "Heavyweight": (8, 35),
        "Light Heavyweight": (7, 34),
        "Middleweight": (6, 34),
        "Welterweight": (5, 32),
        "Lightweight": (4, 32),
        "Featherweight": (3, 32),
        "Bantamweight": (2, 31),
        "Flyweight": (1, 31),
    }

    pprint(vars(fighter1))
    pprint(vars(fighter2))

    # weight class difference score
    if (
        weight_class_scores[fighter1.weight_class][0]
        > weight_class_scores[fighter2.weight_class][0]
    ):
        result_fighter1["weight-class-score"] = (
            weight_class_scores[fighter1.weight_class][0]
            - weight_class_scores[fighter2.weight_class][0]
        )
    elif (
        weight_class_scores[fighter2.weight_class][0]
        > weight_class_scores[fighter1.weight_class][0]
    ):
        result_fighter2["weight-class-score"] = (
            weight_class_scores[fighter2.weight_class][0]
            - weight_class_scores[fighter1.weight_class][0]
        )

    # age difference score (closer a fighter is to the prime age of a weight class, more points are given)
    result_fighter1["age-score"] = 1 / (
        abs(int(fighter1.age) - weight_class_scores[fighter1.weight_class][1]) + 1
    )
    result_fighter2["age-score"] = 1 / (
        abs(int(fighter2.age) - weight_class_scores[fighter2.weight_class][1]) + 1
    )

    # technics score
    

    # height score
    if fighter1.height > fighter2.height:
        result_fighter2["height-score"] = fighter2.height / (fighter1.height * 1.25)
    elif fighter2.height > fighter1.height:
        result_fighter1["height-score"] = fighter1.height / (fighter2.height * 1.25)

    # experience score
    if fighter1.total_fights_in_UFC > fighter2.total_fights_in_UFC:
        result_fighter2["UFC-experience-score"] = fighter2.total_fights_in_UFC / fighter1.total_fights_in_UFC
    elif fighter2.total_fights_in_UFC > fighter1.total_fights_in_UFC:
        result_fighter1["UFC-experience-score"] = fighter1.total_fights_in_UFC / fighter2.total_fights_in_UFC

    total_result_fighter1 = 0
    total_result_fighter2 = 0

    for key, metric_value in metrics.items():
        if result_fighter1[f"{key}-score"] != -1:
            total_result_fighter1 += result_fighter1[f"{key}-score"] * metric_value

        if result_fighter2[f"{key}-score"] != -1:
            total_result_fighter2 += result_fighter2[f"{key}-score"] * metric_value

    print(f"fighter1 score - {total_result_fighter1}")
    print(f"fighter2 score - {total_result_fighter2}")

    fighter1_ratio = total_result_fighter1 / (
        total_result_fighter1 + total_result_fighter2
    )
    fighter2_ratio = total_result_fighter2 / (
        total_result_fighter1 + total_result_fighter2
    )

    print(f"{fighter1_ratio} : {fighter2_ratio}")


def analyze_outcome():
    pass


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
            row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=20
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
        weight_class_input.grid(row=2, column=2, padx=20, pady=15)

        age_label = tk.Label(settings_window, text="Age: ")
        age_label.grid(row=3, column=0)

        age_current_label = tk.Label(settings_window, text=str(metrics["age"]))
        age_current_label.grid(row=3, column=1)

        age_input = tk.Entry(settings_window)
        age_input.grid(row=3, column=2, padx=20, pady=15)

        technics_label = tk.Label(settings_window, text="Technics: ")
        technics_label.grid(row=4, column=0)

        technics_current_label = tk.Label(
            settings_window, text=str(metrics["technics"])
        )
        technics_current_label.grid(row=4, column=1)

        technics_input = tk.Entry(settings_window)
        technics_input.grid(row=4, column=2, padx=20, pady=15)

        height_label = tk.Label(settings_window, text="Height: ")
        height_label.grid(row=5, column=0)

        height_current_label = tk.Label(settings_window, text=str(metrics["height"]))
        height_current_label.grid(row=5, column=1)

        height_input = tk.Entry(settings_window)
        height_input.grid(row=5, column=2, padx=20, pady=15)

        experience_label = tk.Label(settings_window, text="UFC Fight Experience: ")
        experience_label.grid(row=6, column=0)

        experience_current_label = tk.Label(
            settings_window, text=str(metrics["UFC-experience"])
        )
        experience_current_label.grid(row=6, column=1)

        experience_input = tk.Entry(settings_window)
        experience_input.grid(row=6, column=2, padx=20, pady=15)

        warning_label = tk.Label(settings_window, text="")
        warning_label.grid(row=7, column=0, columnspan=2, padx=20, pady=15)

        save_button = tk.Button(
            settings_window,
            text="Save",
            command=lambda: save_metrics(
                settings_window,
                weight_class_input,
                age_input,
                technics_input,
                height_input,
                experience_input,
                warning_label,
            ),
        )
        save_button.grid(row=8, column=0, pady=20)

        cancel_button = tk.Button(
            settings_window,
            text="Cancel",
            command=lambda: on_settings_close(settings_window),
        )
        cancel_button.grid(row=8, column=1, pady=20)

        settings_open = True

        settings_window.protocol(
            "WM_DELETE_WINDOW", lambda: on_settings_close(settings_window)
        )
    else:
        print("Settings open already")


def save_metrics(window, w_entry, a_entry, t_entry, h_entry, e_entry, warning_label):
    global metrics

    try:
        metrics["weight-class"] = str_to_num(w_entry.get())
        metrics["age"] = str_to_num(a_entry.get())
        metrics["technics"] = str_to_num(t_entry.get())
        metrics["height"] = str_to_num(h_entry.get())
        metrics["UFC-experience"] = str_to_num(e_entry.get())

        on_settings_close(window)

    except ValueError:
        warning_label.config(text="Entered input is invalid", fg="red")


def on_settings_close(window):
    global settings_open
    settings_open = False

    window.destroy()
