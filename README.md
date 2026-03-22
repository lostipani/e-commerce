# e-commerce Spark analysis orchestrated by Airflow

## Download data
1. Download the dataset from [this kaggle page](https://www.kaggle.com/datasets/carrie1/ecommerce-data/data).
2. Unzip it in the `data/` folder.

## Notebook mode
1. Set up the Spark cluster `docker compose --profile=notebook up -d`.
2. Browse to `http://127.0.0.1:8888/tree/notebooks` and happy analysis.

## Cluster mode
* Spark master and worker nodes to run jobs.
* Airflow to orchestrate and schedule Spark jobs.

1. Launch it `docker compose --profile=cluster up -d`

### Spark
* Standalone cluster mode: master and worker node(s)

### Airflow
The architecture chosen here is the distributed one but simplified, in which the Scheduler runs both the CeleryExecutor and the DAG processor, whereas separated containers are in place for a Celery Worker node and the API server.

The metadata are persisted to a PostgreSQL instance and Redis serves as the Celery backend.

Run 
```bash
export AIRFLOW_UID=$(id -u)
export AIRFLOW_WWW_USER_USERNAME=airflow
export AIRFLOW_WWW_USER_PASSWORD=airflow
export AIRFLOW_PROJ_DIR=./airflow/
```
Launch
```bash
docker compose --project-directory airflow up --build
```

### Deps
|            | python | java | spark | pyspark | airflow |
|------------|--------|------|-------|---------|---------|
| my-spark   | 3.12   | 11   | 3.5.5 | 3.5.5   | /       |
| my-airflow | 3.12   | 17   | 3.5.5 | 3.5.5   | 2.9.2   |