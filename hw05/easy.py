import asyncio
import aiohttp
import sys

URL = "https://picsum.photos/500"


async def run():
    count = int(sys.argv[1])
    path = sys.argv[2] if len(sys.argv) > 2 else "artifacts/easy/"

    async with aiohttp.ClientSession() as session:
        for i in range(count):
            async with session.get(URL) as response:
                with open(f"{path}{i}.png", "bw") as file:
                    file.write((await response.content.read()))


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
