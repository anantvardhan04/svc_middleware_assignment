import pika


def publish_message(queue, body):
    # Define the connection parameters to establish a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Define a queue
    channel.queue_declare(queue=queue)

    # Publish a message using default exchange
    channel.basic_publish(exchange="", routing_key=queue, body=body)

    # Close the connection
    connection.close()
