from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.json_api import get_btc_price
from api.xml_api import get_gold_price, get_currency_price
import re


def is_valid_time_format(time_str):
    """Проверка правильности ввода времени"""
    pattern = r'^(?:[01][0-9]|2[0-3]):[0-5][0-9]$'
    return re.match(pattern, time_str) is not None


def create_keyboard():
    """функция помогает создать клавиатуру с кнопками для хендлера старт и хелп"""
    print_stock_btn = InlineKeyboardButton(
        text='💱 Узнать текущий курс', callback_data='print_stock_cb')
    set_notifications_btn = InlineKeyboardButton(
        text='⏰ Назначить время оповещения о курсе',
        callback_data='set_notifications_cb')
    row_one = [print_stock_btn]
    row_two = [set_notifications_btn]
    rows = [row_one, row_two]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def generate_stock_text():
    """Генерирует текст курса"""
    return (
        f"Грамм золота: {get_gold_price()}\n"
        f"{get_currency_price('USD')}\n"
        f"{get_currency_price('EUR')}\n"
        f"BTC {get_btc_price()} USD")
