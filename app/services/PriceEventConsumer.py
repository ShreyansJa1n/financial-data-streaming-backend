from app.services.kafka.KafkaConsumer import KafkaConsumerService

topics = ["price_events"]
consumer_service = KafkaConsumerService(topics)

def handle_price_event(message):
    # Process the price event message
    print(f"Processing price event: {message}")
    # Here you can add logic to store the message in the database or perform other actions

def start_price_event_consumer():
    try:
        print("Starting price event consumer...")
        consumer_service.consume_messages(callback=handle_price_event)
    except KeyboardInterrupt:
        print("Stopping price event consumer...")
    

def stop_price_event_consumer():
    consumer_service.close()
    print("Price event consumer stopped.")