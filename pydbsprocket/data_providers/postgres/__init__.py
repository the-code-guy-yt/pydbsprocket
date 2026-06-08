from .connection import PostgresSQLProvider
from pydbsprocket.core.provider_discovery import db_provider_mapper

db_provider_mapper['postgres'] = PostgresSQLProvider
