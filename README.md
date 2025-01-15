# data_analysis
# Retail Analytics & Recommendation System

## Overview
This system loads retail purchase data, performs data analysis (top-selling products, average spending), clusters customers into segments (High Spenders, Frequent Buyers, etc.), and provides product recommendations using collaborative filtering.

## Features
1. **Data Generation**: Creates synthetic data if not provided.
2. **Data Loading & Validation**: Ensures schema correctness using Pandas.
3. **Analysis**: Finds top-selling products/categories, and visualizes results.
4. **Clustering**: Groups customers via K-Means based on spending habits.
5. **Recommendation**: Collaborative filtering with Surprise library.
6. **Reporting**: Generates an HTML page summarizing insights, clusters, and recommendations.
7. **Security**: Includes AES-256 encryption examples and RBAC stubs.
8. **Logging**: Structured logging with unique correlation IDs.
9. **Filtering**: Allows date/category-based filtering.
10. **Production-Ready**: Dockerfile, integration tests, potential scaling with Kubernetes.

## Installation & Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/retail-analytics.git
    ```
2. Install dependencies:
    ```bash
    cd retail-analytics
    pip install -r requirements.txt
    ```
3. Set environment variables (if needed):
    ```bash
    export SECRET_KEY='some_32_char_random_string'
    export DB_HOST='localhost'  # if using a DB
    ...
    ```
4. Run the program:
    ```bash
    python src/main.py
    ```
5. (Optional) Build & Run Docker container:
    ```bash
    docker build -t retail-analytics .
    docker run -p 8000:8000 retail-analytics
    ```

## Testing
- Run unit and integration tests:
    ```bash
    pytest tests/
    ```

## Usage
- The PDF report, once generated, will be saved as `RetailAnalyticsReport.pdf` in the project root.
- Logs are printed to stdout; configure them using `logging_config.yaml`.

## Security & Logging
- AES-256 encryption example in `security.py`.
- Structured JSON logging in `logging_utils.py`.

## Next Steps
- Implement real-time data ingestion with Kafka.
- Integrate advanced RFM or churn prediction methods.
- Deploy to a Kubernetes cluster for auto-scaling.
