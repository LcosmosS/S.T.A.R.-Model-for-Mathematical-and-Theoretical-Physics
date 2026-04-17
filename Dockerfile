FROM sagemath/sagemath:9.8

USER root
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git wget libgomp1 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir \
    numpy pandas matplotlib seaborn scikit-learn tqdm jupyterlab \
    gudhi ripser

WORKDIR /workspace
COPY . /workspace

EXPOSE 8888

ENV JUPYTER_TOKEN=devtoken

CMD ["sh", "-c", "jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=${JUPYTER_TOKEN}"]
