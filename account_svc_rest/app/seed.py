from . import create_app
from app.models.account import Customer, AccountType, Account, Transaction
from app.extensions import db


def seed_data():
    app = create_app()
    with app.app_context():
        # Create all the tables
        db.create_all()
        # Remove all the data if already present
        db.session.query(Account).delete()
        db.session.query(Customer).delete()
        db.session.query(AccountType).delete()
        db.session.query(Transaction).delete()

        # Create account types
        account_types = [
            AccountType(account_type_id=1, account_type="Savings"),
            AccountType(account_type_id=2, account_type="Current"),
        ]
        transactions = [
            Transaction(
                self_account_number="0000000001",
                other_account_number="0000000003",
                transaction_type="CREDIT",
                amount=12333.00,
            ),
            Transaction(
                self_account_number="0000000001",
                other_account_number="0000000004",
                transaction_type="DEBIT",
                amount=1500.00,
            ),
            Transaction(
                self_account_number="0000000002",
                other_account_number="0000000001",
                transaction_type="DEBIT",
                amount=1000.00,
            ),
            Transaction(
                self_account_number="0000000002",
                other_account_number="0000000004",
                transaction_type="DEBIT",
                amount=150947.00,
            ),
            Transaction(
                self_account_number="0000000001",
                other_account_number="0000000002",
                transaction_type="CREDIT",
                amount=450.00,
            ),
        ]
        db.session.add_all(account_types)
        db.session.add_all(transactions)
        db.session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_data()
