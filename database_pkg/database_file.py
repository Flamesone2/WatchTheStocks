import peewee as pw

user_db = pw.SqliteDatabase('user_timezones_and_time_preferences.db')
history_db = pw.SqliteDatabase('user_history.db')


class BaseModel(pw.Model):
    """Класс выполняет функцию базовой модели для User и History"""

    class Meta:
        order_by = 'id'


class User(BaseModel):
    """Класс нужен для создания таблицы в которой
    будут храниться часовой пояс и время отправки
    курса для каждого пользователя"""
    user_id = pw.IntegerField(unique=True)
    timezone = pw.CharField()
    preferred_time = pw.CharField()

    class Meta:
        database = user_db


class History(BaseModel):
    """Нужен для создания таблицы где хранится
     история сообщений о курсе валют"""
    date_n_time = pw.CharField()
    msg = pw.CharField()
    user_id = pw.IntegerField()

    class Meta:
        database = history_db


def add_user_timezone_preferences(user_id: int, timezone: str, preferred_time: str) -> None:
    """Обновляет часовой пояс и предпочитаемое время для существующего пользователя или
    добавляет нового со всей информацией в БД"""
    create_tables()
    if User.select().where(User.user_id == user_id).exists():
        print('Это старый пользователь')
        user = User.get(User.user_id == user_id)
        user.timezone = timezone
        user.preferred_time = preferred_time
        user.save()
    else:
        User.create(user_id=user_id, timezone=timezone, preferred_time=preferred_time)


def add_msg_to_history(user_id: int, date_n_time: str, msg: str) -> None:
    """Добавляет новое сообщение в историю сообщений пользователя"""
    create_tables()
    History.create(user_id=user_id, date_n_time=date_n_time, msg=msg)


def create_tables():
    """Отвечает за создание таблиц, ечли они еще не были созданы"""
    with user_db:
        user_db.create_tables([User])
    with history_db:
        history_db.create_tables([History])
