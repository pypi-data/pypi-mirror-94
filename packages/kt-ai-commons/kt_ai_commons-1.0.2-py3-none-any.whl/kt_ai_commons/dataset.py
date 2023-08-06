import psycopg2
import pandas.io.sql as sqlio
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    return secrets[setting]


def onenavi_train():
    conn = psycopg2.connect(host=get_secret("ip_address"),
                            dbname=get_secret("db_name"),
                            user=get_secret("user"),
                            password=get_secret("PASSWORD"),
                            port=get_secret("port"))

    sql = """
        SELECT *
        FROM onenavi_train
        ;
        """
    print("onenavi_train 데이터 불러오기가 완료되었습니다.")
    return sqlio.read_sql_query(sql, conn)


def onenavi_evaluation():
    conn = psycopg2.connect(host=get_secret("ip_address"),
                            dbname=get_secret("db_name"),
                            user=get_secret("user"),
                            password=get_secret("PASSWORD"),
                            port=get_secret("port"))

    sql = """
        SELECT *
        FROM onenavi_evaluation
        ;
        """
    print("onenavi_evaluation 데이터 불러오기가 완료되었습니다.")
    return sqlio.read_sql_query(sql, conn)


def onenavi_pnu():
    conn = psycopg2.connect(host=get_secret("ip_address"),
                            dbname=get_secret("db_name"),
                            user=get_secret("user"),
                            password=get_secret("PASSWORD"),
                            port=get_secret("port"))

    sql = """
        SELECT *
        FROM onenavi_pnu
        ;
        """
    print("onenavi_pnu 데이터 불러오기가 완료되었습니다.")
    return sqlio.read_sql_query(sql, conn)


def onenavi_signal():
    conn = psycopg2.connect(host=get_secret("ip_address"),
                            dbname=get_secret("db_name"),
                            user=get_secret("user"),
                            password=get_secret("PASSWORD"),
                            port=get_secret("port"))

    sql = """
        SELECT *
        FROM onenavi_signal
        ;
        """
    print("onenavi_signal 데이터 불러오기가 완료되었습니다.")
    return sqlio.read_sql_query(sql, conn)


def onenavi_weather():
    conn = psycopg2.connect(host=get_secret("ip_address"),
                            dbname=get_secret("db_name"),
                            user=get_secret("user"),
                            password=get_secret("PASSWORD"),
                            port=get_secret("port"))

    sql = """
        SELECT *
        FROM onenavi_weather
        ;
        """
    print("onenavi_weather 데이터 불러오기가 완료되었습니다.")
    return sqlio.read_sql_query(sql, conn)
