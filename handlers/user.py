from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums import ParseMode

import keyboards.userkb as kb
from database.requests import set_user, create_ticket

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

user = Router()

class Ticket(StatesGroup):
    question = State()

@user.message(CommandStart())
async def start(message: Message):
    await set_user(message.from_user.id, message.from_user.username)
    caption = 'https://www.alleycat.org/wp-content/uploads/2019/03/FELV-cat.jpg'
    text = (
        '<b>Приветствуем!</b>\n\n'
        'Этот бот предназначен для обратной связи проекта <i>[название]</i>.\n'
        'Задай интересующий тебя вопрос и администрация его рассмотрит.'
    )
    await message.answer_photo(caption, text, parse_mode=ParseMode.HTML, reply_markup=kb.main)

@user.message(F.text == '✏️ Создать тикет')
async def create_ticket_prompt(message: Message, state: FSMContext):
    await message.answer('<b>✏️ Напишите описание своей проблемы</b>', reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    await state.set_state(Ticket.question)

@user.message(Ticket.question)
async def process_ticket(message: Message, state: FSMContext):
    await create_ticket(message.from_user.id, message.text)
    await message.answer("<b>✅ Тикет был отправлен</b>\n\n"
                         "<i>⌛️ Ожидайте ответа от администрации...</i>", parse_mode=ParseMode.HTML)
    await state.clear()
