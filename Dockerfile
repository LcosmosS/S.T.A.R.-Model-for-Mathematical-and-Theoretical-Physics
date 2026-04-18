# — sagemath base, install build tools, install Cremona DB, clone repos
FROM sagemath/sagemath:latest

USER root

# install minimal build tools required by sage -i database_cremona_ellcurve
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential make wget ca-certificates git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

# install full Cremona DB (this downloads/builds data; may take time and disk)
RUN sage -i database_cremona_ellcurve

# clone John Cremona repos (optional; you can mount your local copies instead)
RUN git clone https://github.com/JohnCremona/eclib.git /opt/eclib || true && \
    git clone https://github.com/JohnCremona/ecdata.git /opt/ecdata || true

# install eclib into Sage's python if it provides a Python package (adjust if needed)
RUN sage -python -m pip install --no-cache-dir /opt/eclib || true

# project deps (adjust list to your needs)
RUN sage -python -m pip install --no-cache-dir numpy pandas tqdm scikit-learn gudhi ripser

WORKDIR /workspace
VOLUME ["/workspace"]
EXPOSE 8888

CMD ["bash", "-lc", "sage -python -m jupyterlab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='acsc2026'"]
