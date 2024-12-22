from flask import jsonify
from app.models.account import Account, AccountType, Customer, Transaction
from app.extensions import db
from app.utils.publish import publish_message
import os
import json


# Import pdf generation related modules and classes
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


class AccountService:
    def create_account(self, request):
        # Business logic to create an account
        print("Initiating account creation process...")
        required_fields = ["name", "phone_number", "account_type"]
        data = request.get_json()
        if not data:
            return jsonify(error="No input data provided"), 400
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return (
                jsonify(error=f"Missing required fields: {', '.join(missing_fields)}"),
                400,
            )

        # Parse data and create account
        name = data.get("name")
        phone_number = data.get("phone_number")
        account_type = data.get("account_type")
        print(f"Creating account for {name} with phone number {phone_number}...")

        # Check if phone number is valid (assuming 10 digits)
        if not phone_number.isdigit() or len(phone_number) != 10:
            return jsonify(error="Invalid phone number format"), 400

        # Check if account type is valid
        valid_account_types = ["Savings", "Current"]
        if account_type not in valid_account_types:
            return jsonify(error="Invalid account type"), 400

        # Check if customer already exists
        customer_record = Customer.query.filter_by(phone_number=phone_number).first()
        if customer_record:
            return jsonify(error="Customer with this phone number already exists"), 400

        # Update Customer Table
        customer = Customer(name=name, phone_number=phone_number)
        db.session.add(customer)
        db.session.commit()
        customer = Customer.query.filter_by(phone_number=phone_number).first()

        # Update Account Table
        account_type_row = AccountType.query.filter_by(
            account_type=account_type
        ).first()
        # account_id = account_type_row.account_type_id
        account = Account(
            customer_id=customer.customerid,
            account_type_id=account_type_row.account_type_id,
        )

        db.session.add(account)
        db.session.commit()
        # Update Account Table
        message = "Congratulations {} ! Your {} Account has been created successfully.".format(
            name, account_type_row.account_type
        )
        publish_message("account_svc", message)
        return jsonify(message=message), 201

    def list_account_details(self, customer_id):
        # if in customer table, this cust_id doesnt exist, return error
        # Query customer table, and check if a customer with customer_id 1 exists or not
        customer = Customer.query.filter_by(customerid=customer_id).all()
        if not customer:
            return jsonify(error="Customer ID doesn't exist"), 400

        account = Account.query.filter_by(customer_id=customer_id).first()
        customer = Customer.query.filter_by(customerid=customer_id).first()
        account_type = AccountType.query.filter_by(
            account_type_id=account.account_type_id
        ).first()

        response = {
            "customer_id": account.customer_id,
            "customer_name": customer.name,
            "account_number": account.account_number,
            "balance": account.balance,
            "created_at": account.created_at,
            "account_type": account_type.account_type,
        }

        return jsonify(response), 200

    # def get_account_statement(self, customer_id):
    #     # Fetch all rows for customer_id's account number from transaction table
    #     account = Account.query.filter_by(customer_id=customer_id).first()
    #     if account:
    #         account_number = account.account_number
    #         transactions_statement = []
    #         transactions = Transaction.query.filter_by(
    #             self_account_number=account_number
    #         ).all()
    #         for transaction in transactions:
    #             statement = {
    #                 "self_account_number": transaction.self_account_number,
    #                 "amount": transaction.amount,
    #                 "transaction_type": transaction.transaction_type,
    #                 "other_account_number": transaction.other_account_number,
    #                 "transaction_date": transaction.created_at,
    #             }
    #             transactions_statement.append(statement)
    #         return transactions_statement

    #     else:
    #         return jsonify(
    #             error="No account found for the customer id {}".format(customer_id)
    #         )

    def generate_pdf(self, customer_id):
        # Produce a message in a dedicated pdf generation queue
        event = {"customer_id": customer_id}
        event_json = json.dumps(event)
        publish_message("pdf_generation", str(event_json))
        return (
            jsonify(message="PDF Generation request for account statement created"),
            200,
        )
