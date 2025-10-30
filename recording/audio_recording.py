import sounddevice as sd
from scipy.io.wavfile import write


def record_audio(filename: str, duration: int, samplerate: int, channels: int) -> tuple[bool, str]:
    """Записывает звук с микрофона олуха и сохраняет в WAV."""

    try:
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')

        sd.wait()

        write(filename, samplerate, recording)

        return True, ""

    except Exception as e:
        return False, f"Ошибка записи аудио: {e}. Проверьте микрофон и разрешения."
