from config import config
import psycopg2
from dbmanager import DBManager
from hh_api import HeadHunterAPI


def main():
    dbname = 'vacancies'
    params = config()
    conn = None

    create_database(params, dbname)
    print(f"DB {dbname} was created successfully")

    params.update({'dbname': dbname})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:

                create_vacancies_table(cur)
                print("Table vacancies was created successfully")

                create_companies_table(cur)
                print("Table companies was created successfully")

                vacancies = HeadHunterAPI().get_vacancies()
                insert_vacancies_data(cur, vacancies)
                print("Data was inserted successfully in table vacancies")

                insert_companies_data(cur, vacancies)
                print("Data was inserted successfully in table companies")
                conn.commit()
                print("\nChose command to continue.\n"
                      "1. - Returns a list of all vacancies.\n"
                      "2. - Returns a list of companies and the number of vacancies in each of them.\n"
                      "3. - Returns a list of companies and average salary for each of them.\n"
                      "4. - Returns a list of vacancies with specified keyword\n"
                      "5. - Returns a list of vacancies with salary higher than specified.\n"
                      "0. - Exit the program\n")

                while True:
                    command = input("Enter command: ")
                    if command == "1":
                        DBManager.get_all_vacancies(cur)
                    elif command == "2":
                        DBManager.get_companies_and_vacancies_count(cur)
                    elif command == "3":
                        DBManager.get_avg_salary_by_company(cur)
                    elif command == "4":
                        DBManager.get_vacancies_with_higher_salary(cur, input("Enter salary: "))
                    elif command == "5":
                        DBManager.get_vacancies_with_keyword(cur, input("Enter Search Query: "))
                    elif command == "0":
                        exit(0)
                    else:
                        print("Invalid command")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            cur.close()


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
                "city VARCHAR(50) NOT NULL)")


def insert_vacancies_data(cur, vacancies: list[dict]) -> None:
    """Inserts data into the vacancies table."""
    for vacancy in vacancies:
        try:
            if vacancy['salary'] is None:
                cur.execute("INSERT INTO vacancies (name, salary_min, salary_max, salary_currency, city)"
                            "VALUES (%s, %s, %s, %s, %s)", (vacancy['name'], 0, 0, "null", vacancy['area']['name']))

            else:
                cur.execute("INSERT INTO vacancies (vacancy_id_hh, name, salary_min, salary_max, salary_currency, city)"
                            "VALUES (%s, %s, %s, %s, %s, %s)", (vacancy['id'],
                                                            vacancy['name'],
                                                            vacancy['salary']['from'] if vacancy['salary'][
                                                                                             'from'] is not None else 0,
                                                            vacancy['salary']['to'] if vacancy['salary'][
                                                                                           'to'] is not None else 0,
                                                            vacancy['salary']['currency'] if vacancy['salary'][
                                                                                                 'currency'] is not None else "null",
                                                            vacancy['area']['name']))

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)


def create_companies_table(cur) -> None:
    """Creates the companies table."""
    cur.execute("CREATE TABLE IF NOT EXISTS companies ("
                "company_id SERIAL PRIMARY KEY,"
                "company_id_hh INT,"
                "company_name VARCHAR(100),"
                "company_url VARCHAR(100),"
                "requirement TEXT,"
                "responsibility TEXT)")


def insert_companies_data(cur, vacancies: list[dict]) -> None:
    """Inserts data into the companies table."""
    for vacancy in vacancies:
        cur.execute("INSERT INTO companies (company_id_hh ,company_name, company_url, requirement, responsibility) "
                    "VALUES (%s, %s, %s, %s, %s)", (vacancy['employer']['id'], vacancy['employer']['name'],
                                                    vacancy['employer']['alternate_url'],
                                                    vacancy['snippet']['requirement'],
                                                    vacancy['snippet']['responsibility']))


if __name__ == '__main__':
    main()
