# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set environment variables for bytecode compilation and link mode
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Define build arguments
ARG USERNAME
ARG UID
ARG GID

# Set environment variable for the user
ENV USER=$USERNAME

# Set the working directory
WORKDIR /home/$USER

# Create a group and user with specified GID and UID
RUN groupadd --gid $GID $USER && \
    useradd --uid $UID --gid $GID --create-home --home-dir /home/$USER $USER

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/home/$USER/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /home/$USER
RUN --mount=type=cache,target=/home/$USER/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/home/$USER/.venv/bin:$PATH"

# Switch to the newly created user
USER $USER

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Set command
CMD ["bash"]
