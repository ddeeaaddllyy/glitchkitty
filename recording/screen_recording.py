import time
import cv2
import numpy as np
import mss
import asyncio

FOURCC = cv2.VideoWriter_fourcc(*'mp4v')


def record_screen(filename: str, duration: int, fps: int) -> tuple[bool, str]:
    try:
        with mss.mss() as sct:

            monitor = sct.monitors[1]
            width = monitor["width"]
            height = monitor["height"]

            out = cv2.VideoWriter(filename, FOURCC, fps, (width, height))

            if not out.isOpened():
                return False, "Не удалось инициализировать VideoWriter. Проверьте кодек."

            total_frames = duration * fps
            start_time = time.time()
            frames_recorded = 0

            while frames_recorded < total_frames:

                sct_img = sct.grab(monitor)

                frame = np.array(sct_img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                out.write(frame)
                frames_recorded += 1

                time_passed = time.time() - start_time
                expected_time = frames_recorded / fps
                time_to_wait = expected_time - time_passed
                if time_to_wait > 0:
                    time.sleep(time_to_wait)

            out.release()

            if frames_recorded > 0:
                print(f"Запись завершена. Записано кадров: {frames_recorded}")
                return True, ""
            else:
                return False, "Не записано ни одного кадра."

    except Exception as e:
        return False, f"Критическая ошибка записи: {e}"
