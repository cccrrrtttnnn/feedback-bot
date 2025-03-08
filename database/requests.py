from database.models import async_session
from database.models import User, Ticket
from sqlalchemy import select, delete

async def set_user(tg_id, tg_user):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            user = User(tg_id=tg_id, tg_user=tg_user)
            session.add(user)
            await session.commit()

async def create_ticket(user_tg_id, message_text):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_tg_id))
        if user:
            ticket = Ticket(user=user.id, message=message_text, status="wait", answer="")
            session.add(ticket)
            await session.commit()

async def get_tickets():
    async with async_session() as session:
        result = await session.scalars(select(Ticket).where(Ticket.status == "wait"))
        return result.all()

async def get_ticket_by_id(ticket_id):
    async with async_session() as session:
        return await session.scalar(select(Ticket).where(Ticket.id == ticket_id))

async def get_user_by_id(user_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.id == user_id))

async def save_ticket_answer(ticket: Ticket):
    async with async_session() as session:
        await session.merge(ticket)
        await session.commit()

async def delete_ticket(ticket_id):
    async with async_session() as session:
        await session.execute(delete(Ticket).where(Ticket.id == ticket_id))
        await session.commit()
