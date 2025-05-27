# Base image with Java pre-installed
FROM openjdk:11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV JAVA_HOME=/usr/local/openjdk-11
ENV PATH="$PATH:/opt/spark/bin"

# Install Python, pip, and system tools
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && apt-get clean

# Install Python packages
RUN pip3 install --no-cache-dir \
    pyspark \
    pandas \
    numpy \
    nltk \
    jupyterlab

# Set working directory
WORKDIR /app

# Download required data files
RUN curl -O https://raw.githubusercontent.com/mosesyhc/de300-2025sp-class/refs/heads/main/agnews_clean.csv && \
    curl -O https://raw.githubusercontent.com/mosesyhc/de300-2025sp-class/refs/heads/main/data_for_svm.csv && \
    curl -O https://raw.githubusercontent.com/mosesyhc/de300-2025sp-class/refs/heads/main/w.csv && \
    curl -O https://raw.githubusercontent.com/mosesyhc/de300-2025sp-class/refs/heads/main/bias.csv

# Copy notebook into the container
COPY DATA_ENG300_HW3_MapReduce_and_Spark.ipynb .

# Download NLTK stopwords
RUN python3 -m nltk.downloader stopwords

# Start Jupyter Lab on container startup
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
