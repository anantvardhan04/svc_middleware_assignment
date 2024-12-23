import pika

# Define the connection parameters to establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Define exchanges
channel.exchange_declare(
    exchange="account.created", exchange_type="fanout", durable=True
)

channel.exchange_declare(exchange="pdf.request", exchange_type="direct", durable=True)

channel.exchange_declare(exchange="pdf.generated", exchange_type="direct", durable=True)

# Define a queue
channel.queue_declare(queue="notification-service1-queue", durable=True)
channel.queue_declare(queue="notification-service2-queue", durable=True)
channel.queue_declare(queue="pdf-generator-queue", durable=True)
channel.queue_declare(queue="notification-service2-pdf-queue", durable=True)


# Bind the queue to the exchange
channel.queue_bind(exchange="account.created", queue="notification-service1-queue")
channel.queue_bind(exchange="account.created", queue="notification-service2-queue")
channel.queue_bind(
    exchange="pdf.request", queue="pdf-generator-queue", routing_key="generate_pdf"
)
channel.queue_bind(
    exchange="pdf.generated",
    queue="notification-service2-pdf-queue",
    routing_key="pdf_success",
)

# Close the connection
connection.close()
