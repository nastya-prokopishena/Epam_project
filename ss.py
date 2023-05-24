from aiogram import types, Bot, Dispatcher, executor

TOKEN_API = "6064195503:AAHL9SrKGWqdynJUqqIn04o9dJF8p4-nWVM"

bot = aiogram.Bot(TOKEN_API)
dp = aiogram.Dispatcher(bot)

async def send_telegram_announcement(booking_data):
    # Prepare the announcement message
    announcement_message = f"Table booked!\n\nName: {booking_data['name']}\nTable Number: {booking_data['tableNumber']}\nBooking Time: {booking_data['booking_time']}"

    # Send the announcement to the bot's chat
    chat_id = await bot.get_chat_id()
    await bot.send_message(chat_id, announcement_message)
