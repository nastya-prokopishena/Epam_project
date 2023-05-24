import aiomysql
import aiogram
import asyncio
from datetime import datetime

async def connect_to_db():
    try:
        conn = await aiomysql.connect(
            host='localhost',
            port=3306,
            user="root",
            password="root1234",
            db="table_bookings",
            cursorclass=aiomysql.DictCursor)
    
        print("Connected successfully...")
        return conn
    
    except Exception as ex:
        print("Connection to DataBase refused...")
        print(ex)
        
async def get_table_bookings(table_number):
    try:
        conn = await connect_to_db() 
        async with conn.cursor() as cursor:
            query = """
            SELECT id, booking_start, booking_end
            FROM bookings
            WHERE table_number = %s AND booking_end > NOW()
            """
            await cursor.execute(query, (table_number,))
            bookings = await cursor.fetchall()
    
        return bookings

    except Exception as ex:
        print("Error occurred while fetching bookings from the database:")
        print(ex)
        return []


async def cancel_booking(booking_id):
    try:
        conn = await connect_to_db()
        async with conn.cursor() as cursor:
            query = "DELETE FROM bookings WHERE id = %s"
            await cursor.execute(query, (booking_id,))
            await conn.commit()
        return True
    
    except Exception as ex:
        print("Error occurred while canceling booking:")
        print(ex)
        return False
