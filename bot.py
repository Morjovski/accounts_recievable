import asyncio
import logging
import sys
from time import sleep

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from main import create_answer, check_file, take_config

TOKEN = take_config('API_TOKEN')

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command"""
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@dp.message(F.document)
async def echo_handler(message: types.Message) -> None:
    try:
        document = message.document
        file_folder = f"files/{document.file_name}.xls"
        await bot.download(document, file_folder)
        user_id = str(message.from_user.id)
        check_file(file_folder, user_id)
        answer = create_answer()
        for msg in answer:
            await message.answer(msg)
            sleep(0.5)
    except TypeError:
        await message.answer("Nice try!")

@dp.message(Command('id'))
async def get_user_id(message: types.Message) -> None:
    await message.answer(f"{str(message.from_user.id)} - {message.from_user.first_name}")

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())