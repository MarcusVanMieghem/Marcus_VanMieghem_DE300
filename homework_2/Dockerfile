
FROM jupyter/scipy-notebook:latest


WORKDIR /home/jovyan/work


COPY . /home/jovyan/work/


RUN pip install \
    duckdb \
    cassandra-driver \
    cassandra-sigv4 \
    boto3 \
    matplotlib \
    seaborn


USER root
RUN chown -R jovyan:users /home/jovyan/work
USER jovyan


CMD ["start-notebook.sh"]