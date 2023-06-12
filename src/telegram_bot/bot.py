from aiogram import Bot, types
import asyncio
import os
from dotenv import load_dotenv
# load env variables from .env file
load_dotenv()

# Initialize bot and dispatcher
bot = Bot(token=os.environ.get('BOT_TOKEN', "Nikolai Durov"))
CHANNEL_ID = -1001961706671


async def send_photo(photo_path, caption):
    """
    This function sends a message with an attached photo to the specified chat.

    Parameters:
    chat_id (int or str): Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    photo_path (str): File path to the photo.
    caption (str): Caption to be sent with the photo.
    """
    await bot.send_photo(CHANNEL_ID, types.InputFile(photo_path), caption=caption, parse_mode='HTML')
