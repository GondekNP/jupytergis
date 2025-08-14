# FROM mambaorg/micromamba:latest
FROM quay.io/condaforge/mambaforge

# Create a fresh conda environment for jupytergis dev 
RUN mamba create --name jupytergis_dev -c conda-forge pip "nodejs<22" qgis -y

# Activate the conda environment, using micromamba's env activation 
# https://micromamba-docker.readthedocs.io/en/latest/quick_start.html#running-commands-in-dockerfile-within-the-conda-environment
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Copy JavaScript project files needed for jlpm install
COPY package.json yarn.lock lerna.json nx.json ./
COPY packages/ packages/

# Install development dependencies with dev-install script
COPY requirements-build.txt requirements-build.txt
COPY python/ python/

# Run dev-install script to set up the environment
COPY scripts/dev-install.py scripts/dev-install.py

## TODO: This works properly when run post-install, manually, but not when run in the Dockerfile
# RUN python scripts/dev-install.py --target-path .

# Expose JupyterLab port
ENV JUPYTER_PORT=8888
EXPOSE $JUPYTER_PORT

# Copy other src code into the container (last, to avoid cache invalidation for development changes)
COPY . .