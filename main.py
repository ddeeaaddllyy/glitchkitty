import asyncio
from other_utilits.taskmanagerDetector import if_taskmgr_open
from telegram.telegrambot import main


async def mainActivity():
    """работаем со всем асинхронно"""

    await asyncio.gather(
        if_taskmgr_open(),
        main(),
    )


if __name__ == '__main__':
    asyncio.run(mainActivity())
