from create_data import createData, create_kafka_topic

# Example usage
bootstrap_servers = ['broker:39092']  # Replace with your Kafka broker(s)
topic_name = 'ml_data'
tickers = ["AMZN", "AAPL", "MSFT", "GOOGL", "TSLA"]
num_days = 20
start_date='2022-01-01'
num_partitions = 3
replication_factor = 1

create_kafka_topic(bootstrap_servers, topic_name, num_partitions, replication_factor)

createData(topic_name, "Produce", tickers, num_days, start_date)