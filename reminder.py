import aiogram
from aiogram import types, Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Update
from aiogram.types.chat_member import ChatMemberMember, ChatMemberOwner, ChatMemberAdministrator
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboard import on_players_online_press
from keyboard import on_booking_press
from database import get_table_bookings
from database import cancel_booking

TOKEN_API = "6064195503:AAHL9SrKGWqdynJUqqIn04o9dJF8p4-nWVM"

bot = aiogram.Bot(TOKEN_API)
dp = aiogram.Dispatcher(bot)

async def send_telegram_announcement(booking_data, booking_time):
    announcement_message = f"<b>Table booked!</b>\n\n<b>Name</b>: {booking_data['name']} {booking_data['surname']}\n<b>Table Number</b>: {booking_data['tableNumber']}\n<b>Email</b>: {booking_data['email']}\n<b>Phone</b>: {booking_data['phone']}\n<b>Booking Time</b>: {booking_time}"
    await bot.send_message(chat_id = 1013673667,
                           text=announcement_message,
                           parse_mode="HTML")

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    if last_name is None:
        await bot.send_message(chat_id=message.from_user.id,
                           text=f"<b>Вітаю, {message.from_user.first_name}!</b>",
                           parse_mode="HTML",
                           reply_markup=on_players_online_press())
    else:
        await bot.send_message(chat_id=message.from_user.id,
                           text=f"<b>Вітаю, {message.from_user.first_name} {message.from_user.last_name}!</b>",
                           parse_mode="HTML",
                           reply_markup=on_players_online_press())

@dp.message_handler(text='Назад 🔙')
async def update_reply_keyboard_back(message: types.Message) -> None:
   await bot.send_message(chat_id=message.from_user.id,
                           text='<b>Головне меню 🧾</b>',
                           parse_mode="HTML",
                           reply_markup=on_players_online_press())
   
@dp.message_handler(text='Пореглянути бронювання 🕐')
async def update_reply_keyboard_back(message: types.Message) -> None:
   await bot.send_message(chat_id=message.from_user.id,
                           text='<b>Меню бронювання 🧾</b>',
                           parse_mode="HTML",
                           reply_markup=on_booking_press())
   
@dp.message_handler(text=['Стіл 1', 'Стіл 2', 'Стіл 3', 'Стіл 4', 'Стіл 5', 'Стіл 6', 'Стіл 7', 'Стіл 8', 'Стіл 9'])
async def handle_table_booking_selection(message: types.Message):
    table_number = int(message.text.split()[1])  # Extract the table number from the button text
    bookings = await get_table_bookings(table_number)
    
    keyboard = InlineKeyboardMarkup(row_width=1)  # Initialize the keyboard variable
    
    if bookings:
        for booking in bookings:
            booking_id = booking['id']
            booking_start = booking['booking_start']
            booking_end = booking['booking_end']
            
            button_text = f"ID: {booking_id}\nStart: {booking_start}\nEnd: {booking_end}"
            button_callback_data = f"cancel_booking_{booking_id}_{booking_start}_{booking_end}"
            keyboard.add(InlineKeyboardButton(text=button_text, callback_data=button_callback_data))
        
        response_message = f"<b>Valid Bookings for Table {table_number}:</b>\n\n"
        response_message += "Please select the booking interval you want to cancel:"
    else:
        response_message = f"No valid bookings found for Table {table_number}"
        
    await bot.send_message(chat_id=message.chat.id, text=response_message, parse_mode="HTML", reply_markup=keyboard)




# Callback query handler to handle cancel booking interval button press
@dp.callback_query_handler(lambda query: query.data.startswith('cancel_booking_'))
async def handle_cancel_booking(query: types.CallbackQuery):
    booking_id = query.data.split('_')[2]  # Extract the booking ID from the callback data
    booking_start = query.data.split('_')[3]
    booking_end = query.data.split('_')[4]
    # Implement your logic to cancel the specific interval of the booking using the booking ID
    await cancel_booking(booking_id)
    
        
    await bot.send_message(chat_id=query.message.chat.id, text=f"Booking ID {booking_id} with interval {booking_start} - {booking_end} was canceled.")
if __name__ == '__main__':
    executor.start_polling(dp, 
                           skip_updates=True)    