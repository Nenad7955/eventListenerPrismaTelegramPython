import asyncio

from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from db import EventRepository

dp = Dispatcher()
bot: Bot
event_repository: EventRepository


def main(telegram_api_key, event_repo):
    global bot, event_repository
    bot = Bot(token=telegram_api_key)
    event_repository = event_repo

def timestamp_to_hours_minutes_ago(timestamp):
    current_time = datetime.now()
    timestamp_time = datetime.fromtimestamp(timestamp)
    time_difference = current_time - timestamp_time
    hours_ago = int(time_difference.total_seconds() // 3600)
    minutes_ago = int((time_difference.total_seconds() % 3600) // 60)
    return f"{hours_ago}h{minutes_ago}m ago"


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.id}, {message.from_user.id}")

async def send_message():
    msg = await event_repository.get_all_events_last_24h()

    if msg == []:
        return

    await bot.send_message(chat_id=621905066, text=f"""
    Daily $AIX Stats:
         - First TX: {timestamp_to_hours_minutes_ago(min(item.timestamp for item in msg))}
         - Last TX: {timestamp_to_hours_minutes_ago(max(item.timestamp for item in msg))}
         - AIX processed: {"{:,.2f}".format(sum(int(item.aixProcessed) for item in msg) / 10 ** 18)}
         - AIX distributed: {"{:,.2f}".format(sum(int(item.aixDistributed) for item in msg) / 10 ** 18)}
         - ETH bought: {"{:,.2f}".format(sum(int(item.ethProcessed) for item in msg) / 10 ** 18)}
         - ETH distributed: {"{:,.2f}".format(sum(int(item.ethDistributed) for item in msg) / 10 ** 18)}
    """)

async def send():
    while True:
        await send_message()
        await asyncio.sleep(60*60*24)

