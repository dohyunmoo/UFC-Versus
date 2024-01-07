def query_to_name(name: str):
    formatted_name = " ".join(name.lower().split("-"))
    return formatted_name.title()


def name_to_query(name: str):
    return "-".join(name.lower().split(" "))


def str_to_num(input: str):
    try:
        return int(input)
    except:
        try:
            return float(input)
        except:
            if input == "":
                return "no change"
            raise ValueError


def height_to_num(height: str):
    # 1 foot == 12 inches
    height_list = height.split("'")
    height_inches = int(height_list[0]) * 12 + int(height_list[1][:-1])
    return height_inches


image_ratio = (300, 450)
