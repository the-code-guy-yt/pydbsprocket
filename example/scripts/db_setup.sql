--Creates The DemoDB for pydbsprocket package
--exec:  psql -U my_user_here -d postgres -f db_setup.sql

\echo 'Creating pydbsprocket example db'

CREATE DATABASE "PDBS_DemoDB"
    WITH
    TEMPLATE = template0
    ENCODING = 'UTF8'
    LC_COLLATE = 'C.UTF-8'
    LC_CTYPE = 'C.UTF-8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

\c "PDBS_DemoDB"

\echo 'Creating Schemas'

CREATE SCHEMA IF NOT EXISTS yt_data;
CREATE SCHEMA IF NOT EXISTS web_api;

\echo 'Creating Table yt_data.video_data and building indexes'
\ir db_objs/video_data.sql

--Create Service Account
\echo 'Creating demo_user'
DO
$$
BEGIN
    -- Only create the user if it does not exists - use catalog data for this
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'demo_user') THEN
        CREATE USER demo_user WITH PASSWORD 'demo_password';

        -- Since you hate waste, ensure it has no default permissions
        ALTER ROLE demo_user SET search_path = web_api, public;
    END IF;
END
$$;

\echo 'Updating Permissions for demo_user'
REVOKE ALL ON ALL TABLES IN SCHEMA yt_data FROM demo_user;
REVOKE ALL ON SCHEMA yt_data FROM demo_user;
GRANT USAGE ON SCHEMA web_api TO demo_user;

\echo 'Compiling Procedure web_api.get_channel_video_data'
\ir db_objs/get_channel_video_data.sql

\echo 'Compiling Procedure web_api.bulk_insert_video_data'
\ir db_objs/bulk_insert_video_data.sql


