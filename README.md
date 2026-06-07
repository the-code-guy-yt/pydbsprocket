# pydbsprocket

Lightweight async Python database abstraction for calling stored procedures and retrieving output parameters including RefCursors.

---

## Why pydbsprocket?

- It's not an ORM!
- Call stored procedures with a single decorator 
  - no boilerplate
  - no complex cursor management
  - developers need only know the procedure contract — name, inputs, and outputs
    - no knowledge of the underlying database implementation is required.
- Creates an explicit data contract with stored procedures
- Full support for `OUT` parameters and PostgreSQL RefCursors
- Bulk insert via PostgreSQL composite table types
- Async-first, built on `asyncpg`
- Connection pooling out of the box
- Perfect for use in modern web frameworks like FastAPI/FastHTML
- Light weight - about as fast as it gets
- Extensible - add your own providers
- Does not allow you to accidentally expose queries - Raw SQL is not allowed
- Immune to SQL Injection

---

## Installation

```bash
uv add git+https://github.com/the-code-guy-yt/pydbsprocket.git
```

Or with pip:

```bash
pip install git+https://github.com/the-code-guy-yt/pydbsprocket.git
```

---

## Quick Start

### 1. Configure your connection

```python
# config/database.py
from pydbsprocket.core.connections import ConnectionConfig
import os

DB_PROVIDER = 'postgres'

DB_CONN = ConnectionConfig(
    host=os.getenv("DB_HOST", "localhost"),
    port=5432,
    database='my_database',
    username='my_user',
    password='my_password',
    schema='my_schema',
)
```

### 2. Define your database calls

Use the `@db_call_proc` decorator to map a Python function to a stored procedure. 

1) Collect any variables in the async function specification
2) Create a parameters dictionary of each variable that needs to be passed
   to the stored procedure.  
   **Note**: Some drivers do not support passing parameters by name for this reason all dictionary keys
   should be declared in the dict in the order that they appear in the procedure call. 
   - Driver Developers: Always use named parameters where the driver supports them. 
   - Consumers: Always assume named params are in use - Case and spelling matter.
   - All basic python types can be passed as input parameters without any parameter object
   - All output parameters should pass an OutputParameter class with a DataType enum value specified.
   - All complex input types as an InputCollectionParameter type 
     - value : A list of tuples with fields matching the layout of the type 
     - data_type: A string representing the type name in the database
3) Return a tuple containing 
   - ***Procedure name*** fully qualified with schema where appropriate (str) 
   - ***Parameters Object*** (dict)
   - ***Do you want cursors to return headers*** True or False (bool)
   - ***Field to Return*** The field to return as a string or None
     - If None is specified a full dictionary of parameters will be returned 
       - Useful if your procedure returns multiple output parameters

```python
# db_calls/yt.py
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
    params = {
        'videos': table_in,
        'row_count': OutputParameter(DataType.INTEGER)
    }
    return 'web_api.bulk_insert_video_data', params, False, 'row_count'
```

### 3. Use in a FastAPI app

```python
# webServices.py
from fastapi import FastAPI
from pydbsprocket.core.provider import init_db_provider
from config.database import DB_PROVIDER, DB_CONN
from db_calls.yt import get_channel_video_data, bulk_load_video_data


async def lifespan(app: FastAPI):
    db = await init_db_provider(DB_PROVIDER, DB_CONN)
    await db.create_pool()
    yield
    await db.close_pool()

app = FastAPI(lifespan=lifespan)


@app.get("/list_videos/{channel_id}")
async def get_videos(channel_id: str):
    data = await get_channel_video_data(channel_id)
    headers = data[0]
    rows = [dict(zip(headers, row)) for row in data[1:]]
    return {'data_type': 'VideoData', 'rows': len(rows), 'data': rows}


@app.get("/upload_channel_data")
async def upload_channel_data():
    from data.base_data import channel_data
    rows_inserted = await bulk_load_video_data(channel_data['data'])
    return {'status': 'success', 'rows_inserted': rows_inserted}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("webServices:app", host="0.0.0.0", port=8080, reload=True)
```

### 4. Run standalone (no web framework)
 - Obviously keep pools open for multiple calls and use async code where possible.

```python
import asyncio
from pydbsprocket.core.provider import init_db_provider
from config.database import DB_PROVIDER, DB_CONN
from db_calls.yt import get_channel_video_data


async def main():
    db = await init_db_provider(DB_PROVIDER, DB_CONN)
    await db.create_pool()

    data = await get_channel_video_data('my_channel_id')
    headers = data[0]
    for row in data[1:]:
        print(dict(zip(headers, row)))

    await db.close_pool()

if __name__ == '__main__':
    asyncio.run(main())
```

---

## Docker

A `docker-compose.yml` is included to build the example project for ease of use 
- spins up PostgreSQL, 
- runs the setup script to setup the initial database structure
- launches the FastAPI app on localhost:8080

```bash
docker compose up --build
```

---

## Maximum Security Procedure Implementation Guide

https://youtu.be/MS3c0EHDQpI


## Included Providers

| Provider   | Status      | Package               |
|------------|-------------|-----------------------|
| PostgreSQL | Open source | `pydbsprocket`        |

## Roadmap
1) Addition of before and after execution hooks that you can code to
Potential use cases 
  - Logging
  - Telemetry
  - Caching 
2) Unit and integration tests (contributions welcome)

## Prerequisites
- Python 3.13+ (may work on earlier versions but not tested)
- PostgreSQL (if using packaged provider)

---

## License

MIT