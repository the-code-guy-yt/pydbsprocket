CREATE OR REPLACE PROCEDURE web_api.bulk_insert_video_data(
	IN p_rows yt_data.video_data[],
	OUT row_count integer)
LANGUAGE 'plpgsql'
SECURITY DEFINER
SET search_path = yt_data, pg_temp
AS $BODY$
BEGIN
  INSERT INTO yt_data.video_data (
    id, channel_id, channel_name,
    title, description, date_published,
    tags, medium_thumb_url, max_thumb_url,
    duration, views, likes, dislikes, comments,
    outlier_score
  )
  SELECT DISTINCT
    raw.id, raw.channel_id, raw.channel_name,
    raw.title, raw.description, raw.date_published,
    raw.tags, raw.medium_thumb_url, raw.max_thumb_url,
    raw.duration, raw.views, raw.likes, raw.dislikes, raw.comments,
    raw.outlier_score
  FROM unnest(p_rows) AS raw
    LEFT OUTER JOIN yt_data.video_data as vd
    ON vd.id = raw.id
  WHERE vd.id IS NULL;

  GET DIAGNOSTICS row_count = ROW_COUNT;
  
END;
$BODY$;



--Grant required to use type outside of proc for insert
--Allows referencing of object but not code or contents so safe
GRANT USAGE ON SCHEMA yt_data TO demo_user;

GRANT EXECUTE ON PROCEDURE web_api.bulk_insert_video_data(yt_data.video_data[]) TO demo_user;
