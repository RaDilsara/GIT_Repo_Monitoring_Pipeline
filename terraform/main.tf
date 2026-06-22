terraform {
  required_providers {
    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "1.21.0"
    }
  }
}

# The variables are completely empty placeholders now!
variable "pg_user" {
  description = "Database username"
  type        = string
}

variable "pg_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "pg_db" {
  description = "Database name"
  type        = string
}

# Connect using the empty variables (Terraform fills them using terraform.tfvars)
provider "postgresql" {
  host            = "localhost"
  port            = 5432
  database        = var.pg_db
  username        = var.pg_user
  password        = var.pg_password
  sslmode         = "disable"
  connect_timeout = 15
}

resource "postgresql_schema" "raw_data" {
  name  = "raw_github_data"
  owner = var.pg_user
}

resource "postgresql_schema" "analytics" {
  name  = "analytics"
  owner = var.pg_user
}