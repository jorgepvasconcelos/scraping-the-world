import traceback

from scraping_the_world.models.utils import DataBase


def add_log(log_text: str, log_type: str) -> None:
    try:
        DataBase.execute(query="INSERT INTO logs (log_text, log_type) VALUE (%s, %s)", arguments=[log_text, log_type])
    except:
        traceback.print_exc()


def get_config(name: str):
    value = DataBase.consult_one(query="select value from configs where name = %s; ", arguments=[name])
    value = value['value']
    return value
