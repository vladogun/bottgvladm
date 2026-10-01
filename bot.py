import asyncio
import logging
import os
from typing import Union

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- Фильтр: пускает только админа ---
class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == ADMIN_ID


# Все хэндлеры ниже видят только сообщения от админа
@dp.message(IsAdmin(), Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")


@dp.message(IsAdmin(), Command("help"))
async def cmd_help(message: Message):
    await message.answer("Доступные команды:\n/start\n/help")


@dp.message(IsAdmin(), F.text)
async def echo(message: Message):
    await message.answer(message.text)


# Всем остальным — вежливый отказ (опционально)
@dp.message()
async def deny(message: Message):
    await message.answer("Извини, бот приватный.")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())