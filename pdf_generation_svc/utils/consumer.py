import pika
import os
import json

# Import pdf generation libraries
from reportlab.pdfgen import canvas
from . import account_pb2_grpc, account_pb2
import grpc
from google.protobuf.json_format import MessageToJson
from utils.publish import publish_message


class Consumer:
    def consume_message(self, queue):
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

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
        print(f"Calling account statement service using grpc for {customer_id}...")
        statement = self.get_statement(customer_id)
        statement_json = MessageToJson(statement)
        statement_dict = json.loads(statement_json)
        customer_name = statement_dict.get("customerName")
        transactions = statement_dict.get("transactions")
        # Fetch account statement from the accounts services using grpc

        os.makedirs(statements_dir, exist_ok=True)
        filepath = os.path.join(
            statements_dir, f"account_statement_cust_{customer_id}.pdf"
        )
        document_title = f"Account Statement for Customer: {customer_name}"
        title = "Transaction History"

        # Initialize the canvas
        pdf = canvas.Canvas(filepath)
        pdf.setTitle(document_title)
        pdf.drawCentredString(300, 770, document_title)
        pdf.line(30, 750, 550, 750)
        pdf.drawString(30, 720, title)
        pdf.drawString(30, 700, f"Account ID")
        pdf.drawString(120, 700, f"Date")
        pdf.drawString(320, 700, f"Amount")
        pdf.drawString(380, 700, f"Transaction Type")
        y_axis = 680
        for transaction in transactions:
            pdf.drawString(30, y_axis, f"{transaction['accountId']}")
            pdf.drawString(120, y_axis, f"{transaction['date']}")
            pdf.drawString(320, y_axis, f"{transaction['amount']}")
            pdf.drawString(380, y_axis, f"{transaction['transactionType']}")
            pdf.line(30, 750, 550, 750)
            y_axis -= 20
        pdf.save()
        message = f"Account statement for customer {customer_id} has been generated successfully."
        print(
            f"Account statement for customer {customer_id} has been generated successfully."
        )
        print("[X] Sending message to pdf.generated exchange")
        publish_message("pdf.generated", message)

    def get_statement(self, customer_id):
        # Create a gRPC channel
        try:
            with grpc.insecure_channel("localhost:50051") as channel:
                # Create a gRPC stub
                stub = account_pb2_grpc.AccountServiceGrpcStub(channel)
                # Create a request message
                request = account_pb2.AccountRequest(customer_id=customer_id)
                # Call the gRPC service
                response = stub.getAccountStatement(request)
                print(f"Response received from the server: {response}")
                return response
        except grpc.RpcError as e:
            return f"An error occurred while fetching the account statement:\n {e}"
