import threading

from ufc import get_fighter
from pprint import pprint
from fighter import Fighter


def get_fighter_info1():
    try:
        info1 = get_fighter("Jon Jones")
        fighter1 = Fighter(info1["name"], info1["height"], info1["losses"], info1["wins"], info1["strikes"], info1["takedowns"], info1["weight_class"])
        pprint(vars(fighter1))
    except BaseException as e:
        print("Fighter name is not valid")

def get_fighter_info2():
    try:
        info2 = get_fighter("Dohyun Moon")
        fighter2 = Fighter(info2["name"], info2["height"], info2["losses"], info2["wins"], info2["strikes"], info2["takedowns"], info2["weight_class"])
        pprint(vars(fighter2))
    except BaseException as e:
        print("Fighter name is not valid")

t1 = threading.Thread(target=get_fighter_info1)
t2 = threading.Thread(target=get_fighter_info2)


if __name__ == "__main__":
    t1.start()
    t2.start()

    t1.join()
    t2.join()