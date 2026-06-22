# GitHub Analytics Data Pipeline

An end-to-end Data Engineering project that extracts GitHub Pull Request data, loads it into a PostgreSQL data warehouse, transforms it using dbt, and visualizes insights using Metabase.

## Architecture

```text
GitHub API
     │
     ▼
 Apache Airflow
     │
     ▼
 PostgreSQL
 (raw_github_data)
     │
     ▼
     dbt
     │
     ▼
 PostgreSQL
  (analytics)
     │
     ▼
  Metabase
 Dashboards
```

## Tech Stack

* Apache Airflow – Workflow orchestration
* PostgreSQL – Data warehouse
* dbt – Data transformation
* Metabase – Data visualization
* Docker Compose – Containerized deployment
* Terraform – Database schema provisioning
* GitHub API – Data source

---

## Project Structure

```text
.
├── airflow/
│   ├── dags/
│   └── plugins/
├── dbt/
│   ├── models/
│   └── profiles.yml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars
├── docker-compose.yml
├── .env
└── README.md
```

---

## Security & Local Setup

### 1. Create Environment Variables

Create a `.env` file in the project root:

```env
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

AIRFLOW_ADMIN=
AIRFLOW_PASSWORD=
```

### 2. Configure Terraform Secrets

Create a `terraform.tfvars` file inside the `terraform/` directory:

```hcl
pg_user     = ""
pg_password = ""
pg_db       = ""
```

> These files are excluded from version control using `.gitignore`.

---

## Getting Started

### Start the Infrastructure

Launch all services:

```bash
sudo docker compose up -d
```

This starts:

* PostgreSQL
* Apache Airflow
* Metabase

---

## Provision Database Schemas

Navigate to the Terraform directory:

```bash
cd terraform
```

Initialize Terraform:

```bash
terraform init
```

Apply infrastructure changes:

```bash
terraform apply
```

This automatically creates the required PostgreSQL schemas.

---

## Run the Data Pipeline

Open Airflow:

```text
http://localhost:8080
```

1. Login using your Airflow credentials.
2. Enable the `github_to_postgres_pipeline` DAG.
3. Trigger manually or wait for the scheduled run.

The pipeline will:

* Extract GitHub Pull Request data
* Load raw records into PostgreSQL
* Store data in the `raw_github_data` schema

---

## Transform Data with dbt

Navigate to the dbt directory:

```bash
cd dbt
```

Load environment variables:

```bash
set -a
source ../.env
set +a
```

Run transformations:

```bash
dbt run
```

This creates analytics-ready tables in the `analytics` schema.

---

## Visualize Data with Metabase

Open Metabase:

```text
http://localhost:3000
```

Configure a PostgreSQL connection using the credentials from your `.env` file.

Create dashboards and reports using:

* SQL Editor
* Query Builder

---

## Example Analytics

The project can generate insights such as:

* Pull Requests by Repository
* Pull Requests by Author
* Average Time to Merge
* Open vs Closed Pull Requests
* Contributor Activity Trends
* Repository Performance Metrics

---

## Workflow Overview

1. Airflow extracts GitHub Pull Request data.
2. Data is loaded into PostgreSQL (`raw_github_data`).
3. dbt transforms raw data into analytics models.
4. Metabase visualizes transformed datasets.
5. Dashboards provide actionable GitHub repository insights.

---

## Future Improvements

* Incremental loading
* CI/CD integration with GitHub Actions
* Data quality testing using dbt tests
* Slack notifications for pipeline failures
* Advanced repository analytics
* Kubernetes deployment

---

