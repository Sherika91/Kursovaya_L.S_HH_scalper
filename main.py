from src.config import config
import psycopg2
from src.dbmanager import DBManager
from src.hh_api import HeadHunterAPI
from src.create_database import create_database,\
    create_companies_table,\
    create_vacancies_table,\
    insert_companies_data,\
    insert_vacancies_data

COMMANDS = """
1. - Returns a list of all vacancies.
2. - Returns a list of companies and the number of vacancies in each of them.
3. - Returns a list of companies and average salary for each of them.
4. - Returns a list of vacancies with specified keyword.
5. - Returns a list of vacancies with salary higher than specified.
0. - Exit the program
"""


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
                create_companies_table(cur)
                print("Table companies was created successfully")

                create_vacancies_table(cur)
                print("Table vacancies was created successfully")

                companies = HeadHunterAPI.get_companies()
                insert_companies_data(cur, companies)
                print("Data was inserted successfully in table companies")

                vacancies = HeadHunterAPI().get_vacancies()
                insert_vacancies_data(cur, vacancies)
                print("Data was inserted successfully in table vacancies")

                conn.commit()
                print("\nChoose command to continue.")

                while True:
                    command = input(f"{COMMANDS}\nEnter command: ")

                    if command == "1":
                        for i in DBManager.get_all_vacancies(cur):
                            print(f"Vacancy name - {i[0]}\n"
                                  f"Salary from: {i[1]} - Salary to: {i[2]}\n"
                                  f"City: {i[3]}, Company name - {i[4]}\n"
                                  f"{'-' * 100}")

                    elif command == "2":
                        for i in DBManager.get_companies_and_vacancies_count(cur):
                            print(f"Company Name - {i[0]}, Vacancy count:{i[1]}\n"
                                  f"{'-' * 60}")

                    elif command == "3":
                        for i in DBManager.get_avg_salary_by_company(cur):
                            print(f"Avg salary - {round(i[0])}\n"
                                  f"{'-' * 20}")

                    elif command == "4":
                        for i in DBManager.get_vacancies_with_higher_salary_than_avg(cur):
                            print(f"Vacancy name - {i[0]}\n"
                                  f"Salary from: {i[1]} --> Salary to: {i[2]}\n"
                                  f"Company name -- {i[3]}\n"
                                  f"{'-' * 100}")

                    elif command == "5":
                        for i in DBManager.get_vacancies_with_keyword(cur, input("Enter Search Query: ")):
                            print(f"Vacancy name - {i[0]}\n"
                                  f"Salary from: {i[1]} --> Salary to: {i[2]}\n"
                                  f"Company name -- {i[3]}\n"
                                  f"{'-' * 100}")

                    elif command == "0":
                        print("Goodbye!")
                        exit(0)
                    else:
                        print("Invalid command")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            cur.close()


if __name__ == '__main__':
    main()
