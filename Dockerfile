    # Use a lightweight base image
FROM python:3.9-slim-buster

# Install required packages including Python3 and any other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libprotobuf-dev \
    protobuf-compiler \
    libnl-3-dev \
    libnl-route-3-dev \
    libseccomp-dev \
    flex \
    bison \
    pkg-config \
    python3 \
    python3-pip

# Install nsjail
RUN git clone https://github.com/google/nsjail.git /opt/nsjail && \
    cd /opt/nsjail && \
    make && \
    cp nsjail /usr/local/bin/nsjail

# Copy application files
WORKDIR /app
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY templates/ templates/

COPY nsjail /opt/nsjail
WORKDIR /opt/nsjail
RUN make
RUN cp nsjail /usr/local/bin/nsjail

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Set the entrypoint
CMD ["python3", "app.py"]
