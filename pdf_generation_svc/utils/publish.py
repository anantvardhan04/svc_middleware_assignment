import pika


def publish_message(exchange, body):
    # Define the connection parameters to establish a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Publish a message using default exchange
    channel.basic_publish(exchange=exchange, routing_key="pdf_success", body=body)

    # Close the connection
    connection.close()
