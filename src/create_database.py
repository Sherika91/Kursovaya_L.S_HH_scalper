import psycopg2


def create_database(params: dict, dbname: str) -> None:
    """Create new Data Base"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {dbname}")
    cur.execute(f"CREATE DATABASE {dbname}")

    cur.close()
    conn.close()


def create_vacancies_table(cur) -> None:
    """Creates the vacancies table."""
    cur.execute("CREATE TABLE IF NOT EXISTS vacancies ("
                "vacancy_id SERIAL PRIMARY KEY,"
                "name VARCHAR(100) NOT NULL,"
                "salary_min INT,"
                "salary_max INT,"
                "salary_currency VARCHAR(10),"
                "city VARCHAR(50) NOT NULL,"
                "company_id INT REFERENCES companies(company_id))")


def insert_vacancies_data(cur, vacancies: list[dict]) -> None:
    """Inserts data into the vacancies table."""
    for vacancy in vacancies:
        try:
            if vacancy['salary'] is None:
                cur.execute("INSERT INTO vacancies (name, salary_min, salary_max, salary_currency, city, company_id)"
                            "VALUES (%s, %s, %s, %s, %s, %s)",
                            (vacancy['name'], 0, 0, "null", vacancy['area']['name'], vacancy['employer']['id']))

            else:
                cur.execute("INSERT INTO vacancies (name, salary_min, salary_max, salary_currency, city, company_id)"
                            "VALUES (%s, %s, %s, %s, %s, %s)", (vacancy['name'],
                                                                vacancy['salary']['from'] if vacancy['salary'][
                                                                                             'from'] is not None else 0,
                                                                vacancy['salary']['to'] if vacancy['salary'][
                                                                                           'to'] is not None else 0,
                                                                vacancy['salary']['currency'] if vacancy['salary'][
                                                                                                 'currency'] is not None else "null",
                                                                vacancy['area']['name'], vacancy['employer']['id']))

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)


def create_companies_table(cur) -> None:
    """Creates the companies table."""
    cur.execute("CREATE TABLE IF NOT EXISTS companies ("
                "company_id INT PRIMARY KEY,"
                "company_name VARCHAR(100),"
                "company_url VARCHAR(200))")


def insert_companies_data(cur, companies: list[dict]) -> None:
    """Inserts data into the companies table."""
    for company in companies:
        cur.execute("INSERT INTO companies (company_id ,company_name, company_url) "
                    "VALUES (%s, %s, %s)", (company['id'], company['name'], company['alternate_url']))
