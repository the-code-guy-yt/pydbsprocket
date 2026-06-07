CREATE OR REPLACE PROCEDURE web_api.get_channel_video_data(
    IN p_channel_id text,
    OUT cur refcursor)
LANGUAGE 'plpgsql'
SECURITY DEFINER
SET search_path = yt_data, pg_temp
AS $BODY$
BEGIN
    -- We open the cursor and the OUT parameter 'cur' holds the pointer to it
    OPEN cur FOR
        SELECT
            id, channel_id, channel_name,
            title, description, date_published,
            tags, medium_thumb_url, max_thumb_url,
            duration, views, likes, dislikes, comments,
            outlier_score
        FROM yt_data.video_data
        WHERE channel_id = p_channel_id
        ORDER BY date_published DESC;
END;
$BODY$;

GRANT EXECUTE ON PROCEDURE web_api.get_channel_video_data(text) TO demo_user;