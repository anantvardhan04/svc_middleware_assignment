from utils.consumer import Consumer

consumer = Consumer()
queue = "pdf_generation"
consumer.consume_message(queue)
