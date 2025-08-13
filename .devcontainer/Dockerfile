FROM mambaorg/micromamba:latest

USER root
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Get the host user's UID and GID (passed as build args)
ARG USER_UID=1000
ARG USER_GID=1000

# Update the user's UID and GID to match the host
RUN groupmod --gid $USER_GID $MAMBA_USER && \
    usermod --uid $USER_UID --gid $USER_GID $MAMBA_USER && \
    chown -R $USER_UID:$USER_GID /home/$MAMBA_USER

USER $MAMBA_USER
WORKDIR /home/$MAMBA_USER

# Create a fresh conda environment for jupytergis dev 
RUN micromamba create --name jupytergis_dev -c conda-forge pip "nodejs<22" qgis -y

# Copy source code and ensure proper ownership
COPY --chown=$MAMBA_USER:$MAMBA_USER . .

# Set shell to use micromamba environment
SHELL ["micromamba", "run", "-n", "jupytergis_dev", "/bin/bash", "-c"]

# Install development dependencies with dev-install script
RUN python scripts/dev-install.py

EXPOSE 8888

CMD ["micromamba", "run", "-n", "jupytergis_dev", "jlpm", "run", "watch"]