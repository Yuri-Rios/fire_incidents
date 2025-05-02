FROM python:3.10

# Airflow envs
ENV AIRFLOW_HOME=/opt/airflow
ENV PYSPARK_PYTHON=python3

# Basic Installs + Adoptium OpenJDK 11 
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
        build-essential \
        libsasl2-dev \
        libffi-dev \
        libpq-dev && \
    curl -L -o /tmp/openjdk.tar.gz https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.23+9/OpenJDK11U-jdk_x64_linux_hotspot_11.0.23_9.tar.gz && \
    mkdir -p /opt/java/openjdk && \
    tar -xzf /tmp/openjdk.tar.gz -C /opt/java/openjdk --strip-components=1 && \
    rm /tmp/openjdk.tar.gz && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="$JAVA_HOME/bin:$PATH"

# Python packages
RUN pip install --upgrade pip && \
    pip install \
        pandas \
        pyspark==3.4.1 \
        apache-airflow[postgres]==2.7.3 \
        flask-session==0.4.0

# Creates Airflow dir and init
RUN mkdir -p $AIRFLOW_HOME && airflow db init || true

WORKDIR $AIRFLOW_HOME

EXPOSE 8080

# Runs scheduler and webserver
CMD ["sh", "-c", "airflow scheduler & airflow webserver -p 8080"]
