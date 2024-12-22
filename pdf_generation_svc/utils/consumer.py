import pika
import os
import json

# Import pdf generation libraries
from reportlab.pdfgen import canvas


class Consumer:
    def consume_message(self, queue):
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue)

        # Create a consumer
        channel.basic_consume(
            queue=queue, auto_ack=True, on_message_callback=self.callback
        )
        print("[X] Listening to messages. Press Ctrl + X to exit")
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(f"[X] Received message: {body}")
        # # Initalize the variables
        statements_dir = "statements"
        # # customer_id = body["customer_id"]
        body_dict = json.loads(body)
        customer_id = body_dict.get("customer_id")
        print(customer_id)
        # Fetch account statement from the accounts services using grpc

        os.makedirs(statements_dir, exist_ok=True)
        filepath = os.path.join(
            statements_dir, f"account_statement_cust_{customer_id}.pdf"
        )
        document_title = f"Account Statement for Customer ID: {customer_id}"
        title = "Transaction History"
        textLines = [
            "Some information related to the account statement",
            "Transaction History",
        ]
        # Initialize the canvas
        pdf = canvas.Canvas(filepath)
        pdf.setTitle(document_title)
        # Register an external font
        # pdfmetrics.registerFont(TTFont("custom_font", "SakBunderan.ttf"))
        # pdf.setFont("custom_font", 36)
        pdf.drawCentredString(300, 770, document_title)
        pdf.line(30, 710, 550, 710)  # Save the PDF to a file
        pdf.save()

        # Return the PDF as a response
        with open(filepath, "rb") as pdf_file:
            pdf_data = pdf_file.read()

        print("PDF generated successfully for customer {}".format(customer_id))
