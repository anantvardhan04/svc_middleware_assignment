from app.account_core import bp
from flask import request


from app.account_core.service import AccountService  # Create this service file


account_service = AccountService()


@bp.route("/create", methods=["POST"])
def create_account():
    # Call service method to handle business logic
    result = account_service.create_account(request)

    return result


@bp.route("/<customer_id>", methods=["GET"])
def list_account(customer_id):
    # Call service method to handle business logic
    result = account_service.list_account_details(customer_id)

    return result


# @bp.route("/statement/<customer_id>", methods=["GET"])
# def get_account_statement(customer_id):
#     result = account_service.get_account_statement(customer_id)
#     return result


@bp.route("/statement/<customer_id>/generatepdf", methods=["GET"])
def generate_pdf(customer_id):
    result = account_service.generate_pdf(customer_id)
    return result
