{{ config(materialized='table') }}

-- Extracts unique user information from the nested JSON
SELECT DISTINCT
    CAST(raw_json->'user'->>'id' AS BIGINT) AS user_id,
    user_login AS username,
    CAST(raw_json->'user'->>'type' AS VARCHAR) AS user_type,
    CAST(raw_json->'user'->>'site_admin' AS BOOLEAN) AS is_site_admin
FROM raw_github_data.pull_requests
WHERE raw_json->'user'->>'id' IS NOT NULL