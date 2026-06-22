import json
import requests
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Define the default arguments for the DAG
default_args = {
    'owner': 'data_engineer',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# Task 1: Connect to the GitHub API and fetch recent pull requests
def extract_github_data(**kwargs):
    repo = "apache/superset" # We are analyzing the Superset open-source project!
    url = f"https://api.github.com/repos/{repo}/pulls?state=all&per_page=100"
    
    response = requests.get(url)
    response.raise_for_status() # Fail the task if the API limit is hit
    
    prs = response.json()
    
    # Save the raw JSON to Airflow's temporary memory (XCom) to pass to the next task
    kwargs['ti'].xcom_push(key='raw_prs', value=prs)
    print(f"Successfully extracted {len(prs)} pull requests from {repo}.")

# Task 2: Load the data into our local PostgreSQL database
def load_data_to_postgres(**kwargs):
    # Retrieve the data from the previous task
    prs = kwargs['ti'].xcom_pull(key='raw_prs', task_ids='extract_github_data')
    
    import psycopg2
    # Connect directly to our Docker Postgres container
    conn = psycopg2.connect(
        host="postgres", 
        database="airflow",
        user="airflow",
        password="airflow",
        port="5432"
    )
    cursor = conn.cursor()

    # Create the table inside our raw_github_data schema
    create_table_query = """
    CREATE TABLE IF NOT EXISTS raw_github_data.pull_requests (
        id BIGINT PRIMARY KEY,
        number INT,
        title TEXT,
        state VARCHAR(50),
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        user_login VARCHAR(100),
        raw_json JSONB
    );
    """
    cursor.execute(create_table_query)

    # Insert the records. If the ID already exists, update it (Upsert logic).
    insert_query = """
    INSERT INTO raw_github_data.pull_requests (id, number, title, state, created_at, updated_at, user_login, raw_json)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE SET 
        state = EXCLUDED.state, 
        updated_at = EXCLUDED.updated_at,
        raw_json = EXCLUDED.raw_json;
    """

    count = 0
    for pr in prs:
        cursor.execute(insert_query, (
            pr.get('id'),
            pr.get('number'),
            pr.get('title'),
            pr.get('state'),
            pr.get('created_at'),
            pr.get('updated_at'),
            pr.get('user').get('login') if pr.get('user') else 'unknown',
            json.dumps(pr) # We store the whole JSON payload so we can extract more fields later in dbt!
        ))
        count += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Successfully loaded {count} records into PostgreSQL.")

# Define the DAG sequence
with DAG(
    'github_to_postgres_pipeline',
    default_args=default_args,
    schedule_interval='@daily', # Run once a day automatically
    catchup=False,
    description='Extract GitHub PRs and load to Postgres'
) as dag:

    # Define Task 1
    extract_task = PythonOperator(
        task_id='extract_github_data',
        python_callable=extract_github_data,
        provide_context=True
    )

    # Define Task 2
    load_task = PythonOperator(
        task_id='load_data_to_postgres',
        python_callable=load_data_to_postgres,
        provide_context=True
    )

    # Set the dependency order (Extract MUST run before Load)
    extract_task >> load_task