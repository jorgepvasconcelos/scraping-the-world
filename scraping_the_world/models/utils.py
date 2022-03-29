from __future__ import annotations

from contextlib import contextmanager
from time import sleep
import traceback

import pymysql.cursors

from scraping_the_world.models.database_schema import SCHEMA_DDL
from env import ENV

@contextmanager
def conecta():
    conexao = pymysql.connect(
        host=ENV['DB_HOST'],
        user=ENV['DB_USER'],
        password=ENV['DB_PASSWORD'],
        port=int(ENV['DB_PORT']),
        db=ENV['DB_NAME'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        yield conexao
    finally:
        conexao.close()


class DataBase:
    @staticmethod
    def execute(query: str, arguments: list = None) -> None:
        with conecta() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, arguments)
                conexao.commit()

    @staticmethod
    def executemany(query: str, arguments: list[list] = None) -> None:
        with conecta() as conexao:
            with conexao.cursor() as cursor:
                cursor.executemany(query, arguments)
                conexao.commit()

    @staticmethod
    def consult_all(query: str, arguments: list = None) -> list | None:
        with conecta() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, arguments)
                result = cursor.fetchall()
                return result if result else None

    @staticmethod
    def consult_one(query: str, arguments: list = None) -> dict | None:
        with conecta() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query, arguments)
                result = cursor.fetchone()
                return result if result else None


def create_database():
    for _ in range(10):
        try:
            DataBase.execute(SCHEMA_DDL)
            break
        except:
            traceback.print_exc()
            sleep(2)


if __name__ == '__main__':
    ...