import pika


def publish_message(exchange, message):
    # Define the connection parameters to establish a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Publish a message using default exchange
    # Declare a fanout exchange
    # Publish a message to the fanout exchange
    channel.basic_publish(exchange=exchange, routing_key="generate_pdf", body=message)

    # Close the connection
    connection.close()
