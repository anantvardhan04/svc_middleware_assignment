from app.extensions import db


class Customer(db.Model):
    customerid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)

    def __repr__(self):
        return "<Customer {}>".format(self.name)


class AccountType(db.Model):
    account_type_id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<AccountType {}>".format(self.account_type)


class Account(db.Model):
    @staticmethod
    def generate_account_number():
        last_account = (
            db.session.query(Account).order_by(Account.account_number.desc()).first()
        )
        if last_account and last_account.account_number:
            next_number = int(last_account.account_number) + 1
        else:
            next_number = 1
        return str(next_number).zfill(10)

    account_number = db.Column(
        db.String(10),
        primary_key=True,
        default=generate_account_number,
    )

    customer_id = db.Column(
        db.Integer, db.ForeignKey("customer.customerid"), nullable=False, unique=True
    )
    account_type_id = db.Column(
        db.Integer, db.ForeignKey("account_type.account_type_id"), nullable=False
    )
    balance = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    created_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False,
    )

    def __repr__(self):
        return "<Account {}>".format(self.customer_id)

    def __init__(self, **kwargs):
        if "account_number" not in kwargs:
            kwargs["account_number"] = self.generate_account_number()
        super().__init__(**kwargs)


#  CREATE TABLE transaction (
#     transaction_id  VA SERIAL PRIMARY KEY,
#     from_account_number VARCHAR(10) NOT NULL,
#     to_account_number VARCHAR(10) NOT NULL,
#     amount NUMERIC(15, 2) NOT NULL,
#     transaction_type VARCHAR(20) NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# )


class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    self_account_number = db.Column(
        db.String(10), db.ForeignKey("account.account_number"), nullable=False
    )
    other_account_number = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    transaction_type = db.Column(
        db.Enum("CREDIT", "DEBIT", name="transaction_type_enum"),
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(), nullable=False
    )
