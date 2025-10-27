import asyncio
import os
import cv2
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('API_TOKEN')
VIDEO_FILENAME = "recorded_video.mp4"
RECORD_DURATION_SEC = 5
FPS = 30
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')
CAMERA_INDEX = 0

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def record_video(filename: str, duration: int, fps: int, seconds: int) -> bool:

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        return False

    cap.set(cv2.CAP_PROP_FPS, fps)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(filename, FOURCC, fps, (frame_width, frame_height))

    total_frames = duration * fps
    frames_recorded = 0

    print(f"Начало записи {duration} секунд видео ({frame_width}x{frame_height} @ {fps} FPS)...")

    while frames_recorded < total_frames:
        ret, frame = cap.read()

        if ret:
            out.write(frame)
            frames_recorded += 1

        else:
            print("Предупреждение: Не удалось получить кадр.")
            break

    cap.release()
    out.release()

    cv2.destroyAllWindows()

    if frames_recorded == total_frames:
        print(f"Запись завершена. Видео сохранено как: {filename}")
        return True
    else:
        print(f"Запись прервана. Записано кадров: {frames_recorded}/{total_frames}")
        return False


@dp.message(Command("camera_record"))
async def handle_record_and_send(message: types.Message):
    chat_id = message.chat.id

    await message.answer("🎥 Начинаю запись 5-секундного видео...")

    loop = asyncio.get_running_loop()
    try:
        success = await loop.run_in_executor(
            None, record_video, VIDEO_FILENAME, RECORD_DURATION_SEC, FPS
        )
    except Exception as e:
        await message.answer(f"❌ Произошла ошибка при записи видео: {e}")
        return

    if success and os.path.exists(VIDEO_FILENAME):
        await message.answer("✅ Запись завершена. Отправляю видео...")

        try:
            video_file = types.FSInputFile(VIDEO_FILENAME)

            await bot.send_video(
                chat_id=chat_id,
                video=video_file,
                caption="Видео с веб-камеры (5 сек, 30 FPS)"
            )
            await message.answer("🎉 Видео успешно отправлено!")

        except Exception as e:
            await message.answer(f"❌ Произошла ошибка при отправке видео: {e}")

        finally:
            os.remove(VIDEO_FILENAME)
            print(f"Локальный файл {VIDEO_FILENAME} удален.")

    else:
        await message.answer("❌ Не удалось записать видео. Проверьте подключение веб-камеры.")


async def main():
    """Запускает опрос бота."""
    print("Бот запущен. Ожидание команды /000...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")