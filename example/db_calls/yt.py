from pydbsprocket.core.decorators import db_call_proc
from pydbsprocket.core.db_types import DataType, OutputParameter, InputCollectionParameter
from datetime import datetime

@db_call_proc
async def get_channel_video_data(channel_id: str):
    params = {
        'p_channel_id': channel_id,
        'cur': OutputParameter(DataType.CURSOR)
    }

    return 'web_api.get_channel_video_data', params, True, 'cur'

@db_call_proc
async def bulk_load_video_data(data: list[dict]):
    vids = [
        (
            vid['id'],
            vid['channel_id'],
            vid['channel_name'],
            vid['title'],
            vid['description'],
            datetime.strptime(vid['date_published'], "%Y-%m-%dT%H:%M:%S%z"),
            vid['tags'],
            vid['medium_thumb_url'],
            vid['max_thumb_url'],
            vid['duration'],
            vid['views'],
            vid['likes'],
            vid['dislikes'],
            vid['comments'],
            vid['outlier_score']
        )
        for vid in data
    ]

    table_in = InputCollectionParameter(
        value=vids,
        data_type='yt_data.video_data'
    )
    params = {'videos': table_in, 'row_count': OutputParameter(DataType.INTEGER)}

    return 'web_api.bulk_insert_video_data', params, False, 'row_count'