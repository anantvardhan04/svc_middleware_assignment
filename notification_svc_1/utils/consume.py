import pika


class Consumer:
    def consume_message(self, queue):
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        channel.queue_declare(queue)
        channel.basic_consume(
            queue=queue, auto_ack=True, on_message_callback=self.callback
        )
        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(f" [x] {body}")
