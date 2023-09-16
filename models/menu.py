from models.absclasses import AbstractClassMenu
from models.headhunter import HeadHunterAPI
from models.jsonsaver import JsonSaver
from models.superjob import SuperJobAPI


class Menu(AbstractClassMenu):
    """ Меню программы """

    list_platforms: list = [
        HeadHunterAPI,
        SuperJobAPI
    ]

    json_saver: JsonSaver = JsonSaver()

    def __init__(self):
        self.user_find_text: str = 'python'
        self.salary: int = 0
        self.city: str = self.validate_input_city('красноярск')
        self.experience: int = 0
        self.count_pages: int = 1

    def show_menu(self):
        print('\nВыберите пункт меню:\n'
              '1) Задать параметры для парсинга\n'
              '2) Сменить платформу по которой будем парсить\n'
              '3) Запустить парсинг\n'
              '4) Посмотреть результат\n'
              '5) Сохранить json в файл\n'
              '6) Инфо\n'
              '7) Выход')

        user_input = self.validate_input_int(input())

        match user_input:
            case 1:
                self.set_parse_params()
            case 2:
                self.change_platform()
                self.start_parse()
            case 3:
                self.start_parse()
            case 4:
                self.show_result()
                self.show_menu()
            case 5:
                self.save_result()
                self.show_menu()
            case 6:
                print('\nИнфо - пока пусто')
                self.show_menu()
            case 7:
                self.exit()
            case _:
                self.menu_item_missing()
                self.show_menu()

    def set_parse_params(self):
        print(f'\nВыберите пункт меню:\n'
              f'1) Задать название вакансии\n'
              f'2) Задать минимальную ЗП\n'
              f'3) Задать город\n'
              f'4) Задать опыт работы\n'
              f'5) Задать количество страниц для парсинга (на 1ой странице будет 10 вакансий)\n'
              f'6) Начать парсинг\n'
              f'7) Выход в главное меню')

        user_input = self.validate_input_int(input())

        match user_input:
            case 1:
                self.user_find_text = input(
                    'Введите название вакансии(слово по которому будет искать вакансии): ').strip()
            case 2:
                self.salary = self.validate_input_int(input('Введите минимальную ЗП(цифру): '))
            case 3:
                self.city = self.validate_input_city(
                    input('Введите название города(чувствителен к регистру пишите город правильно): ').strip()
                )
            case 4:
                self.experience = self.validate_input_int(input('Введите опыт работы в годах(цифру): '))
            case 5:
                self.count_pages = self.validate_input_int(input(
                    'Введите количество страниц(на 1ой странице будет 10 вакансий): '))
            case 6:
                self.start_parse()
            case 7:
                self.show_menu()
            case _:
                self.menu_item_missing()
                self.set_parse_params()

        self.set_parse_params()

    def change_platform(self):
        print(f'\nСейчас выбраны все платформы')
        [print(f'{num}) {self.list_platforms[num - 1].__name__}') for num in range(1, len(self.list_platforms) + 1)]
        print('7) Выход в главное меню')

        user_input = self.validate_input_int(
            input('Введите цифру платформы которая будет использоваться для парсинга: '))

        match user_input:
            case 1:
                self.list_platforms = [HeadHunterAPI]
            case 2:
                self.list_platforms = [SuperJobAPI]
            case 7:
                self.show_menu()
            case _:
                self.menu_item_missing()
                self.change_platform()

    def start_parse(self):
        str_list_platforms = ', '.join(str(i).split('.')[-1][:-2] for i in self.list_platforms)

        print(f'\nПарсинг будет выполняться через: {str_list_platforms}\n'
              f'Парсинг вакансий по слову:       {self.user_find_text}\n'
              f'ЗП ищется от:                    {self.salary} руб/usd\n'
              f'Город ищется:                    {self.city}\n'
              f'Опыт работы ищется от:           {self.experience} года(лет)\n'
              f'Страниц будет загружено:         {self.count_pages} шт\n'
              f'Вакансий будет найдено:          {self.count_pages * 10 * len(self.list_platforms)} шт\n'
              f'1) Начать парсинг\n'
              f'6) Задать параметры для парсинга\n'
              f'7) Выход в главное меню')

        user_input = self.validate_input_int(input())

        match user_input:
            case 1:
                print('\nПарсинг начался, пожалуйста подождите (っ◕‿◕)っ\n')
                print('Возможные ошибки:', end=' ')
                try:
                    self.start_parse_by_vacancies()
                except Exception as e:
                    print(e)
                else:
                    print('повезло :)\n')
                    print('Все прошло успешно, взаимодействуйте дальше с меню\n')
            case 6:
                self.set_parse_params()
            case 7:
                self.show_menu()
            case _:
                self.menu_item_missing()
                self.start_parse()

        self.show_menu()

    def show_result(self):
        print('\nРезультат будет отображен в консоль выберите пункт меню:\n'
              '1) Показать все результаты\n'
              '2) Показать сортировку по ЗП\n'
              '7) Выход в главное меню')

        user_input = self.validate_input_int(input())

        match user_input:
            case 1:
                vacancy = self.json_saver.get_data_vacancy()
                data = self.json_saver.get_data_to_vacancy(vacancy)
            case 2:
                vacancy = self.json_saver.sorted_by_salary()
                data = self.json_saver.get_data_to_vacancy(vacancy)
            case 7:
                self.show_menu()
            case _:
                self.menu_item_missing()
                self.show_result()

        print(*data, sep='\n\n', end='\n\n')

    def save_result(self):
        self.json_saver.save_data_to_json()

    @staticmethod
    def exit():
        JsonSaver.clear_cash()
        quit()

    @staticmethod
    def menu_item_missing():
        print('\nПункт меню отсутствует\n')

    @classmethod
    def validate_input_int(cls, user_input: str) -> int:
        """ Валидация введенного пользователем числа """

        try:
            user_input = int(user_input.strip())
            return user_input
        except ValueError:
            user_input = input('Неверный ввод, попробуйте еще раз ввести цифру: ')
            return cls.validate_input_int(user_input)

    @staticmethod
    def validate_input_city(user_input: str) -> str:
        """ Валидация введенного пользователем города """

        if '-' in user_input:
            correct_city = user_input.split('-')
            return '-'.join(map(str.capitalize, correct_city))

        elif ' ' in user_input:
            correct_city = user_input.split()
            return ' '.join(map(str.capitalize, correct_city))

        return user_input.capitalize()

    def start_parse_by_vacancies(self):

        options = {
            'text': self.user_find_text,
            'salary': self.salary,
            'city': self.city,
            'experience': self.experience,
            'pages': self.count_pages
        }

        for platform in self.list_platforms:
            platform = platform()
            data = platform.get_vacancies(options)
            self.json_saver.rotate(platform, data)
