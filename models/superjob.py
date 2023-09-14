import json
import os
from pprint import pprint

import requests

from models.absclasses import AbstractClassAPI


class SuperJobAPI(AbstractClassAPI):

    url = 'https://api.superjob.ru/2.0/vacancies/'
    API_KEY = os.getenv('SUPERJOB_API_KEY')
    path_to_json = os.path.join(os.path.dirname(__file__), '..', 'data', 'sj_vacancy.json')

    def __init__(self, keyword):
        self.keyword = keyword

    def get_vacancies(self, pages=0):

        query_parameters = {
            'keyword': self.keyword,
            'count': 10,
            'page': pages
        }

        headers = {
            'X-Api-App-Id': self.API_KEY
        }

        response = requests.get(self.url, params=query_parameters, headers=headers)
        return response.json()

    def save_data(self, pages=0):
        with open(self.path_to_json, 'a', encoding='utf-8') as file:
            lst = []
            for page in range(pages):
                data = self.get_vacancies(pages)
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

            self.clear_data()
            json.dump(lst, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    sj = SuperJobAPI('python')
    pprint(sj.get_vacancies())
    sj.save_data()