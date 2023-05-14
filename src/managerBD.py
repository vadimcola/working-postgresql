import psycopg2


class DBManager:
    """в классе реализованы методы с SQL запросами"""

    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.database_name, **params)

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""

        with self.conn.cursor() as cur:
            cur.execute('SELECT name, open_vacancies FROM employers')
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""

        with self.conn.cursor() as cur:
            cur.execute('SELECT name_employer, name_vacancy, salary_from, salary_to, url_vacancy '
                        'FROM vacancies')
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute('SELECT (AVG(salary_from)+AVG(salary_to))/2 AS salary_avg FROM vacancies')
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_vacancies_with_higher_salary(self):
        with self.conn.cursor() as cur:
            """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

            cur.execute('SELECT name_vacancy FROM vacancies '
                        'WHERE vacancies.salary_from > (SELECT (AVG(salary_from)+AVG(salary_to))/2 FROM vacancies)'
                        'OR vacancies.salary_to > (SELECT (AVG(salary_from)+AVG(salary_to))/2 FROM vacancies)')
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""

        with self.conn.cursor() as cur:
            cur.execute(f"SELECT name_vacancy "
                        f"FROM vacancies "
                        f"WHERE vacancies.name_vacancy LIKE '%{keyword}%'")
            rows = cur.fetchall()
            for row in rows:
                print(row)
