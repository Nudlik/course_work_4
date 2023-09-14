import json
import os
from pprint import pprint

import requests

from models.absclasses import AbstractClassAPI


class HeadHunterAPI(AbstractClassAPI):

    url = r'https://api.hh.ru/vacancies/'
    path_to_json = os.path.join(os.path.dirname(__file__), '..', 'data', 'hh_vacancy.json')

    def __init__(self, find_text):
        self.find_text = find_text
        self.USD_RATE = 60  # возможно надо дергать с другой апишки

    def get_vacancies(self, pages=0):

        query_parameters = {
            'text': self.find_text,
            'per_page': 10,
            'page': pages
        }

        response = requests.get(self.url, params=query_parameters)
        return response.json()

    def save_data(self, pages=0):
        with open(self.path_to_json, 'a', encoding='utf-8') as file:
            lst = []
            for page in range(pages):
                data = self.get_vacancies(pages)
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

            self.clear_data()
            json.dump(lst, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    hh = HeadHunterAPI('python')
    pprint(hh.get_vacancies())
    hh.save_data()
