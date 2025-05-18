import re


def is_ids_valid(ids: str):
    return re.search(r'^[0-9, ]*$', ids)