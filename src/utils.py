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
    with open('src/employer.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print("Данные выгружены!!!")


def getting_json_vacancies(keyword):
    data = getting_vacancies(employer_id(keyword))
    with open('src/vacancies.json', 'w', encoding='utf-8') as file:
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
                    name_employer VARCHAR(255) NOT NULL,
                    name_vacancy VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    url_vacancy TEXT
                )
            """)

    conn.commit()
    conn.close()

def save_data_to_database_emp(database_name: str, params: dict):
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        with open('src/employer.json', 'r', encoding='utf-8') as file:
            employer = json.load(file)
            for emp in employer:
                name = emp['name']
                url_employer = emp['alternate_url']
                open_vacancies = emp['open_vacancies']
                cur.execute(
                    """
                    INSERT INTO employers (name, url_employer, open_vacancies)
                    VALUES (%s, %s, %s)
                    """,
                    (name, url_employer, open_vacancies)
                )

    conn.commit()
    conn.close()


def save_data_to_database_vac(database_name: str, params: dict):
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        with open('src/vacancies.json', 'r', encoding='utf-8') as file:
            vacancies = json.load(file)
            for vac in vacancies:
                name_employer = vac['employer']['name']
                name_vacancy = vac['name']
                if vac['salary'] is None:
                    salary_from = 0
                    salary_to = 0
                else:
                    salary_from = vac['salary']['from']
                    if salary_from is None:
                        salary_from = 0
                    else:
                        salary_from
                    salary_to = vac['salary']['to']
                    if salary_to is None:
                        salary_to = 0
                    else:
                        salary_to
                url_vacancy = vac['alternate_url']
                cur.execute(
                    """
                    INSERT INTO vacancies (name_employer, name_vacancy, salary_from, salary_to,
                    url_vacancy)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (name_employer, name_vacancy, salary_from, salary_to,
                    url_vacancy)
                )

    conn.commit()
    conn.close()