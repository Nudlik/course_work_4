import json
from pprint import pprint

import requests

from absclasses import AbstractClassAPI


class HeadHunterAPI(AbstractClassAPI):

    url = r'https://api.hh.ru/vacancies/'
    path_to_json = r'../data/hh_vacancy.json'

    def __init__(self, find_text):
        self.find_text = find_text
        self.USD_RATE = 60  # возможно надо дергать с другой апишки

    def get_vacancies(self):

        query_parameters = {
            'text': self.find_text,
            'per_page': 10,
            'page': 0
        }

        response = requests.get(self.url, params=query_parameters)
        return response.json()

    def save_data(self):
        data = self.get_vacancies()
        with open(self.path_to_json, 'w', encoding='utf-8') as file:
            lst = []
            for vacancy in data['items']:

                salary = vacancy['salary']
                if isinstance(salary, dict):
                    currency = salary['currency']
                    from_ = salary['from']
                    if currency == 'USD':
                        salary = from_ * self.USD_RATE
                    elif from_ is None:
                        salary = 0
                    else:
                        salary = from_
                else:
                    salary = 0

                lst.append({
                    'name': vacancy['name'],
                    'url': vacancy['alternate_url'],
                    'salary': salary,
                    'experience': vacancy['experience']['name'],
                    'requirements': vacancy['snippet']['responsibility'],
                    'city': vacancy['area']['name']
                })

            json.dump(lst, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    hh = HeadHunterAPI('python')
    pprint(hh.get_vacancies())
    hh.save_data()
