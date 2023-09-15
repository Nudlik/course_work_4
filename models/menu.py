from models.absclasses import AbstractClassMenu
from models.headhunter import HeadHunterAPI
from models.jsonsaver import JsonSaver
from models.superjob import SuperJobAPI


class Menu(AbstractClassMenu):

    list_platforms: list = [
        HeadHunterAPI,
        SuperJobAPI
    ]

    json_saver: JsonSaver = JsonSaver()

    def __init__(self):
        self.user_find_text: str = 'python'
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
        user_find_text = input('Введите слово для поиска по которому будем искать вакансии: ').lower().strip()
        count_page = self.validate_input_int(input('Введите количество страниц для парсинга'
                                               '(на 1ой странице будет 10 вакансий): ').strip())
        self.user_find_text = user_find_text
        self.count_pages = count_page

        self.start_parse()

    def change_platform(self):
        print(f'\nСейчас выбраны все платформы')
        [print(f'{num}) {self.list_platforms[num - 1].__name__}') for num in range(1, len(self.list_platforms) + 1)]
        print('7) Выход в главное меню')

        user_input = self.validate_input_int(input('Введите цифру платформы которая будет использоваться для парсинга: '))

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
        print(f'\nПарсинг вакансий по слову: {self.user_find_text}\n'
              f'Страниц будет загружено {self.count_pages}\n'
              f'Вакансий будет найдено {self.count_pages * 10 * len(self.list_platforms)}\n'
              f'1) Начать парсинг\n'
              f'2) Задать параметры для парсинга\n'
              f'7) Выход в главное меню')

        user_input = self.validate_input_int(input())

        match user_input:
            case 1:
                print('\nПарсинг начался, пожалуйста подождите')

                for platform in self.list_platforms:
                    platform = platform()
                    data = platform.get_vacancies(self.user_find_text, self.count_pages)
                    self.json_saver.rotate(platform, data)

                    print('Все прошло успешно, взаимодействуйте дальше с меню\n')
                    self.show_menu()
            case 2:
                self.set_parse_params()
            case 7:
                self.show_menu()
            case _:
                self.menu_item_missing()
                self.start_parse()

    def show_result(self):
        print('\n1) Показать все результаты\n'
              '2) Показать сортировку по ЗП\n'
              '7) Выход в главное меню')

        user_input = self.validate_input_int(input())

        match user_input:
            case 1:
                data = self.json_saver.get_data_to_vacancy(self.json_saver.get_data_vacancy())
                print(*data, sep='\n\n', end='\n\n')
            case 2:
                data = self.json_saver.get_data_to_vacancy(self.json_saver.sorted_by_salary())
                print(*data, sep='\n\n', end='\n\n')
            case 7:
                self.show_menu()
            case _:
                self.menu_item_missing()
                self.show_result()

    def save_result(self):
        self.json_saver.save_data_to_json()

    @staticmethod
    def exit():
        quit()

    @staticmethod
    def menu_item_missing():
        print('\nПункт меню отсутствует\n')

    @classmethod
    def validate_input_int(cls, user_input):
        try:
            user_input = int(user_input)
            return user_input
        except Exception:
            user_input = input('Неверный ввод, попробуйте еще раз ввести цифру: ')
            return cls.validate_input_int(user_input)


if __name__ == '__main__':
    menu = Menu()
    menu.show_menu()
