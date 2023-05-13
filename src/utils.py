import json
import psycopg2
import requests as requests

from config import config


def getting_employer(keyword: str):
    params = {'text': keyword,
              'per_page': 10,
              'only_with_vacancies': True
              }
    response_url = requests.get('https://api.hh.ru/employers', params=params)
    response_data = json.loads(response_url.text)
    employers = response_data['items']
    return employers


def employer_id(keyword):
    employer_list = []
    employers = getting_employer(keyword)
    for emp in employers:
        employer_list.append(emp['id'])
    return tuple(employer_list)


def getting_vacancies(index):
    params = {'employer_id': index,
              'per_page': 100,
              }
    response_url = requests.get('https://api.hh.ru/vacancies', params=params)
    response_data = json.loads(response_url.text)
    vacancies = response_data['items']
    return vacancies


def getting_json_employer(keyword):
    data = getting_employer(keyword)
    with open('employer.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print("Данные выгружены!!!")


def getting_json_vacancies(keyword):
    data = getting_vacancies(employer_id(keyword))
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print("Данные выгружены!!!")


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE employers (
                    id_employer SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    url_employer TEXT,
                    open_vacancies INTEGER
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE vacancies (
                    id_vacancy SERIAL PRIMARY KEY,
                    id_employer INT REFERENCES employers(id_employer),
                    name_employer VARCHAR(255) NOT NULL,
                    name_vacancy VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    url_vacancy TEXT
                )
            """)

    conn.commit()
    conn.close()

def save_data_to_database(data, database_name, params)
