import asyncio
import aiohttp
import aiofiles
import sys

URL = "https://picsum.photos/500"
path = sys.argv[2] if len(sys.argv) > 2 else "artifacts/easy/"


async def sub_task(session, img_num):
    async with session.get(URL) as response:
        async with aiofiles.open(f"{path}{img_num}.png", "bw") as file:
            await file.write(await response.read())


async def run():
    count = int(sys.argv[1])
    async with aiohttp.ClientSession() as session:
        tasks = (sub_task(session, i) for i in range(count))
        await asyncio.gather(*tasks)


asyncio.run(run())
