
```markdown
# TeleMedica ETL Pipeline

This project is a lightweight, containerized ETL pipeline designed for ingesting, transforming, validating, and serving healthcare data for BI consumption. Built with Apache Airflow, PostgreSQL, and Pgweb — it's optimized for rapid development and production-readiness.

---

## 🔧 Project Structure

telemedica_etl/
│
├── dags/
│ ├── etl_dag.py # Simple pandas DAG
│ ├── spark_patient_dag.py #  Spark ETL DAG
│ ├── transform_and_load.py # Pandas transformation logic
│ └── sample_patient.json # Example input data
│
├── init/
│ ├── init.sql # DB table definitions
│ └── views.sql # View definitions
│
├── Dockerfile.airflow # Airflow custom image
├── docker-compose.yml # Stack orchestration
├── requirements.txt # Python dependencies
└── README.md

JSON/CSV data → Pandas/Spark → Postgres → SQL views. Airflow DAGs orchestrate it all

---

## 🚀 Components

| Component  | Description |
|------------|-------------|
| **PostgreSQL**     | Main relational DB for all patient and treatment data |
| **Apache Airflow** | Orchestrates data ingestion, transformation, validation |
| **Pgweb**          | Web-based SQL query UI (runs on port `8081`) |

---

## 🐳 Running the Project

```bash
docker-compose up -d
````

* Airflow UI: [http://localhost:8080](http://localhost:8080) (user: `admin` / pass: `admin`)
* Pgweb SQL UI: [http://localhost:8081](http://localhost:8081)

---

## 📊 BI Accessibility

We expose ** views** to support common queries like:

```sql
SELECT * FROM metformin_patients_q2_2023;
```

* Views can be refreshed  via Airflow DAGs.
* Only **de-identified or masked** views are exposed to BI users.

### Connecting Power BI / Tableau

Use the `bi_user` Postgres role:

* Host: `localhost`
* Port: `5432`
* DB: `medica`
* User: `bi_user`
* Password: *(as set)*

---

## ✅ Data Quality & Validation

* **Validation DAG** checks:

  * sample validation is added

---
---

## 🔄 Handling Multiple Data Sources with Schema Differences

This ETL pipeline is built to support ingestion from multiple sources (e.g., hospitals, clinics, devices) — each with their own schema variations and data formats.

### 🛠 Strategy

- ✅ **Schema Mappings Config**: Maintain a `schema_mappings.yaml` to define field mappings, type conversions, and code normalization per source.
- ✅ **Pluggable Parsers**: Implement source-specific parser classes to handle field-level transformations and quirks.
- ✅ **Canonical Normalization**: Standardize fields (e.g., gender, dates) into a unified schema using Spark.
- ✅ **Validation Layer**: Add data quality checks (nulls, type mismatches, allowed values) before loading.
- ✅ **Staging Tables**: Load raw transformed data into `staging_<source>` tables to isolate errors.
- ✅ **Final Clean Load**: Move validated records into production-ready fact and dimension tables.

### 💡 Benefits

- 📦 **Easy to Add New Sources** — just create a config + parser.
- 🔍 **Full Traceability** — each step is logged and auditable.
- 🚫 **Fault Isolation** — malformed data doesn’t block the pipeline.
- 🔁 **Scalable & Modular** — built for growing data diversity.


## 🔐 Security & Compliance

* **Masked Views**: PII fields like name/email are masked before BI exposure.

* **DB Roles**: `bi_user` has read-only access to pre-approved views/tables.

* **Future-proofing**:

  ```sql
  GRANT SELECT ON ALL TABLES IN SCHEMA public TO bi_user;
  ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO bi_user;
  ```

* GDPR/HIPAA best practices:

  * Audit logging (planned)
  * Anonymization strategy
  * Data retention policies (planned via Airflow cleanup DAG not implemented)

---

## ⚡ Scalability & Performance

* PostgreSQL indexes on critical fields (e.g `patient_id`)
* Partitioning strategies for large temporal tables (e.g., `treatments`)
* Materialized views to offload common aggregations
* Support for future migration to big data analytics(Pyspark sample dag is added for presentation purpose)

---

## 🛠️ Development Notes

* Airflow DAGs are modular and follow `extract -> transform -> validate -> load` pattern.
* Custom validation or ingestion logic can be added to `dags/`.
* Init SQL scripts auto-run via `/init/` folder when DB container starts.

---

## 🧪 Future Enhancements

* Full test suite with `pytest` or `Great Expectations`
* Role-based column-level security
* REST API for data access
* Alerts on data quality failures (Slack/email)
* Incremental ETL support for large-scale ingestion
