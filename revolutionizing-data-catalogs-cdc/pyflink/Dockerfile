FROM flink:1.20.1

# Install Python
RUN apt-get update -y && \
apt-get install -y python3 python3-pip python3-dev && \
rm -rf /var/lib/apt/lists/*

# Ensure python command points to python3
RUN ln -s /usr/bin/python3 /usr/bin/python



# # install Java & updates
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y ant && \
    apt-get clean;

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64

WORKDIR /opt/flink
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY download_libs.sh .
RUN chmod +x ./download_libs.sh && ./download_libs.sh

COPY ./usr_jobs/ ./usr_jobs/
RUN cp /opt/flink/opt/flink-python-1.20.1.jar /opt/flink/lib/