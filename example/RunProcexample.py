import asyncio
from pydbsprocket.core.provider import init_db_provider
from config.database import DB_PROVIDER, DB_CONN
from db_calls.yt import get_channel_video_data
from time import perf_counter


async def run_proc(channel_id: str) -> None:

    disc_start_time = perf_counter()
    db = await init_db_provider(DB_PROVIDER, DB_CONN)
    disc_end_time = perf_counter()

    pool_start_time = perf_counter()
    await db.create_pool()
    pool_end_time = perf_counter()

    proc_start_time = perf_counter()
    data = await get_channel_video_data(channel_id)
    proc_end_time = perf_counter()

    teardown_start_time = perf_counter()
    await db.close_pool()
    teardown_end_time = perf_counter()

    resultgen_start_time = perf_counter()
    for row in data:
        print(row)
    resultgen_end_time = perf_counter()

    print(f'Discovery Time: {disc_end_time - disc_start_time}')
    print(f'Pool Time: {pool_end_time - pool_start_time}')
    print(f'Proc Time: {proc_end_time - proc_start_time}')
    print(f'Teardown Time: {teardown_end_time - teardown_start_time}')
    print(f'Result Print Time: {resultgen_end_time - resultgen_start_time}')

if __name__ == '__main__':
    asyncio.run(run_proc('UCzPrD3YgJsBMV23Gra2f00w'))