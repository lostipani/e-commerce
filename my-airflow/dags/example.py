import pendulum
from datetime import datetime

from airflow.decorators import dag, task
from airflow.providers.apache.spark.operators.spark_submit import (
    SparkSubmitOperator,
)


@dag(
    dag_id="pyspark_chained_jobs",
    schedule=None,
    start_date=pendulum.datetime(2026, 3, 28, tz="UTC"),
    catchup=False,
    tags=["spark", "example"],
)
def pyspark_pipeline():
    """Two chained PySpark jobs using Airflow 3 TaskFlow API."""

    @task()
    def start() -> dict:
        """Prepare shared config/metadata passed downstream."""
        run_date = datetime.now().strftime("%Y-%m-%d")
        print(f"Starting pipeline for {run_date}")
        return {
            "run_date": run_date,
            "input_path": f"s3://bucket/raw/{run_date}",
        }

    @task()
    def end(result: dict) -> None:
        """Log completion after both Spark jobs finish."""
        print(f"Pipeline complete. Last result: {result}")

    # --- PySpark Job 1 (e.g. ingestion / transformation) ---
    job_1 = SparkSubmitOperator(
        task_id="pyspark_job_1",
        application="s3://bucket/jobs/job_1.py",  # path to your PySpark script
        conn_id="spark_default",  # Airflow Spark connection
        application_args=[
            "--date",
            "{{ ds }}",
        ],  # Jinja templating still works
        conf={
            "spark.executor.memory": "4g",
            "spark.executor.cores": "2",
        },
        name="airflow_pyspark_job_1",
    )

    # --- PySpark Job 2 (e.g. aggregation / load) ---
    job_2 = SparkSubmitOperator(
        task_id="pyspark_job_2",
        application="s3://bucket/jobs/job_2.py",
        conn_id="spark_default",
        application_args=["--date", "{{ ds }}"],
        conf={
            "spark.executor.memory": "8g",
            "spark.executor.cores": "4",
        },
        name="airflow_pyspark_job_2",
    )

    # --- Chain: start >> job_1 >> job_2 >> end ---
    config = start()
    job_1.set_upstream(config)  # TaskFlow task feeds into the Spark operator
    job_2.set_upstream(job_1)
    end(job_2.output)  # pass job_2's XCom output to the end task


pyspark_pipeline()
