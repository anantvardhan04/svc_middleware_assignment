import account_svc.app.account_statement.account_pb2_grpc as account_pb2_grpc
import account_svc.app.account_statement.account_pb2 as account_pb2
import grpc
from concurrent import futures


class AccountServiceGrpc(account_pb2_grpc.AccountServiceGrpcServicer):
    def getAccountStatement(self, request, context):
        customer_id = request.customer_id
        return "Customer ID: {}".format(customer_id)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    account_pb2_grpc.add_AccountServiceGrpcServicer_to_server(
        AccountServiceGrpc(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Account Service running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
