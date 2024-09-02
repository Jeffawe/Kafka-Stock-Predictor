# Data Pipeline and Machine Learning Model Deployment Using Kafka, CockroachDB, and Streamlit

This repository provides a complete data pipeline setup that ingests financial data from Yahoo Finance, streams it into Kafka, stores and processes it in CockroachDB, trains a machine learning model, and deploys the model using Streamlit. The entire setup is containerized using Docker, enabling easy deployment and scalability.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [File Structure](#file-structure)
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

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
