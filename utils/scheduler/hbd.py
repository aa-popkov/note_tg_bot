from datetime import datetime, date

from models import UserHappyBirthday, User
from utils.bot import bot


async def hbd_notify():
    notify_days = {
        30: "дней",
        14: "дней",
        3: "дня",
        1: "день",
        0: "СЕГОДНЯ",
    }
    years_old = ["год", "года", "лет"]
    all_users = await User.get_all_users()
    for user in all_users:
        user_hbd_count = await UserHappyBirthday.get_count_by_user(user.tg_id)
        for i in range(0, user_hbd_count, 5):
            user_hbd = await UserHappyBirthday.get_all_hbd_by_user(user.tg_id, i)
            for hbd in user_hbd:
                start_date = date(
                    date.today().year,
                    hbd.person_birthdate.month,
                    hbd.person_birthdate.day,
                )
                date_diff = (start_date - date.today()).days
                if date_diff not in notify_days.keys():
                    continue

                notify_text = (
                    notify_days.get(0)
                    if date_diff == 0
                    else f"через {date_diff} {notify_days.get(date_diff)}"
                )

                years_num = datetime.today().year - hbd.person_birthdate.year
                years_text = years_old[
                    (
                        2
                        if years_num == 0
                        or years_num % 10 == 0
                        or years_num % 10 > 5
                        or years_num in range(11, 19)
                        else 0 if years_num % 10 == 1 else 1
                    )
                ]

                await bot.send_message(
                    chat_id=user.tg_id,
                    text=f"⏰ Напоминаю, <b>{notify_text}</b>\n"
                    f"🎂 День рождение у <b>{hbd.person_name}</b>\n"
                    f"📅 Дата: <b>{hbd.person_birthdate}</b>\n"
                    f"🎈 Исполняется: <b>{years_num} {years_text}</b>\n",
                )
