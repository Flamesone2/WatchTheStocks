from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from handlers_and_keyboards.utils import create_keyboard, generate_stock_text
from database_pkg.database_file import History, add_msg_to_history, create_tables
from datetime import datetime as dt

router = Router()


@router.message(CommandStart())
async def handle_start(message: types.Message) -> None:
    """Хендлер для комманды /start с inline клавиатурой"""
    text = markdown.text(
        f"Привет, {message.from_user.first_name}! Я биржевой бот, "
        "могу сообщить актуальный курс доллара и евро, а также "
        "стоимость биткоина и золота! Ещё я могу отправлять обновления "
        "цен на эти активы ежедневно "
        "в назначенное вами время")
    markup = create_keyboard()
    await message.answer(text=text, parse_mode="HTML",
                         reply_markup=markup)


@router.message(Command("printstock"))
async def printstock_cmd(message: types.Message) -> None:
    """Хендлер для комманды /printstock"""
    text = generate_stock_text()
    add_msg_to_history(user_id=message.from_user.id,
                       date_n_time=dt.now().strftime('%Y-%m-%d %H:%M'),
                       msg=text)
    await message.answer(text=text, parse_mode="HTML")


@router.message(Command("help"))
async def bot_help(message: types.Message) -> None:
    """Хендлер для комманды /help"""
    text = "Я могу сообщить вам актуальные курсы доллара и евро, а также стоимость биткоина и золота"
    markup = create_keyboard()
    await message.answer(
        parse_mode="HTML",
        text=text,
        reply_markup=markup
    )


@router.message(Command("history"))
async def history(message: types.Message) -> None:
    """Хендлер для комманды /history"""
    text = str()
    create_tables()
    for msg in History.select():
        if message.from_user.id == msg.user_id:
            text += (f'{msg.date_n_time}\n'
                     f'{msg.msg}\n'
                     f'\n')

    if not text:
        text = "История сообщений пуста."

    await message.answer(text='История сообщений:\n')
    await message.answer(
        parse_mode="HTML",
        text=text
    )
