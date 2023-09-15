import requests

from models.absclasses import AbstractClassAPI
from settings import API_KEY_SUPERJOB


class SuperJobAPI(AbstractClassAPI):

    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': API_KEY_SUPERJOB}

    def get_vacancies(self, find_text, pages=1):
        res = []
        for page in range(pages):

            query_parameters = {
                'keyword': find_text,
                'count': 10,
                'page': page
            }

            response = requests.get(self.url, params=query_parameters, headers=self.headers)
            res.extend(response.json()['objects'])

        return res

    def __str__(self):
        return 'https://www.superjob.ru/'
