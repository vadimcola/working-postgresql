from config import config
from src.managerBD import DBManager
from src.utils import create_database, save_data_to_database_emp, getting_json_employer, getting_json_vacancies, \
    save_data_to_database_vac


def main():
    params = config()
    select_employer = input("Введите работодателя для получения данных ...   ")
    getting_json_employer(select_employer)
    getting_json_vacancies(select_employer)
    print("Идет загрузка в базу данных")
    create_database('hh', params)
    save_data_to_database_emp('hh', params)
    save_data_to_database_vac('hh', params)
    print("Данные загружены !!!!")
    while True:
        get = DBManager('hh', params)
        answer = input(f"Теперь вам доступны следующие команды для отображения информации:\n"
                       f"1: Получить список всех компаний и количество вакансий у каждой компании\n"
                       f"2: Получить список всех вакансий с указанием названия компании,"
                       f"названия вакансии, зарплаты и ссылки на вакансию\n"
                       f"3: Получить среднюю зарплату по вакансиям\n"
                       f"4: Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
                       f"5: Получить список всех вакансий по ключевому слову \n"
                       f"6: Выход из программы \n"
                       f"   Введите цифру команды ...   ")

        if answer not in ('1', '2', '3', '4', '5', '6'):
            print("!!!! Ошибка ввода !!!!")
            continue
        elif answer == '1':
            get.get_companies_and_vacancies_count()
        elif answer == '2':
            get.get_all_vacancies()
        elif answer == '3':
            get.get_avg_salary()
        elif answer == '4':
            get.get_vacancies_with_higher_salary()
        elif answer == '5':
            keyword = input('Введите ключевое слово ...')
            get.get_vacancies_with_keyword(keyword)
        elif answer == "6":
            print("Спасибо !!!!")
            break


if __name__ == "__main__":
    main()
