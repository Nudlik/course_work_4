import json
import os
from pprint import pprint

import requests

from absclasses import AbstractClassAPI


class SuperJobAPI(AbstractClassAPI):

    url = 'https://api.superjob.ru/2.0/vacancies/'
    API_KEY = os.getenv('SUPERJOB_API_KEY')
    path_to_json = '../data/sj_vacancy.json'

    def __init__(self, keyword):
        self.keyword = keyword

    def get_vacancies(self):

        query_parameters = {
            'keyword': self.keyword
        }

        headers = {
            'X-Api-App-Id': self.API_KEY
        }

        response = requests.get(self.url, params=query_parameters, headers=headers)
        return response.json()

    def save_data(self):
        data = self.get_vacancies()
        with open(self.path_to_json, 'w', encoding='utf-8') as file:
            lst = []
            for vacancy in data['objects']:

                requirements = vacancy['candidat'][:100] + '...'

                lst.append({
                    'name': vacancy['profession'],
                    'url': vacancy['link'],
                    'salary': vacancy['payment_from'],
                    'experience': vacancy['experience']['title'],
                    'requirements': requirements,
                    'city': vacancy['town']['title']
                })

            json.dump(lst, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    sj = SuperJobAPI('python')
    pprint(sj.get_vacancies())
    sj.save_data()