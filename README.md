* Fetch [my spark project](https://github.com/lostipani/spark) and launch a containerised Spark cluster:
```bash
docker compose up
```
* Once running launch the jupyter notebook on the spark-master node
```bash
docker exec -it e-commerce-spark-master-1 bash -c "jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --notebook-dir=/app"
```