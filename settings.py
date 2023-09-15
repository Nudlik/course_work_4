import os


# пути к файлам json(кэш и прочее)
path_to_root = os.path.dirname(__file__)
path_to_all_vacancy = os.path.join(path_to_root, 'data', 'all_vacancy.json')
path_to_hh_vacancy = os.path.join(path_to_root, 'data', 'hh_vacancy.json')
path_to_sj_vacancy = os.path.join(path_to_root, 'data', 'sj_vacancy.json')

# список путей к вайлам
LIST_TO_JSON = [
    path_to_hh_vacancy,
    path_to_sj_vacancy
]

# API ключи
API_KEY_SUPERJOB = os.getenv('SUPERJOB_API_KEY')
