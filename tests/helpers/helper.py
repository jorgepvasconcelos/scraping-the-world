
def response_is_not_empty(data_dict: dict) -> bool:
    for value in data_dict.values():
        if value is None:
            break
        return True
    return False