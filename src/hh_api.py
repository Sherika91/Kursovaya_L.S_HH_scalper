from configparser import ParsingError
import requests
from abc import ABC, abstractmethod

COMPANIES = {"yandex": "1740",
             "teremok": "27879",
             "labirint": "17488",
             "abcp": "561525",
             "simplex": "1250899",
             "writers_way": "2175093",
             "tolyati": "9139449",
             "ozon": "2180",
             "fix_price": "196621",
             "start_job": "4811615"}


class AbstractAPi(ABC):
    """This is an abstract class for API"""

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(AbstractAPi):
    """This is a class for HeadHunter API"""

    def __init__(self):
        self.api_url = "https://api.hh.ru/vacancies?employer_id="
        self.params = {
            "pages": 0,
            "per_page": 100,
            "only_with_vacancies": True
        }

    def get_vacancies(self):
        vacancies = []

        for company in COMPANIES.values():
            response = requests.get(f"{self.api_url}{company}", params=self.params)
            print(f'{self.__class__.__name__} - Loading Page: {self.params["pages"]}')
            if response.status_code != 200:
                raise ParsingError(f"Error while trying to get Vacancies, Status: {response.status_code}")
            else:
                data = response.json()['items']
                vacancies.extend(data)
                self.params["pages"] += 1

        return vacancies

    @staticmethod
    def get_companies():
        companies = []
        for company in COMPANIES.values():
            response = requests.get(f"https://api.hh.ru/employers/{company}").json()
            companies.append(response)
        return companies
