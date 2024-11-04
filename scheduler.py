from database_pkg.database_file import User, add_msg_to_history
from bot_config import bot, scheduler
from handlers_and_keyboards.utils import generate_stock_text
from datetime import datetime as dt
import logging


async def sending_message(chat_id: int) -> None:
    """Функция посылает сообщение о курсе по наступлению запланированного
    времени отправки"""
    text = generate_stock_text()
    logging.info(f'Sending message to chat_id: {chat_id}')
    await bot.send_message(chat_id=chat_id, text=text)
    chat = await bot.get_chat(chat_id)
    user_id = chat.id
    add_msg_to_history(user_id=user_id, date_n_time=dt.now().strftime('%Y-%m-%d %H:%M'),
                       msg=text)


async def scheduler_sender(id_in_tg: int, chat_id: int) -> None:
    """Функция добавляет задачу запущенному в bot_config шедулеру об отправке курса
    в нужное время"""
    for user in User.select():
        if id_in_tg == user.user_id:
            user_tz_int = int(user.timezone)
            preferred_hour = int(user.preferred_time[:2])
            preferred_minute = int(user.preferred_time[3:])
            # Корректировка времени в зависимости от часового пояса пользователя
            moscow_tz_int = 3  # Московское время UTC+3
            adjusted_hour = (preferred_hour - user_tz_int + moscow_tz_int) % 24
            logging.info(
                f'User timezone: {user.timezone}, Original send time: {preferred_hour}:{preferred_minute}, '
                f'Adjusted send time: {adjusted_hour}:{preferred_minute} UTC+3')
            scheduler.add_job(sending_message, 'cron', hour=adjusted_hour, minute=preferred_minute, args=[chat_id])
