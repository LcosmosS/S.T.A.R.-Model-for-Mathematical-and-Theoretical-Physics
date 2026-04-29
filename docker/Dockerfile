# Use a small base image
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV PATH=/opt/conda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    curl \
    git \
    build-essential \
    cmake \
    pkg-config \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV MINICONDA_VERSION=py310_23.9.0-1
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /opt/conda \
    && rm /tmp/miniconda.sh \
    && /opt/conda/bin/conda clean -afy

# Create conda env with Python 3.10 and install TDA libs from conda-forge
# Use explicit Python 3.10 to match gudhi 3.5.1 compatibility
RUN conda config --set channel_priority strict \
    && conda config --add channels conda-forge \
    && conda create -n star-env python=3.10 -y \
    && /opt/conda/bin/conda run -n star-env python -m pip install --upgrade pip setuptools wheel \
    && /opt/conda/bin/conda run -n star-env conda install -y -c conda-forge \
       gudhi=3.5.1 ripser=0.6.2 persim=0.6.0 numpy scipy pandas \
    && /opt/conda/bin/conda clean -afy

# Make the conda env the default for subsequent RUN steps
SHELL ["conda", "run", "-n", "star-env", "/bin/bash", "-lc"]

# Create a non-root user
ARG USER=star
ARG UID=1000
RUN useradd -m -u ${UID} ${USER}

WORKDIR /home/${USER}/app
COPY . /home/${USER}/app
RUN chown -R ${USER}:${USER} /home/${USER}/app

USER ${USER}

# Install package in editable mode with dev extras (inside the conda env)
RUN python -m pip install --no-cache-dir -e ".[dev,tda]"

# Expose a default working directory and entrypoint
ENV PYTHONPATH=/home/${USER}/app:$PYTHONPATH
WORKDIR /home/${USER}/app

# Default command: show python version and installed packages (override in CI)
CMD ["bash", "-lc", "python -V && python -c 'import gudhi, ripser; print(\"gudhi\", gudhi.__version__, \"ripser\", ripser.__version__)'"]
