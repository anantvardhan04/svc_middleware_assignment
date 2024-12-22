from utils.consume import Consumer


account_svc_queue = "account_svc"
consumer = Consumer()

consumer.consume_message(account_svc_queue)
