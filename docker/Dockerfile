FROM sagemath/sagemath:latest

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git python3-pip && \
    apt-get clean

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /workspace
COPY . /workspace
