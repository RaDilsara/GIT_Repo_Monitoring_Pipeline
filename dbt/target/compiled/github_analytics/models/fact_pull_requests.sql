

-- The central fact table connecting the action to the dimensions
SELECT
    id AS pr_id,
    number AS pr_number,
    -- Foreign Keys linking to our Dimension tables
    CAST(raw_json->'user'->>'id' AS BIGINT) AS user_id,
    CAST(raw_json->'base'->'repo'->>'id' AS BIGINT) AS repo_id,
    
    -- PR specifics
    title,
    state,
    created_at,
    updated_at,
    CAST(raw_json->>'closed_at' AS TIMESTAMP) AS closed_at,
    CAST(raw_json->>'merged_at' AS TIMESTAMP) AS merged_at,
    CAST(raw_json->>'draft' AS BOOLEAN) AS is_draft,
    CAST(raw_json->>'locked' AS BOOLEAN) AS is_locked
FROM raw_github_data.pull_requests