import xml.etree.ElementTree as Et
import requests
from datetime import datetime as dt
from datetime import timedelta
from bs4 import BeautifulSoup
from typing import Literal, Union

currency_url = "http://www.cbr.ru/scripts/XML_daily.asp"
dt = dt.now()
metals_url = (
    f'https://www.cbr.ru/scripts/xml_metall.asp?date_req1={dt.strftime("%d/%m/%Y")}'
    f'&date_req2={dt.strftime("%d/%m/%Y")}'
)


# документация не очень у цб рф(нашел только примеры запросов),
# поэтому пришлось немного помудрить с datetime при запросе цен на золото


def get_currency_price(wanted_currency: Literal["USD", "EUR"]) -> Union[None, str]:
    """Функция для получения курса евро и доллара в строковом формате"""
    for currency in get_root_xml(currency_url).findall("Valute"):
        char_code = currency.find("CharCode").text
        value = currency.find("Value").text.replace(",", ".")
        if char_code == wanted_currency:
            return f"{char_code} {round(float(value), 2)} RUB"


def get_not_empty_page(url, current_date):
    """
    Функция для проверки url: если на странице нет видимой информации,
    проверяется ссылка с предыдущей датой до тех пор, пока в ссылке не найдется
    хоть один символ видимого текста
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    visible_text = soup.get_text(strip=True)
    length = len(visible_text)
    if length != 0:
        return url
    else:
        previous_date = current_date - timedelta(days=1)
        new_metals_url = (f'https://www.cbr.ru/scripts/xml_metall.asp?date_req1={previous_date.strftime("%d/%m/%Y")}'
                          f'&date_req2={previous_date.strftime("%d/%m/%Y")}')

        return get_not_empty_page(new_metals_url, previous_date)


def get_root_xml(url) -> Et.Element:
    """Функция для получения информации из xml elementTree"""
    response = requests.get(get_not_empty_page(url, dt))
    if response.status_code == 200:
        tree = Et.ElementTree(Et.fromstring(response.content))
        root = tree.getroot()
        return root


def get_gold_price() -> Union[None, str]:
    """Функция для получения цены на золото в строковом формате"""
    for record in get_root_xml(metals_url).findall("Record"):
        value = record.find("Buy").text.replace(",", ".")
        result = f"{round(float(value), 2)} RUB"
        return result
