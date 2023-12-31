def query_to_name(name: str):
    return " ".join(name.split("-"))


def name_to_query(name: str):
    return "-".join(name.split(" "))
