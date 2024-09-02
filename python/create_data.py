import time
import logging
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from finance_data import get_stock_data_json
import json
from kafka.errors import TopicAlreadyExistsError

# Configure logging
logging.basicConfig(
    filename='sensor_log.txt',  # Log file name
    level=logging.INFO,         # Log level
    format='%(asctime)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)


producer = KafkaProducer(bootstrap_servers='broker:39092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
def log_sensor_data():
        datum = get_stock_data_json()
        for x in datum:
            data = x
            log_message = (
                f"Ticker: {data['Ticker']}, "
                f"Date: {data['Date']}, "
                f"Open: {data['Open']:.2f}, "
                f"High: {data['High']:.2f}, "
                f"Low: {data['Low']:.2f}, "
                f"Close: {data['Close']:.2f}, "
                f"Volume: {data['Volume']}"
            )
        
            logging.info(log_message)
            time.sleep(1) 
    
def sendToTopic(topic_name, ticker, num_days, start_date):
    data = get_stock_data_json(ticker, num_days, start_date)
    for x in data:
        producer.send(topic_name, x)
        print(x)
        time.sleep(1)
        
    print(f"Items of length {len(data)} added to the topic.")
    
def createData(topic_name, type, ticker, num_days, start_date):
    if type == "Log":
        log_sensor_data()
    else:
        sendToTopic(topic_name, ticker, num_days, start_date)
        
def create_kafka_topic(bootstrap_servers, topic_name, num_partitions=1, replication_factor=1):
    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers,
        client_id='create_topic_client'
    )
    
    # Check if the topic already exists
    existing_topics = admin_client.list_topics()

    if topic_name in existing_topics:
        print(f"Topic '{topic_name}' already exists.")
    else:
        topic_list = [NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
        
        try:
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print(f"Topic '{topic_name}' created successfully.")
        except TopicAlreadyExistsError:
            print(f"Topic '{topic_name}' already exists (caught in exception).")
        except Exception as e:
            print(f"Failed to create topic '{topic_name}'. Error: {str(e)}")
        finally:
            admin_client.close()