# Dockerfile — build Sage from source, install Cremona DB, Python deps, JupyterLab
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ARG SAGE_VERSION=10.7
ARG SAGE_TARBALL_URL=https://mirrors.mit.edu/sage/src/sage-${SAGE_VERSION}.tar.gz
ENV PATH=/opt/sage-${SAGE_VERSION}/local/bin:$PATH

# system build deps (kept minimal but sufficient for Sage build)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential m4 git wget ca-certificates python3 python3-dev python3-distutils \
    gfortran libssl-dev libffi-dev libgmp-dev libmpfr-dev libmpc-dev \
    libblas-dev liblapack-dev libboost-all-dev libreadline-dev libncurses5-dev \
    libbz2-dev zlib1g-dev liblzma-dev pkg-config curl bzip2 xz-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

# download and extract Sage source
RUN wget -qO sage-src.tar.gz "${SAGE_TARBALL_URL}" && \
    tar -xzf sage-src.tar.gz && \
    rm sage-src.tar.gz

WORKDIR /opt/sage-${SAGE_VERSION}

# build Sage (use all CPUs)
RUN make -j$(nproc)

# install full Cremona database (optional package)
RUN ./sage -i database_cremona_ellcurve

# install Python packages needed by ACSC
RUN ./sage -python -m pip install --no-cache-dir numpy pandas tqdm scikit-learn gudhi ripser

# create workspace and set permissions
WORKDIR /workspace
RUN mkdir -p /workspace && chmod -R a+rX /workspace

EXPOSE 8888

# default command launches JupyterLab via Sage's Python
CMD ["bash", "-lc", "./sage -python -m jupyterlab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='acsc2026'"]
