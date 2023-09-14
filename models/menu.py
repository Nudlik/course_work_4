from models.absclasses import AbstractClassMenu


class Menu(AbstractClassMenu):

    def show_menu(self):
        print('Выберите пункт меню:\n'
              '1) Задать параметры для парсинга\n'
              '2) Запустить парсинг\n'
              '3) Посмотреть результат\n'
              '4) Сохранить в файл\n'
              '5) Отсортировать по ЗП\n'
              '6) Выход')

        user_input = int(input())

        match user_input:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
                pass
            case _:
                pass

    def parse_params(self):
        pass

    def start_parse(self):
        pass

    def show_result(self):
        pass

    def save_result(self):
        pass

    def sort_result_by_salary(self):
        pass

    def exit(self):
        pass
