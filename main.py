import const
import dbwork
import excelwork
import pyowm
import logging
import xlrd
import asyncio
from geopy import distance
from geopy.distance import lonlat, distance, geodesic, vincenty
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, venue
from aiogram.bot import api


owm = pyowm.OWM(const.key_Token_open_weather)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PATCHED_URL = "https://telegg.ru/orig/bot{token}/{method}"
setattr(api, 'API_URL', PATCHED_URL)

loop = asyncio.get_event_loop()
bot = Bot(token=const.key_Token, parse_mode="HTML")
dp = Dispatcher(bot=bot, loop=loop)

button_news = KeyboardButton('Новости 💬')
button_location = KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
button_weather = KeyboardButton("Погода 🌤")
markup_first = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup_first.add(button_news, button_weather, button_location)

inline_button_exhibitions = InlineKeyboardButton("Выставки", callback_data="exhibitions")
inline_button_activity = InlineKeyboardButton("Мероприятия", callback_data="activity")
inline_button_stock = InlineKeyboardButton("Акция", callback_data="stock")
inline_markup_first = InlineKeyboardMarkup(row_width=2)
inline_markup_first.add(inline_button_exhibitions, inline_button_activity, inline_button_stock)


@dp.callback_query_handler(lambda qwer: qwer.data == "exhibitions")
async def work_answer_exhibitions(callback_query: types.CallbackQuery):
    info_name = "Выставки"
    work_db = dbwork.DATABase()
    messages = work_db.data_info_return(info_name)
    await bot.send_message(callback_query.from_user.id, messages)


@dp.callback_query_handler(lambda qwer: qwer.data == "activity")
async def work_answer_activity(callback_query: types.CallbackQuery):
    info_name = "Мероприятия"
    work_db = dbwork.DATABase()
    messages = work_db.data_info_return(info_name)
    await bot.send_message(callback_query.from_user.id, messages)


@dp.callback_query_handler(lambda qwer: qwer.data == "stock")
async def work_answer_exhibitions(callback_query: types.CallbackQuery):
    info_name = "Акции"
    work_db = dbwork.DATABase()
    messages = work_db.data_info_return(info_name)
    await bot.send_message(callback_query.from_user.id, messages)


@dp.message_handler(lambda message: 'Новости 💬' == message.text)
async def work_answer_news(message: types.message):
    info_name = "Главные новости"
    work_db = dbwork.DATABase()
    messages = work_db.data_info_return(info_name)
    await message.reply(messages, reply=False, reply_markup=inline_markup_first)


@dp.message_handler(lambda message: 'Погода 🌤' == message.text)
async def work_weather(message: types.message):
    observation = owm.weather_at_place('Moscow, RU')
    w = observation.get_weather()
    weather_temp = w.get_temperature('celsius')['temp']
    weather_temp_max = w.get_temperature('celsius')['temp_max']
    weather_temp_min = w.get_temperature('celsius')['temp_min']
    weather_answer = (
        """В Москве сейчас {}℃ (mаx={}℃ min={}℃)""".format(weather_temp, weather_temp_max, weather_temp_min))
    await message.reply(weather_answer, reply=False)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user = types.User.get_current()
    await message.reply(
        """Привет {}! 
        Я - PlaceForMoscow
        "текст про бота"
        """.format(user.first_name),
        reply=False, reply_markup=markup_first
    )
    # await message.reply("Убираем шаблоны сообщений", reply_markup=ReplyKeyboardRemove())
    work_db = dbwork.DATABase()
    work_db.data_add_new_person()



@dp.message_handler(commands=['help'])
async def send_menu(message: types.Message):
    await message.reply(
        """
        Бот ничего не ответил?
        — Просто повторите запрос.
        
        Что делать, если не отображаются кнопки?
        — Найдите в правом нижнем углу иконку клавиатуры (выглядит, как 4 квадрата в рамке) и нажмите на неё.
        
        Хотите оставить фидбек
        — Начните сообщение со слова "Админ".
        
        Что я умею:
        >>>>>>>>>>>
        """, reply=False
    )


@dp.message_handler(commands=['admin'])
async def work_admin(message: types.Message):
    user = types.User.get_current()
    if user.id == const.admin_id:
        await message.reply("info ", reply=False)


@dp.message_handler(lambda message: True, content_types=['location'])
async def work_location(message: types.Message):
    lon = message.location.longitude
    lat = message.location.latitude
    user_local = (lat, lon)
    workexcel = excelwork.Excel()
    index = workexcel.distance_calculation(user_local)
    print(index)
    await message.reply("Рядом с вами: {}".format(workexcel.common_name[index]), reply=False)
    await message.answer_venue(latitude=workexcel.array_lat[index],
                               longitude=workexcel.array_lon[index],
                               title=workexcel.category[index],
                               address=workexcel.common_name[index])


@dp.message_handler(content_types=types.ContentType.TEXT)
async def work_echo(message: types.Message):
    work_db = dbwork.DATABase()
    text = message.text
    user = types.User.get_current()
    if user.id == const.admin_id:
        if text.startswith("Выставки"):
            info_name = "Выставки"
            info_text = message.text
            work_db.data_update_info(info_name, info_text)
            await message.reply("save", reply=False)

        elif text.startswith("Мероприятия"):
            info_name = "Мероприятия"
            info_text = message.text
            work_db.data_update_info(info_name, info_text)
            await message.reply("save", reply=False)

        elif text.startswith("Акции"):
            info_name = "Акции"
            info_text = message.text
            work_db.data_update_info(info_name, info_text)
            await message.reply("save", reply=False)

        elif text.startswith("Главные новости"):
            info_name = "Главные новости"
            info_text = message.text
            work_db.data_update_info(info_name, info_text)
            await message.reply("save", reply=False)

        elif text.startswith("answer"):
            work_db.data_return_all_info()
            await message.reply(work_db.data_return_all_info(), reply=False)

    elif text and user.id != const.admin_id and not text.startswith('/'):
        await message.reply("{} такой команды нет".format(text), reply=False)
        person_answer = text
        work_db.data_add_text_person(person_answer)
    elif text and user.id != const.admin_id and text.startswith('/'):
        await message.reply("{} такой команды нет".format(text), reply=False)


async def send_admin_startup(dp):
    await bot.send_message(chat_id=const.admin_id, text="Бот запущен")


def main():
    executor.start_polling(dispatcher=dp, skip_updates= True, on_startup=send_admin_startup)


if __name__ == '__main__':
    main()
