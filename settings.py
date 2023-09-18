import os


# пути к файлам(кэш и прочее)
path_to_root = os.path.dirname(__file__)
path_to_all_vacancy_json = os.path.join(path_to_root, 'saves', 'all_vacancy.json')
path_to_all_vacancy_csv = os.path.join(path_to_root, 'saves', 'all_vacancy.csv')
path_to_all_vacancy_txt = os.path.join(path_to_root, 'saves', 'all_vacancy.txt')

path_to_hh_vacancy = os.path.join(path_to_root, 'data', 'hh_vacancy.json')
path_to_sj_vacancy = os.path.join(path_to_root, 'data', 'sj_vacancy.json')


# список путей к вайлам
LIST_WITH_JSON_PATH = [
    path_to_hh_vacancy,
    path_to_sj_vacancy
]


# API ключи
API_KEY_SUPERJOB = os.getenv('SUPERJOB_API_KEY')
