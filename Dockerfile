# Dockerfile — sagemath base, clone ecdata/eclib/lmfdb, copy cremona DB if present
FROM sagemath/sagemath:latest

USER root

# Install tools needed for cloning, extracting, and building small Python pieces
RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget ca-certificates tar build-essential pkg-config python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

# Clone John Cremona repos and LMFDB
RUN git clone https://github.com/JohnCremona/ecdata.git /opt/ecdata || true
RUN git clone https://github.com/JohnCremona/eclib.git /opt/eclib || true
RUN git clone https://github.com/LMFDB/lmfdb.git /opt/lmfdb || true

# If ecdata contains a cremona DB directory or tarball, copy/extract it into Sage DB dir
RUN mkdir -p /usr/local/share/sage/databases && \
    if [ -d /opt/ecdata/cremona ]; then \
        cp -a /opt/ecdata/cremona /usr/local/share/sage/databases/cremona; \
    elif [ -f /opt/ecdata/cremona.tar.gz ]; then \
        tar -xzf /opt/ecdata/cremona.tar.gz -C /usr/local/share/sage/databases; \
    else \
        echo "No cremona dir/tarball in ecdata; full DB may require sage -i or external tarball"; \
    fi && \
    chmod -R a+rX /usr/local/share/sage/databases/cremona || true

# Install eclib if it exposes a Python package (best-effort)
RUN sage -python -m pip install --no-cache-dir /opt/eclib || true

# Install LMFDB Python requirements (best-effort). LMFDB has many optional deps;
# we install core packages commonly needed for local development.
RUN sage -python -m pip install --no-cache-dir \
    numpy pandas tqdm scikit-learn flask pymongo gunicorn \
    || true

# Optional: install lmfdb as a local package for development (editable)
# This will not run if lmfdb has no setup.py/pyproject; it's best-effort.
RUN if [ -f /opt/lmfdb/setup.py ] || [ -f /opt/lmfdb/pyproject.toml ]; then \
      sage -python -m pip install --no-cache-dir -e /opt/lmfdb || true; \
    else \
      echo "LMFDB repo has no installable package metadata; use it as source in /opt/lmfdb"; \
    fi

# copy and extract prebuilt cremona DB into Sage DB dir
COPY cremona_db.tar.gz /tmp/cremona_db.tar.gz

# Extract it into Sage’s database directory
RUN mkdir -p /usr/local/share/sage/databases && \
    tar -xzf /tmp/cremona_db.tar.gz -C /usr/local/share/sage/databases && \
    rm /tmp/cremona_db.tar.gz && \
    chmod -R a+rX /usr/local/share/sage/databases/cremona

ENV SAGE_DATABASES=/usr/local/share/sage/databases
ENV PYTHONNOUSERSITE=1

# Project workspace
WORKDIR /workspace
RUN mkdir -p /workspace && chmod -R a+rX /workspace

VOLUME ["/workspace"]
EXPOSE 8888

# Start JupyterLab via Sage's Python
CMD ["bash", "-lc", "sage -python -m jupyterlab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='acsc2026'"]
