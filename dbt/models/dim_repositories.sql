{{ config(materialized='table') }}

-- Extracts unique repository information from the nested JSON
SELECT DISTINCT
    CAST(raw_json->'base'->'repo'->>'id' AS BIGINT) AS repo_id,
    CAST(raw_json->'base'->'repo'->>'full_name' AS VARCHAR) AS repo_name,
    CAST(raw_json->'base'->'repo'->>'html_url' AS VARCHAR) AS repo_url,
    CAST(raw_json->'base'->'repo'->>'description' AS TEXT) AS repo_description
FROM raw_github_data.pull_requests
WHERE raw_json->'base'->'repo'->>'id' IS NOT NULL