from utils.consumer import Consumer

consumer = Consumer()
queue = "pdf-generator-queue"
consumer.consume_message(queue)
