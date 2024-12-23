from utils.consume import Consumer


queue = ["notification-service2-queue", "notification-service2-pdf-queue"]
consumer = Consumer()

consumer.consume_message(queue)
