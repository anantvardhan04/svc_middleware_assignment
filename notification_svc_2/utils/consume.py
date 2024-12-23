import pika


class Consumer:
    def consume_message(self, queue):
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        for q in queue:
            channel.basic_consume(
                queue=q, auto_ack=True, on_message_callback=self.callback
            )
        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(f" [x] {body}")
