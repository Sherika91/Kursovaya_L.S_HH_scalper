class DBManager:

    @staticmethod
    def get_all_vacancies(cur):
        """Returns a list of all vacancies."""
        script = """SELECT name, salary_min, salary_max, city, companies.company_name FROM vacancies
        JOIN companies ON companies.company_id = vacancies.company_id"""

        cur.execute(script)
        result = cur.fetchall()
        return result

    @staticmethod
    def get_companies_and_vacancies_count(cur):
        """Returns a list of companies and the number of vacancies in each of them."""
        script = """SELECT company_name, COUNT(*) FROM companies
        JOIN vacancies ON companies.company_id = vacancies.company_id
        GROUP BY company_name"""

        cur.execute(script)
        result = cur.fetchall()
        return result

    @staticmethod
    def get_avg_salary_by_company(cur):
        """Returns a list of companies and average salary for each of them."""
        query = """
                SELECT AVG((salary_min + salary_max) / 2)
                FROM vacancies"""
        cur.execute(query)
        result = cur.fetchall()
        return result

    @staticmethod
    def get_vacancies_with_higher_salary_than_avg(cur):
        """Returns a list of vacancies with salary higher than avg."""
        script = """SELECT name, salary_min, salary_max, companies.company_name FROM vacancies
                    LEFT JOIN companies ON vacancies.company_id = companies.company_id
                    WHERE salary_max > (SELECT AVG((salary_min + salary_max) / 2) FROM vacancies)"""

        cur.execute(script)
        result = cur.fetchall()
        return result

    @staticmethod
    def get_vacancies_with_keyword(cur, keyword):
        """Returns a list of vacancies with specified keyword in description."""
        script = f"""SELECT name, salary_min, salary_max, companies.company_name FROM vacancies
        JOIN companies ON vacancies.company_id = companies.company_id
        WHERE name LIKE '%{keyword}%'"""

        cur.execute(script)
        result = cur.fetchall()
        return result
