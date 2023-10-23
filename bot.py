import os
import asyncio
import logging

from contextlib import suppress
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters.command import Command
from aiogram.types import BotCommand
from aiogram.methods.delete_message import DeleteMessage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

from utils.mail1sec import generate_mails, check_mail, delete_mail


load_dotenv()


logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def setup_bot_commands():
    bot_commands = [
        BotCommand(command="/start", description="Стартуем!"),
        BotCommand(command="/new_mail", description="Создать новый временный почтовый ящик"),
        BotCommand(command="/delete_mail", description="Удалить временную почту"),
        BotCommand(command='/clear', description='Очистить предыдущие сообщения')
    ]
    await bot.set_my_commands(bot_commands)


@dp.message(Command('clear'))
async def clear(message: types.Message):
    chat_id = message.chat.id
    message_id = message.message_id

    await bot.delete_message(chat_id=chat_id, message_id=message_id)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаём обработчик создания кнопок
    builder = InlineKeyboardBuilder()
    # Сама кнопка
    builder.add(types.InlineKeyboardButton(
        text="Создать почту",
        callback_data="create_mail")
    )
    # Сообщение и вывод кнопки ответом
    await message.answer("Бот поможет создать временную почту в 1 клик!",
        reply_markup=builder.as_markup())

# Обработчик нажатия кнопки создания почты
@dp.callback_query(F.data == "create_mail")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(generate_mails())
    await callback.answer()


@dp.message(Command("new_mail"))
async def new_mail(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Удалить",
        callback_data="random_value")
    )
    await message.answer(generate_mails())


@dp.message(Command("delete_mail"))
async def new_mail(message: types.Message):
    await message.answer(delete_mail())


async def main():
    await dp.start_polling(bot)
    await dp.message.register(setup_bot_commands)


if __name__ == "__main__":
    asyncio.run(main())
