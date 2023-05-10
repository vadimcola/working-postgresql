import json

import requests as requests

params = {'text': None,
          'per_page': 100,
          'only_with_vacancies': True
          }

response_url = requests.get('https://api.hh.ru/employers', params=params)
response_data = json.loads(response_url.text)
vacancies = response_data['items']
for i in vacancies:
    print(i)
