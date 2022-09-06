import re


def split_producer_names(text: str):
    text = text.replace(" and ", ", ")
    text = text.replace(",,", ",")
    return re.split(" and |, ", text)
