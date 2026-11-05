FROM python:3.11-slim-bookworm
RUN pip install --no-cache-dir pytest==8.3.3 Flask==3.0.3 grpcio==1.66.2 protobuf==5.28.3
WORKDIR /src
ENTRYPOINT ["python", "-m", "pytest", "-q", "-p", "no:cacheprovider"]
