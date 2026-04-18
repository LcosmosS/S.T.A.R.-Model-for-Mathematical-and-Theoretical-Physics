# Dockerfile — use official Sage image, install Cremona DB and your repos
FROM sagemath/sagemath:latest

# install system tools you may need (git, wget)
USER root
RUN apt-get update && apt-get install -y --no-install-recommends git wget && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

# install full Cremona DB (runs inside the container's Sage)
RUN sage -i database_cremona_ellcurve

# clone and install eclib and ecdata (adjust if you prefer to mount)
RUN git clone https://github.com/JohnCremona/eclib.git /opt/eclib && \
    git clone https://github.com/JohnCremona/ecdata.git /opt/ecdata

# If eclib has a Python install step, install it into Sage's python
RUN sage -python -m pip install --no-cache-dir /opt/eclib || true

# Python deps for your project (adjust list)
RUN sage -python -m pip install --no-cache-dir numpy pandas tqdm scikit-learn gudhi ripser

WORKDIR /workspace
VOLUME ["/workspace"]
EXPOSE 8888

CMD ["bash", "-lc", "sage -python -m jupyterlab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='acsc2026'"]
