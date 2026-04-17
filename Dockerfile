FROM sagemath/sagemath:latest

USER root

RUN mkdir -p /var/lib/apt/lists/partial && chmod -R 755 /var/lib/apt/lists

ENV DEBIAN_FRONTEND=noninteractive

# Install system deps for Python wheels if needed
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
