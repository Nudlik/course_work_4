from models.absclasses import AbstractClassMenu
from models.headhunter import HeadHunterAPI
from models.jsonsaver import JsonSaver
from models.superjob import SuperJobAPI


class Menu(AbstractClassMenu):

    def __init__(self):
        self.user_find_text: str = 'python'
        self.count_pages: int = 1
        self.list_platforms: list = [HeadHunterAPI, SuperJobAPI]
        self.json_saver: JsonSaver = JsonSaver()

    def show_menu(self):
        print('Выберите пункт меню:\n'
              '1) Задать параметры для парсинга\n'
              '2) Сменить платформу по которой будем парсить\n'
              '3) Запустить парсинг\n'
              '4) Посмотреть результат\n'
              '5) Сохранить в файл\n'
              '6) Отсортировать по ЗП\n'
              '7) Выход')

        user_input = int(input())

        match user_input:
            case 1:
                self.set_parse_params()
            case 2:
                self.change_platform()
            case 3:
                self.start_parse()
            case 4:
                pass
            case 5:
                pass
            case 6:
                pass
            case 7:
                pass
            case _:
                pass

    def set_parse_params(self):
        user_find_text = input('Введите слово для поиска по которому будем искать вакансии: ').lower().strip()
        count_page = int(input('Введите количество страниц для парсинга(на 1ой странице будет 10 вакансий): ').strip())
        self.user_find_text = user_find_text
        self.count_pages = count_page

        self.show_menu()

    def change_platform(self):
        platforms = ', '.join(str(i.__name__) for i in self.list_platforms)
        print(f'Сейчас выбрана(ы) платформа(ы): {platforms}')
        user_input = int(input('Введите цифру платформы для парсинга: '))
        match user_input:
            case 1:
                self.list_platforms = [HeadHunterAPI]
            case 2:
                self.list_platforms = [SuperJobAPI]
            case _:
                pass

        self.show_menu()

    def start_parse(self):
        for platform in self.list_platforms:
            platform = platform()
            data = platform.get_vacancies(self.user_find_text, self.count_pages)
            self.json_saver.rotate(platform, data)

        self.show_menu()

    def show_result(self):
        pass

    def save_result(self):
        pass

    def sort_result_by_salary(self):
        pass

    def exit(self):
        pass


if __name__ == '__main__':
    menu = Menu()
    menu.show_menu()
