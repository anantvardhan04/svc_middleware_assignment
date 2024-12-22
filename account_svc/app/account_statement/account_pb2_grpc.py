# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import account_svc.app.account_statement.account_pb2 as account__pb2

GRPC_GENERATED_VERSION = "1.68.1"
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower

    _version_not_supported = first_version_is_lower(
        GRPC_VERSION, GRPC_GENERATED_VERSION
    )
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f"The grpc package installed is at version {GRPC_VERSION},"
        + f" but the generated code in account_pb2_grpc.py depends on"
        + f" grpcio>={GRPC_GENERATED_VERSION}."
        + f" Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}"
        + f" or downgrade your generated code using grpcio-tools<={GRPC_VERSION}."
    )


class AccountServiceGrpcStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getAccountStatement = channel.unary_unary(
            "/AccountServiceGrpc/getAccountStatement",
            request_serializer=account__pb2.AccountRequest.SerializeToString,
            response_deserializer=account__pb2.AccountResponse.FromString,
            _registered_method=True,
        )


class AccountServiceGrpcServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getAccountStatement(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_AccountServiceGrpcServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "getAccountStatement": grpc.unary_unary_rpc_method_handler(
            servicer.getAccountStatement,
            request_deserializer=account__pb2.AccountRequest.FromString,
            response_serializer=account__pb2.AccountResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "AccountServiceGrpc", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers("AccountServiceGrpc", rpc_method_handlers)


# This class is part of an EXPERIMENTAL API.
class AccountServiceGrpc(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getAccountStatement(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/AccountServiceGrpc/getAccountStatement",
            account__pb2.AccountRequest.SerializeToString,
            account__pb2.AccountResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )
