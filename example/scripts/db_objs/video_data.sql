-- Table: yt_data.video_data

--DROP TABLE IF EXISTS yt_data.video_data CASCADE;

CREATE TABLE IF NOT EXISTS yt_data.video_data
(
    id character varying(11) COLLATE pg_catalog."default" NOT NULL,
    channel_id character varying(24) COLLATE pg_catalog."default" NOT NULL,
    channel_name text COLLATE pg_catalog."default" NOT NULL,
    title character varying(100) COLLATE pg_catalog."default" NOT NULL,
    description character varying(5000) COLLATE pg_catalog."default" NOT NULL,
    date_published timestamp with time zone NOT NULL,
    tags text[] COLLATE pg_catalog."default" NOT NULL DEFAULT '{}'::text[],
    medium_thumb_url text COLLATE pg_catalog."default" NOT NULL,
    max_thumb_url text COLLATE pg_catalog."default" NOT NULL,
    duration character varying(8) COLLATE pg_catalog."default" NOT NULL,
    views bigint NOT NULL DEFAULT 0,
    likes bigint,
    dislikes bigint,
    comments bigint,
    outlier_score double precision NOT NULL DEFAULT 0,
    CONSTRAINT video_data_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;
-- Index: video_data_channel_id_idx

-- DROP INDEX IF EXISTS yt_data.video_data_channel_id_idx;

CREATE INDEX IF NOT EXISTS video_data_channel_id_idx
    ON yt_data.video_data USING btree
    (channel_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: video_data_published_idx

-- DROP INDEX IF EXISTS yt_data.video_data_published_idx;

CREATE INDEX IF NOT EXISTS video_data_published_idx
    ON yt_data.video_data USING btree
    (date_published DESC NULLS FIRST)
    TABLESPACE pg_default;
-- Index: video_data_views_desc_idx

-- DROP INDEX IF EXISTS yt_data.video_data_views_desc_idx;

CREATE INDEX IF NOT EXISTS video_data_views_desc_idx
    ON yt_data.video_data USING btree
    (views DESC NULLS FIRST)
    TABLESPACE pg_default;