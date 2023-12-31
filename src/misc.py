def query_to_name(name: str):
    formatted_name = " ".join(name.lower().split("-"))
    return formatted_name.title()


def name_to_query(name: str):
    return "-".join(name.lower().split(" "))
