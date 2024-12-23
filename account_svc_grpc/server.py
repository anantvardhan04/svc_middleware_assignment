import generated
import grpc
from concurrent import futures
import requests


mock_responses = {
    "1": {
        "customer_name": "Anant Vardhan",
        "transactions": [
            {
                "account_id": "1",
                "date": "12-Dec-2023",
                "amount": 100.00,
                "transaction_type": "CREDIT",
            }
        ],
    }
}


class AccountServiceGrpc(generated.account_pb2_grpc.AccountServiceGrpcServicer):
    def getAccountStatement(self, request, context):
        customer_id = request.customer_id
        print(f"Received request for customer_id: {customer_id}")
        account_svc_base_url = "http://127.0.0.1:5000/account/"
        customer_detail_api = account_svc_base_url + f"{customer_id}"
        account_statement_api = account_svc_base_url + f"statement/{customer_id}"

        customer_detail_resonse = requests.get(customer_detail_api).json()
        customer_name = customer_detail_resonse.get("customer_name")
        transactions = requests.get(account_statement_api).json()
        transaction_formatted_list = []
        for transaction in transactions:
            transaction_formatted = generated.account_pb2.Transaction(
                account_id=transaction["other_account_number"],
                date=transaction["transaction_date"],
                amount=float(transaction["amount"]),
                transaction_type=transaction["transaction_type"],
            )
            transaction_formatted_list.append(transaction_formatted)
        response = generated.account_pb2.AccountResponse(
            customer_name=customer_name,
            transactions=transaction_formatted_list,
        )
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    generated.account_pb2_grpc.add_AccountServiceGrpcServicer_to_server(
        AccountServiceGrpc(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Account Service running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
