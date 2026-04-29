# docker/Dockerfile
FROM mambaorg/micromamba:1.4.0

ARG USER=star
ARG UID=1000
ARG CONDA_ENV=star-env
ARG PYTHON_VERSION=3.12

ENV PATH=/opt/conda/bin:$PATH
SHELL ["/bin/bash", "-lc"]

# Ensure we run package installation as root
USER root

# Minimal system deps needed for conda packages and pip wheels
RUN mkdir -p /var/lib/apt/lists/partial \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    curl \
    git \
    build-essential \
    cmake \
    pkg-config \
    libffi-dev \
    libssl-dev \
 && rm -rf /var/lib/apt/lists/*

# Create conda env with Python 3.10 and install TDA libs from conda-forge
RUN micromamba create -y -n ${CONDA_ENV} python=${PYTHON_VERSION} -c conda-forge \
    numpy scipy pandas \
    gudhi=3.12.0 ripser=0.6.14 persim=0.3.8 \
 && micromamba clean --all --yes

# Make the conda env the default for subsequent RUN steps
ENV CONDA_DEFAULT_ENV=${CONDA_ENV}
ENV CONDA_PREFIX=/opt/conda/envs/${CONDA_ENV}
ENV PATH=${CONDA_PREFIX}/bin:${PATH}

# Create non-root user only if it doesn't already exist
# If UID 1000 is already taken, create the user without specifying UID
RUN if id -u ${USER} >/dev/null 2>&1; then \
      echo "user ${USER} already exists"; \
    else \
      if id -u ${UID} >/dev/null 2>&1; then \
        echo "UID ${UID} already taken, creating ${USER} without explicit UID"; \
        useradd -m ${USER}; \
      else \
        useradd -m -u ${UID} ${USER}; \
      fi; \
    fi

WORKDIR /home/${USER}/app
COPY . /home/${USER}/app
# chown will succeed whether the user existed or was just created
RUN chown -R ${USER}:${USER} /home/${USER}/app

# Switch to non-root user for installing Python package and runtime
USER ${USER}

# Upgrade pip and install package in editable mode with extras inside the conda env
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install --no-cache-dir -e ".[dev,tda]"

# Ensure PYTHONPATH is defined (avoids undefined-var warnings)
ENV PYTHONPATH=/home/${USER}/app:$PYTHONPATH
WORKDIR /home/${USER}/app

# Default verification command (override in CI)
CMD ["bash", "-lc", "python -c \"import sys, gudhi, ripser; print('py', sys.version.split()[0], 'gudhi', gudhi.__version__, 'ripser', ripser.__version__)\""]
