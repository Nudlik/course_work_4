from models.absclasses import AbstractClassMenu
from models.headhunter import HeadHunterAPI
from models.jsonsaver import JsonSaver
from models.superjob import SuperJobAPI
from models.vacancy import Vacancy


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
                self.show_menu()
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
                pass
            case 7:
                quit()
            case _:
                self.menu_item_missing()
                self.show_menu()

    def set_parse_params(self):
        user_find_text = input('Введите слово для поиска по которому будем искать вакансии: ').lower().strip()
        count_page = int(input('Введите количество страниц для парсинга(на 1ой странице будет 10 вакансий): ').strip())
        self.user_find_text = user_find_text
        self.count_pages = count_page


    def change_platform(self):
        print(f'Сейчас выбранаы платформы все платформы')
        [print(f'{num}) {self.list_platforms[num - 1].__name__}') for num in range(1, len(self.list_platforms) + 1)]
        print('7) Выход в главное меню')

        user_input = int(input('Введите цифру платформы которая будет использоваться для парсинга: '))

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
        print(f'Парсинг вакансий по слову: {self.user_find_text}\n'
              f'Страниц будет загружено {self.count_pages}\n'
              f'Вакансий будет найдено {self.count_pages * 10 * len(self.list_platforms)}\n'
              f'1) Начать парсинг\n'
              f'7) Выход в главное меню')

        user_input = int(input())

        match user_input:
            case 1:
                print('Парсинг начался, пожалуйста подождите')

                for platform in self.list_platforms:
                    platform = platform()
                    data = platform.get_vacancies(self.user_find_text, self.count_pages)
                    self.json_saver.rotate(platform, data)

                    self.show_menu()
            case 7:
                self.show_menu()
            case _:
                self.menu_item_missing()
                self.start_parse()

    def show_result(self):
        data_vacancy = self.json_saver.get_data_vacancy()
        for vacancy in data_vacancy:
            vacancy = Vacancy(name=vacancy['name'],
                              url=vacancy['url'],
                              salary=vacancy['salary'],
                              experience=vacancy['experience'],
                              requirements=vacancy['requirements'],
                              city=vacancy['city'])
            print(vacancy, end='\n\n')

    def save_result(self):
        self.json_saver.save_data_to_json()

    def sort_result_by_salary(self):
        pass

    def exit(self):
        pass

    @staticmethod
    def menu_item_missing():
        print('Пункт меню отсутствует')


if __name__ == '__main__':
    menu = Menu()
    menu.show_menu()
