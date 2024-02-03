import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from main import create_answer, check_file, take_config, get_request

TOKEN = take_config('API_TOKEN')

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\n/help - команда для ознакомления с возможностями.")

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
    except TypeError:
        await message.answer("Не понял. Свяжись с Евгением")
        await bot.send_contact(take_config("ADMIN_CONTACT"), take_config("ADMIN_NUMBER"), 'Евгений')

@dp.message(Command('contact'))
async def admin_contact(message: types.Message) -> None:
    await bot.send_contact(take_config("ADMIN_CONTACT"), take_config("ADMIN_NUMBER"), 'Евгений')

@dp.message(Command('id'))
async def get_user_id(message: types.Message) -> None:
    await message.answer(f"{str(message.from_user.id)}")

@dp.message(Command('request'))
async def create_layout(message: types.Message) -> None:
    request_text = message.reply_to_message.text
    request_get = get_request(request_text)
    await message.reply(request_get)

@dp.message(Command('help'))
async def help(message: types.Message) -> None:
    await message.answer("Привет!\nСбрось сюда файл дебиторки и получишь вывод должников, которые закреплены за тобой!\n/id - для вывода своего id телеграма\n/request - создание шаблона для отправки бугхалтеру (Обязательно процитируй нужное сообщение из списка должников!)")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())