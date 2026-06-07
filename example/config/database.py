from pydbsprocket.core.connections import ConnectionConfig
import os

DB_PROVIDER = 'postgres'
DB_CONN = ConnectionConfig(host=os.getenv("DB_HOST", "localhost"),
                         port=5432,
                         database='PDBS_DemoDB',
                         username='demo_user',
                         password='demo_password',
                         schema='web_api',
                         )
