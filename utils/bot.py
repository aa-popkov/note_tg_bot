from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import client

from utils import config

redis = client.Redis(password=config.REDIS_PASSWORD)
dp = Dispatcher(storage=RedisStorage(redis))
bot = Bot(config.TG_BOT_API_KEY, parse_mode=ParseMode.HTML)
