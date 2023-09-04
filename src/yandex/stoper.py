import asyncio


class Stoper:

    async def stoper(self, timeout):
        await asyncio.sleep(timeout)
