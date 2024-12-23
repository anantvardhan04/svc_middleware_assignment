from utils.consume import Consumer


account_svc_queue = "notification-service1-queue"
consumer = Consumer()

consumer.consume_message(account_svc_queue)
