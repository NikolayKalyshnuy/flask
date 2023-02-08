from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import bot.config as config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

logging.basicConfig(level=logging.INFO)
loop = asyncio.new_event_loop()
storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
dispatcher = Dispatcher(bot, loop, storage=storage)

import models, routes



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
