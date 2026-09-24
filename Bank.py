import json
import random
import string
from pathlib import Path
from datetime import datetime


class Bank:

    DATABASE = Path("data.json")

    def __init__(self):
        self.data = self.load_data()

    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self):

        if not self.DATABASE.exists():
            return []

        try:
            with open(self.DATABASE, "r") as file:
                data = json.load(file)

            if not isinstance(data, list):
                return []

            # Convert old data format to new format
            for account in data:

                if "accountNo." in account and "accountNo" not in account:
                    account["accountNo"] = account.pop("accountNo.")

                if "balance" not in account:
                    account["balance"] = 0

                if "transactions" not in account:
                    account["transactions"] = []

            return data

        except (json.JSONDecodeError, OSError):
            return []

    # =====================================================
    # SAVE DATA
    # =====================================================

    def save_data(self):

        with open(self.DATABASE, "w") as file:
            json.dump(self.data, file, indent=4)

    # =====================================================
    # GENERATE ACCOUNT NUMBER
    # =====================================================

    def generate_account_number(self):

        while True:

            letters = "".join(
                random.choices(string.ascii_uppercase, k=3)
            )

            numbers = "".join(
                random.choices(string.digits, k=3)
            )

            special = random.choice("!@#$%^&*")

            account_number = letters + numbers + special

            if not any(
                account.get("accountNo") == account_number
                for account in self.data
            ):
                return account_number

    # =====================================================
    # FIND ACCOUNT
    # =====================================================

    def find_account(self, account_no, pin):

        for account in self.data:

            if (
                account.get("accountNo") == account_no
                and str(account.get("pin")) == str(pin)
            ):
                return account

        return None

    # =====================================================
    # GET ACCOUNT
    # =====================================================

    def get_account(self, account_no):

        for account in self.data:

            if account.get("accountNo") == account_no:
                return account

        return None

    # =====================================================
    # CREATE ACCOUNT
    # =====================================================

    def create_account(self, name, age, email, pin):

        name = name.strip()
        email = email.strip()
        pin = pin.strip()

        if not name:
            return False, "Name cannot be empty."

        if age < 18:
            return False, "You must be at least 18 years old."

        if not pin.isdigit() or len(pin) != 4:
            return False, "PIN must contain exactly 4 digits."

        if "@" not in email or "." not in email:
            return False, "Please enter a valid email."

        account = {

            "name": name,

            "age": age,

            "email": email,

            "pin": pin,

            "accountNo": self.generate_account_number(),

            "balance": 0.0,

            "transactions": []

        }

        self.data.append(account)

        self.save_data()

        return True, account

    # =====================================================
    # LOGIN
    # =====================================================

    def login(self, account_no, pin):

        return self.find_account(
            account_no.strip(),
            pin.strip()
        )

    # =====================================================
    # DEPOSIT
    # =====================================================

    def deposit(self, account_no, amount):

        account = self.get_account(account_no.strip())

        if account is None:
            return False, "Account not found."

        try:
            amount = float(amount)

        except (ValueError, TypeError):
            return False, "Please enter a valid amount."

        if amount <= 0:
            return False, "Amount must be greater than ₹0."

        if amount > 10000:
            return False, "Maximum deposit is ₹10,000 at a time."

        # Make sure balance exists
        if "balance" not in account:
            account["balance"] = 0.0

        account["balance"] = float(account["balance"])

        # Add money
        account["balance"] += amount

        # Make sure transaction list exists
        if "transactions" not in account:
            account["transactions"] = []

        # Add transaction
        account["transactions"].append({

            "type": "Deposit",

            "amount": amount,

            "date": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

        })

        # Save changes
        self.save_data()

        return True, f"₹{amount:,.2f} deposited successfully."

    # =====================================================
    # WITHDRAW
    # =====================================================

    def withdraw(self, account_no, amount):

        account = self.get_account(account_no.strip())

        if account is None:
            return False, "Account not found."

        try:
            amount = float(amount)

        except (ValueError, TypeError):
            return False, "Please enter a valid amount."

        if amount <= 0:
            return False, "Amount must be greater than ₹0."

        balance = float(account.get("balance", 0))

        if amount > balance:
            return False, "Insufficient balance."

        account["balance"] = balance - amount

        if "transactions" not in account:
            account["transactions"] = []

        account["transactions"].append({

            "type": "Withdrawal",

            "amount": amount,

            "date": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

        })

        self.save_data()

        return True, f"₹{amount:,.2f} withdrawn successfully."

    # =====================================================
    # ACCOUNT DETAILS
    # =====================================================

    def get_details(self, account_no):

        account = self.get_account(account_no)

        if account is None:
            return None

        return {

            "Name": account.get("name"),

            "Age": account.get("age"),

            "Email": account.get("email"),

            "Account Number": account.get("accountNo"),

            "Balance": account.get("balance", 0)

        }

    # =====================================================
    # UPDATE ACCOUNT
    # =====================================================

    def update_account(
        self,
        account_no,
        name,
        email,
        new_pin
    ):

        account = self.get_account(account_no)

        if account is None:
            return False, "Account not found."

        name = name.strip()
        email = email.strip()
        new_pin = new_pin.strip()

        if not name:
            return False, "Name cannot be empty."

        if "@" not in email or "." not in email:
            return False, "Please enter a valid email."

        if not new_pin.isdigit() or len(new_pin) != 4:
            return False, "PIN must contain exactly 4 digits."

        account["name"] = name
        account["email"] = email
        account["pin"] = new_pin

        self.save_data()

        return True, "Account details updated successfully."

    # =====================================================
    # DELETE ACCOUNT
    # =====================================================

    def delete_account(self, account_no):

        account = self.get_account(account_no)

        if account is None:
            return False, "Account not found."

        self.data.remove(account)

        self.save_data()

        return True, "Account deleted successfully."

    # =====================================================
    # TRANSACTION HISTORY
    # =====================================================

    def get_transactions(self, account_no):

        account = self.get_account(account_no)

        if account is None:
            return []

        return account.get("transactions", [])