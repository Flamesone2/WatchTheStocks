from aiogram import F, Router, types
from aiogram.types import CallbackQuery
from handlers_and_keyboards.utils import generate_stock_text
from aiogram.fsm.context import FSMContext
from .states_for_notifications_cb import SetNotifications
from .utils import is_valid_time_format
from database_pkg.database_file import add_user_timezone_preferences, add_msg_to_history
from datetime import datetime as dt

from scheduler import scheduler_sender

router = Router()


@router.callback_query(F.data == 'print_stock_cb')
async def print_stock_cb(callback_query: CallbackQuery):
    """Кнопка для команды /printstock"""
    text = generate_stock_text()
    await callback_query.message.answer(text=text, parse_mode='HTML')
    add_msg_to_history(user_id=callback_query.from_user.id,
                       date_n_time=dt.now().strftime('%Y-%m-%d %H:%M'),
                       msg=text)


@router.callback_query(F.data == 'set_notifications_cb')
async def set_notifications_cb(callback_query: CallbackQuery, state: FSMContext):
    """Кнопка для команды /set_notifications"""
    await state.set_state(SetNotifications.time_zone)

    text = ('Введите пожалуйста свой часовой пояс в формате UTC +-n\n'
            '(Москва: +3\n'
            'Лос-Анджелес: -7')
    await callback_query.message.answer(text=text)


@router.message(SetNotifications.time_zone)
async def typing_time_zone(message: types.Message, state: FSMContext):
    """Одна из функций кнопки установки времени отправки курса.
    Отвечает за ввод часового пояса, сохраняет эти данные в состояния states"""

    try:
        number = message.text

        if number.startswith('+') or number.startswith('-') or number.startswith('0'):
            await state.update_data(time_zone=number)
            await state.set_state(SetNotifications.time_preferences)
            await message.answer(f"Ваш часовой пояс: {number} UTC\n"
                                 f"Введите время в формате 00:00 в которое хотели бы получать обновления курса")

            await state.update_data(user_id=message.from_user.id, timezone=number)
        else:
            raise ValueError('Значение часового пояса должно начинаться с "+", "-" или быть нулевым.')

    except ValueError as VE:
        await message.answer(f'{VE}')
        await message.answer("Пожалуйста, введите корректное значение!")


@router.message(SetNotifications.time_preferences)
async def typing_time_preferences(message: types.Message, state: FSMContext):
    """Одна из функций кнопки установки времени отправки курса.
    Отвечает за ввод предпочтительного времени отправки курса, заносит информацию
    в бд с помощью add_user_timezone_preferences и запускает функцию отправки
    курса ко времени"""
    try:
        time = message.text
        if is_valid_time_format(time):
            await message.answer(f'Ежедневное время отправки курса установлено на {time}.')
            data = await state.get_data()  # занесение информации в базу данных
            user_id = data.get('user_id')
            timezone = data.get('timezone')
            add_user_timezone_preferences(user_id=user_id, timezone=timezone, preferred_time=str(time))
            await scheduler_sender(id_in_tg=message.from_user.id, chat_id=message.chat.id)

            await state.clear()
        else:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите корректное значение.")
