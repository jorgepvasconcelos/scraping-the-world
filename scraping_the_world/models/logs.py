import traceback

from scraping_the_world.models.utils import DataBase


def add_log(text: str, tipe: str):
    try:
        DataBase.execute(query="INSERT INTO logs (text, tipe) VALUE (%s, %s)", arguments=[text, tipe])
    except:
        traceback.print_exc()
