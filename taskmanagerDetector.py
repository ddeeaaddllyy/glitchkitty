import asyncio
import psutil
import sys

task = ['T', 'a', 's', 'k', 'm', 'g', 'r', '.', 'e', 'x', 'e']


async def if_taskmgr_open():
    """Шмон программы если поялвяется диспетчер"""
    while True:
        found = await asyncio.to_thread(lambda:
                                        any(p.info['name'] == ''.join(task) for p in psutil.process_iter(['name']))
                                        )
        if found:
            sys.exit()
