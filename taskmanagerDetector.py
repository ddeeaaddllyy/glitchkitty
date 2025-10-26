import asyncio
import psutil
import sys

TASKMGR = 'Taskmgr.exe'
new = ['T', 'a', 's', 'k', 'm', 'g', 'r', '.', 'e', 'x', 'e']
# реализую обход в будущем


async def if_taskmgr_open():
    """Шмон программы если поялвяется диспетчер"""
    while True:
        found = await asyncio.to_thread(lambda:
                                        any(p.info['name'] == TASKMGR for p in psutil.process_iter(['name']))
                                        )
        if found:
            sys.exit()
