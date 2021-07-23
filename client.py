import time
import asyncio

import aiohttp


async def fetch(session, url, body):
    data = {
        'body': body,
    }
    async with session.post(url, json=data) as response:
        return await response.text()


async def post_filter(url, pattern):
    data = {
        'pattern': pattern,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.text()


async def main():
    start = time.monotonic()
    server = 'http://0.0.0.0:4567/'
    path_filters = server + 'filters'
    path_send = server + 'send'
    good_pattern = 'C+'
    redos_pattern = 'A(B|C+)+D'
    redos_time_x = 300
    redoc_inject = False
    body = 'ACCCCCCCCCCCCCCCCCCCCCCCCX'
    rps = 2

    await post_filter(path_filters, good_pattern)

    while True:
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, path_send, body) for _ in range(rps)]
            responses = await asyncio.gather(*tasks)
            print('rps!')
            for response in responses:
                print(response)
            if start + redos_time_x < time.monotonic() and not redoc_inject:
                await post_filter(path_filters, redos_pattern)
                redoc_inject = True
                print('redos inject')
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
