from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💬 Тикеты', callback_data='ticket')]
])

async def ticket_list(tickets_with_users):
    builder = InlineKeyboardBuilder()
    for ticket, user in tickets_with_users:
        builder.button(text=f"№{ticket.id} | {user.tg_id}", callback_data=f"ticket_{ticket.id}")
    builder.adjust(1)
    return builder.as_markup()

async def ticket_detail(ticket_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ответить', callback_data=f'answer_{ticket_id}'), InlineKeyboardButton(text='Отклонить', callback_data=f'decline_{ticket_id}')],
    [InlineKeyboardButton(text='Назад', callback_data='123')]
    ])
    return keyboard
