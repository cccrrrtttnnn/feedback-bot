import os
from aiogram import Router, F
from aiogram.filters import Filter, Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode

import keyboards.adminkb as kb
from database.requests import (get_tickets, get_user_by_id, get_ticket_by_id, delete_ticket,
                               save_ticket_answer)

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from dotenv import load_dotenv

load_dotenv()

admin = Router()

ADMIN_ID = int(os.getenv("ADMIN", "0"))

class AdminProtect(Filter):
    def __init__(self):
        self.admin_id = ADMIN_ID
    async def __call__(self, message: Message):
        return message.from_user.id == self.admin_id

class Answer(StatesGroup):
    answer = State()

@admin.message(AdminProtect(), Command('adm_menu'))
async def adm_menu(message: Message):
    await message.answer('Admin Menu', reply_markup=kb.main, parse_mode=ParseMode.HTML)

@admin.callback_query(F.data == 'ticket')
async def tickets_list(callback: CallbackQuery):
    tickets = await get_tickets()
    if not tickets:
        await callback.message.edit_text("Нет тикетов")
        return

    tickets_with_users = []
    for ticket in tickets:
        user = await get_user_by_id(ticket.user)
        tickets_with_users.append((ticket, user))
    await callback.message.edit_text("Выберите тикет:", reply_markup=await kb.ticket_list(tickets_with_users))

@admin.callback_query(F.data.startswith("ticket_"))
async def show_ticket_detail(callback: CallbackQuery):
    ticket_id = int(callback.data.split("_")[1])
    ticket = await get_ticket_by_id(ticket_id)
    user = await get_user_by_id(ticket.user)
    text = (
        f"⏰ <b>Новый тикет!</b>\n\n"
        f"<b>👤 Пользователь:</b> {user.tg_id} | @{user.tg_user}\n\n"
        f"<blockquote>{ticket.message}</blockquote>"
    )
    await callback.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=await kb.ticket_detail(ticket.id))

@admin.callback_query(F.data.startswith("answer_"))
async def prompt_answer(callback: CallbackQuery, state: FSMContext):
    ticket_id = int(callback.data.split("_")[1])
    await state.update_data(ticket_id=ticket_id)
    await callback.message.answer("Напишите ответ для пользователя:")
    await callback.message.delete()
    await state.set_state(Answer.answer)

@admin.message(Answer.answer)
async def process_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    ticket_id = data.get("ticket_id")
    answer_text = message.text
    ticket = await get_ticket_by_id(ticket_id)
    ticket.answer = answer_text
    ticket.status = "success"
    await save_ticket_answer(ticket)
    user = await get_user_by_id(ticket.user)
    await message.bot.send_message(user.tg_id, f"Ответ на ваш тикет:\n{answer_text}")
    await message.answer("Ответ отправлен")
    await state.clear()

@admin.callback_query(F.data.startswith("decline_"))
async def decline_ticket(callback: CallbackQuery):
    ticket_id = int(callback.data.split("_")[1])
    ticket = await get_ticket_by_id(ticket_id)
    user = await get_user_by_id(ticket.user)
    await delete_ticket(ticket_id)
    await callback.answer("Тикет удален")
    await callback.bot.send_message(user.tg_id, "Ваш тикет отклонен")
    await callback.message.edit_text("Админ меню", reply_markup=kb.main)
