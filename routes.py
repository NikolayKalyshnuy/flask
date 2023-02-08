from main import app
from flask import render_template, url_for
from models import db
from models import Product, Order, OrderProduct

from multiprocessing import Process
from aiogram import types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, LabeledPrice, ContentType
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from main import dispatcher as dp, bot
import bot.keyboards as keyboards
import bot.Price as Price

def bot_start_polling():
    executor.start_polling(dispatcher=dp, skip_updates=True)

@app.route('/')
def catalog():
    return render_template("catalog.html", products=Product.query.all(), order_product=OrderProduct)

@app.get(rule='/start_bot')
def start_bot():
    print("Bot start")
    bot_process = Process(target=bot_start_polling)
    bot_process.start()
    return str(bot_process.pid)


from bot.config import admin_id, users

class register(StatesGroup):
    state1 = State()
    state2 = State()
    complaint_add = State()


@dp.message_handler(Command('start'))
async def start(message: Message):
    if await bot.send_message(message.chat.id, "Hey"):
        # register_(message.answer)
        await message.answer('Hello, bot is running.\nGo to registration.')
        await message.answer('Hey! You have started registration.\nEnter your name please')
        await register.complaint_add.set()

        with open('id.csv', 'a', encoding='utf8') as f:
            f.write(f'{message.from_user.id}:{message.from_user.first_name}''\n')  # Тест запись в csv


@dp.message_handler(state=register.complaint_add)
async def process_fio_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['complaint'] = message.text
        await message.answer(f'Добро пожаловать {data["complaint"]}')
        await message.answer(f'Enter your phone number please')
        await register.state1.set()


@dp.message_handler(state=register.state1)
async def process_fio_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
        await message.answer(f'Your number {data["phone"]}')
        await message.answer('Registration successfully', reply_markup=keyboards.kb)
        await state.finish()


@dp.message_handler(Command('sendall'))  # рассылка сообщений пользователям бота.
async def send_all(message: Message):  # вызываем /sendall и после пробела вводим текст, который хотим отправить.
    if message.chat.id == admin_id:  # Пример: /sendall Hello. В сообщении отправит текст - Hello.
        await message.answer('Start')
        for i in users:
            await bot.send_message(i, message.text[message.text.find(' '):])
        await message.answer('Done')
    else:
        await message.answer('Error')


@dp.message_handler(content_types="web_app_data")  # получаем отправленные данные
async def answer(web_app_message):
    await bot.send_message(web_app_message.chat.id,
                           Price.PRICE[f'{web_app_message.web_app_data.data}'][f'{web_app_message.web_app_data.data}'])
    # отправляем сообщение в ответ на отправку данных из веб-приложения


@dp.message_handler(content_types='text')
async def order(message: Message):
    await bot.send_message(message.chat.id, Price.PRICE['1']['1'])

