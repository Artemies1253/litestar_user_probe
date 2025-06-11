import re


def is_ids_valid(ids: str) -> bool:
    return bool(re.search(r"^[0-9, ]*$", ids))
