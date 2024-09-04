from kafka import KafkaConsumer
from cockroach_connect import getConnection
import logging
from datetime import datetime
import re
import json

# Setup logging
logger = logging.getLogger('cockroachdb_kafka')
logger.setLevel(logging.INFO)  # Set to INFO level

# Get mandatory connection
conn = getConnection(True)

def sanitize_text(text):
    if text is None:
        return None
    
    return re.sub(r'[^\x20-\x7E]', '', text)

def setup_database():
    """Create the table if it does not exist."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS stock_data (
                        id SERIAL PRIMARY KEY,
                        ticker VARCHAR(10),
                        date DATE,
                        open FLOAT,
                        high FLOAT,
                        low FLOAT,                                                                                                                                                                                                          
                        close FLOAT,
                        volume BIGINT,
                        dividends FLOAT,
                        stock_splits FLOAT
                )
            """)
            conn.commit()
            logger.info("Table created or already exists.")
    except Exception as e:
        logger.error(f"Problem setting up the database: {e}")

def cockroachWrite(event):
    """Write Kafka event to the stock_data table in the database."""
    try:
        # Read and convert data from event
        data = json.loads(event.value)
            
        # Extract values from JSON data
        ticker = data['Ticker']
        date_str = data['Date']
        open_price = data['Open']
        high = data['High']
        low = data['Low']
        close = data['Close']
        volume = data['Volume']
        dividends = data['Dividend']  # Use 0.0 as a default if not present
        stock_splits = data['Stock Split']  # Use 0.0 as a default if not present

        # Check for None values and log if necessary
        if not all([ticker, date_str, open_price, high, low, close, volume]):
            logger.error(f"Missing required stock data fields in JSON: {data}")

        # Parse date string to date object
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Insert into the database
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO stock_dat                                                                                                                                                                                         a (ticker, date, open, high, low, close, volume, dividends, stock_splits) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (ticker, date, open_price, high, low, close, volume, dividends, stock_splits))
        conn.commit()
        logger.info(f"Stock data for {ticker} on {date_str} inserted successfully.")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
    except KeyError as e:
        logger.error(f"Missing key in JSON data: {e}")
    except Exception as e:
        logger.error(f"Problem writing to database: {e}")

# Initialize Kafka consumer
consumer = KafkaConsumer(
    "ml_data",
    bootstrap_servers=['broker:39092'], 
    auto_offset_reset='earliest'
)

def test(event):
    data = json.loads(event.value)
    print(data)
            

# Setup the database once
setup_database()

# Process messages
for msg in consumer:
    cockroachWrite(msg)
    logger.info("Msg seen.") 
