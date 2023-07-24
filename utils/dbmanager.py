import psycopg2
from config import config


class DBManager:
    def __init__(self):
        self.params = config()

        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                self.get_companies_and_vacancies_count(cur)
                self.get_all_vacancies(cur)
                self.get_avg_salary_by_company(cur)
                self.get_vacancies_with_higher_salary(cur)
                self.get_vacancies_with_keyword(cur)

    @staticmethod
    def get_companies_and_vacancies_count(cur):
        """Returns a list of companies and the number of vacancies in each of them."""
        script = """SELECT company_name, COUNT(vacancy_id) FROM companies
        LEFT JOIN vacancies ON companies.company_id = vacancies.company_id
        GROUP BY company_name"""

        return cur.execute(script)

    @staticmethod
    def get_all_vacancies(cur):
        """Returns a list of all vacancies."""
        script = """SELECT vacancy_id, name, salary_min, salary_max, salary_currency FROM vacancies
        LEFT JOIN companies ON companies.company_id = vacancies.vacancy_id"""

        return print(cur.execute(script))

    @staticmethod
    def get_avg_salary_by_company(cur):
        """Returns a list of companies and average salary for each of them."""
        script = """SELECT company_name, AVG(salary) FROM companies
        LEFT JOIN vacancies ON companies.company_id = vacancies.company_id
        GROUP BY company_name"""

        return cur.execute(script)

    def get_vacancies_with_higher_salary(self, salary_range):
        """Returns a list of vacancies with salary higher than specified."""
        script = """SELECT vacancy_id, vacancy_name, salary, company_name FROM vacancies
        LEFT JOIN companies ON vacancies.company_id = companies.company_id
        WHERE salary > %s"""

        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                return cur.execute(script, (salary_range,))

    def get_vacancies_with_keyword(self, keyword):
        """Returns a list of vacancies with specified keyword in description."""
        script = """SELECT vacancy_id, vacancy_name, salary, company_name FROM vacancies
        LEFT JOIN companies ON vacancies.company_id = companies.company_id
        WHERE description LIKE %s"""

        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                return cur.execute(script, (keyword,))

