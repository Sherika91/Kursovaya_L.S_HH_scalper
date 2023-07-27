import psycopg2
from config import config


class DBManager:
    def __init__(self, salary_range, keyword):
        self.params = config()
        self.salary_range = salary_range
        self.keyword = keyword

        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                self.get_all_vacancies(cur)
                self.get_companies_and_vacancies_count(cur)
                self.get_avg_salary_by_company(cur)
                self.get_vacancies_with_higher_salary(cur, self.salary_range)
                self.get_vacancies_with_keyword(cur, self.keyword)

    # 1. - Returns a list of all vacancies.
    @staticmethod
    def get_all_vacancies(cur):
        """Returns a list of all vacancies."""
        script = """SELECT vacancy_id, name, salary_min, salary_max, salary_currency FROM vacancies
        LEFT JOIN companies ON companies.company_id_hh = vacancies.vacancy_id"""

        cur.execute(script)
        return print(cur.fetchall())

    # 2. - Returns a list of companies and the number of vacancies in each of them.
    @staticmethod
    def get_companies_and_vacancies_count(cur):
        """Returns a list of companies and the number of vacancies in each of them."""
        script = """SELECT company_name, COUNT(vacancy_id) FROM companies
        LEFT JOIN vacancies ON companies.company_id = vacancies.vacancy_id
        GROUP BY company_name"""

        cur.execute(script)
        result = cur.fetchall()
        return print(result)

    # 3. - Returns a list of companies and average salary for each of them.
    @staticmethod
    def get_avg_salary_by_company(cur):
        """Returns a list of companies and average salary for each of them."""
        query = """
                SELECT name, AVG((v.salary_min + v.salary_max) / 2)
                FROM companies 
                JOIN vacancies v
                ON companies.company_id_hh = companies.company_id
                GROUP BY name
            """
        cur.execute(query)
        result = cur.fetchall()
        return print(result)

    # 4. - Returns a list of vacancies with salary higher than specified.
    def get_vacancies_with_higher_salary(self, salary_range):
        """Returns a list of vacancies with salary higher than specified."""
        script = """SELECT vacancy_id, name, salary_max, company_name FROM vacancies
                    LEFT JOIN companies ON vacancies.vacancy_id = companies.company_id
                    WHERE salary_max > %s"""

        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(script, (salary_range,))
                result = cur.fetchall()
                return print(result)

    # 5. - Returns a list of vacancies with specified keyword
    def get_vacancies_with_keyword(self, keyword):
        """Returns a list of vacancies with specified keyword in description."""
        script = """SELECT vacancy_id, vacancy_name, salary, company_name FROM vacancies
        LEFT JOIN companies ON vacancies.company_id = companies.company_id
        WHERE description LIKE %s"""

        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(script, (keyword,))
                result = cur.fetchall()
                print(result)
