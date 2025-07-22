FROM ubuntu:latest
echo "Start log summary"
# build/test steps here


RUN echo "Start log summary" && \
    apt-get update && \
    apt-get install -y curl python3 python3-pip && \
    curl -LO "https://storage.googleapis.com/kubernetes-release/release/v1.1.0/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl
RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash && \
    echo "End log summary"