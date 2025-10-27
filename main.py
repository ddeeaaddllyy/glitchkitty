import asyncio
from taskmanagerDetector import if_taskmgr_open
from telegrambot import main


async def mainActivity():
    """работаем со всем асинхронно"""

    await asyncio.gather(
        if_taskmgr_open(),
        main(),
    )


if __name__ == '__main__':
    try:
        asyncio.run(mainActivity())
    except KeyboardInterrupt:
        print('bye bye =)')