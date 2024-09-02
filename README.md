# Data Pipeline and Machine Learning Model Deployment Using Kafka, CockroachDB, and Streamlit

This repository provides a complete data pipeline setup that ingests financial data from Yahoo Finance, streams it into Kafka, stores and processes it in CockroachDB, trains a machine learning model, and deploys the model using Streamlit. The entire setup is containerized using Docker, enabling easy deployment and scalability.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Docker Compose Services](#docker-compose-services)
- [Contributing](#contributing)
- [License](#license)

## Overview

The goal of this project is to build a robust data pipeline that seamlessly integrates data ingestion, storage, processing, and machine learning model deployment. This pipeline can be adapted to various use cases requiring real-time data processing and predictive modeling.

## Architecture

The architecture of this data pipeline consists of several key components:

1. **Data Ingestion**: Financial data is fetched from Yahoo Finance using a Python script (`create.py`) and is streamed into Kafka.
2. **Kafka**: A distributed streaming platform used for building real-time data pipelines and streaming applications.
3. **CockroachDB**: A distributed SQL database that stores and processes the streamed data for further use.
4. **Machine Learning**: The `write_to_ml.py` script trains a machine learning model based on the processed data stored in CockroachDB.
5. **Model Deployment**: The trained model is deployed using Streamlit, allowing for interactive data visualization and predictions.

## Prerequisites

Before setting up the pipeline, ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.x](https://www.python.org/downloads/)

### Setup and Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/kafka-cockroachdb-ml-pipeline.git
    cd kafka-cockroachdb-ml-pipeline
    ```

2. **Environment Variables**: Set up necessary environment variables in your `.env` file:

    ```env
    COCKROACH1_DATA_DIR=/path/to/data1
    COCKROACH2_DATA_DIR=/path/to/data2
    COCKROACH3_DATA_DIR=/path/to/data3
    COCKROACH1_CERTS_DIR=/path/to/certs1
    COCKROACH2_CERTS_DIR=/path/to/certs2
    COCKROACH3_CERTS_DIR=/path/to/certs3
    COCKROACH1_HOST=cockroach1
    COCKROACH2_HOST=cockroach2
    COCKROACH3_HOST=cockroach3
    ```

3. **Build and Run Containers**:

    ```bash
    docker-compose up -d
    ```

4. **Run Python Scripts**:

   - Produce data to Kafka:

    ```bash
    python create.py
    ```

   - Connect to CockroachDB and write data:

    ```bash
    python cockroach_connect.py
    python db_writer.py
    ```

   - Train the machine learning model and deploy it:

    ```bash
    python write_to_ml.py
    streamlit run your_streamlit_app.py
    ```

## Docker Compose Services

- **CockroachDB**: Three-node CockroachDB cluster (`cockroach1`, `cockroach2`, `cockroach3`).
- **Kafka**: Kafka brokers (`kafka-1`, `kafka-2`, `kafka-3`), Schema Registry, and Kafka Connect.
- **ksqlDB**: Stream processing with ksqlDB.
- **Streamlit**: Deploys the trained machine learning model.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
