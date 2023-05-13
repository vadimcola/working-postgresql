import json

import requests as requests


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

