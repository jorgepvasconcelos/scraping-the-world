import traceback

from scraping_the_world.models.utils import DataBase


def add_log(text: str, tipe: str) -> None:
    try:
        DataBase.execute(query="INSERT INTO logs (text, tipe) VALUE (%s, %s)", arguments=[text, tipe])
    except:
        traceback.print_exc()


def get_config(name: str):
    value = DataBase.consult_one(query="select value from configs where name = %s; ", arguments=[name])
    value = value['value']
    return value
