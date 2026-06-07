from fastapi import FastAPI
from pydbsprocket.core.provider import init_db_provider
from config.database import DB_PROVIDER, DB_CONN
from db_calls.yt import get_channel_video_data, bulk_load_video_data

async def lifespan(app: FastAPI):
    print('Starting app and connecting to db')
    db = await init_db_provider(DB_PROVIDER, DB_CONN)
    await db.create_pool()
    yield  # App runs here
    await db.close_pool()

app = FastAPI(lifespan=lifespan)


@app.get("/list_videos/{channel_id}")
async def get_videos(channel_id: str):

    data = await get_channel_video_data(channel_id)
    row_count = len(data) - 1
    if row_count >=0:
        headers = data[0]
        row_count = len(data)-1
    else:
        row_count = 0
    data = [dict(zip(headers, row)) for row in data[1:]]

    return {'data_type':'YouTubeVideoData', 'rows': row_count, 'data': data}


@app.get("/list_videos")
async def get_videos_default():
    return await get_videos('UCzPrD3YgJsBMV23Gra2f00w')


@app.get("/upload_channel_data")
async def upload_channel_data():
    from data.base_data import channel_data
    upload_data = channel_data['data']
    rows_inserted = await bulk_load_video_data(upload_data)
    return {'status':'success', 'rows_inserted':rows_inserted}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("webServices:app", host="0.0.0.0", port=8080, reload=True)