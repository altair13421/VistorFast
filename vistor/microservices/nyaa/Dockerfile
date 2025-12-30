FROM archlinux:latest

# Install dependencies
RUN pacman -Sy --noconfirm --needed reflector

# Using reflector for best servers
RUN reflector --latest 5 --sort rate --save /etc/pacman.d/mirrorlist

# Install base-devel and python
RUN pacman -Syu --noconfirm --needed \
    base-devel \
    python \
    python-pip \
    sqlite \
    && pacman -Scc --noconfirm

# Update System and install python build tools
RUN pacman -Syu --noconfirm \
    && pacman -S --noconfirm python-virtualenv \
    python-setuptools python-wheel \
    && pacman -Scc --noconfirm

# Create a non-root user for security (similar to tiangolo's images)
RUN useradd -m -u 1000 -s /bin/bash appuser

WORKDIR /app

# Copy requirements first for better caching
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies as root first
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy application files
COPY ./app /app/app

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
