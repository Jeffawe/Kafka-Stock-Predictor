from kafka import KafkaConsumer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import json
import joblib
import random
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

def get_data_from_kafka(sample_size=1500, max_messages=2000):
    # Initialize Kafka consumer
    consumer = KafkaConsumer(
        "ml_data",
        bootstrap_servers=['broker:39092'], 
        auto_offset_reset='earliest'
    )

    # Initialize an empty list to store the consumed messages
    data_list = []

    # Consume messages from Kafka
    for message in consumer:
        data_list.append(json.loads(message.value))
        
        # Stop consuming if we reach the maximum number of messages
        if len(data_list) >= sample_size:
            break
        
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data_list)
    
    print(df)
    
    return df


def train_pipeline():
    df = get_data_from_kafka()

        # Define features and target
    X = df[['Ticker', 'Open', 'High', 'Low', 'Volume']]
    y = df['Close']

    # Define preprocessing steps: One-Hot Encoding for categorical 'Ticker' feature
    preprocessor = ColumnTransformer(
        transformers=[
            ('ticker', OneHotEncoder(handle_unknown='ignore'), ['Ticker'])
        ],
        remainder='passthrough'  # Keep all other columns unchanged
    )

    # Create the pipeline with preprocessing and model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', LinearRegression())
    ])

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the pipeline
    pipeline.fit(X_train, y_train)

    # Save the pipeline
    joblib.dump(pipeline, 'stock_price_pipeline.pkl')

    # Evaluate the pipeline
    score = pipeline.score(X_test, y_test)
    return pipeline, score

train_pipeline()

