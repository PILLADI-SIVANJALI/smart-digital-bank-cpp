from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


# ==========================================
# FILE PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCOUNTS_FILE = os.path.join(BASE_DIR, "accounts.txt")
TRANSACTIONS_FILE = os.path.join(BASE_DIR, "transactions.txt")
INVOICES_FILE = os.path.join(BASE_DIR, "invoices.txt")


# ==========================================
# READ ACCOUNTS
# ==========================================

def load_accounts():

    accounts = []

    if not os.path.exists(ACCOUNTS_FILE):
        return accounts

    with open(ACCOUNTS_FILE, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            # Format:
            # account name pin balance

            if len(parts) != 4:
                continue

            try:

                account = int(parts[0])
                name = parts[1]
                pin = parts[2]
                balance = float(parts[3])

                accounts.append({
                    "account": account,
                    "name": name,
                    "pin": pin,
                    "balance": balance
                })

            except ValueError:

                continue

    return accounts


# ==========================================
# SAVE ACCOUNTS
# ==========================================

def save_accounts(accounts):

    with open(ACCOUNTS_FILE, "w") as file:

        for account in accounts:

            file.write(
                f"{account['account']} "
                f"{account['name']} "
                f"{account['pin']} "
                f"{account['balance']}\n"
            )


# ==========================================
# FIND ACCOUNT
# ==========================================

def find_account(accounts, account_number):

    for account in accounts:

        if account["account"] == account_number:

            return account

    return None

# ==========================================
# SAVE TRANSACTION
# ==========================================

def save_transaction(account, transaction_type, amount, balance):

    from datetime import datetime

    # Current date
    date = datetime.now().strftime("%d-%b-%Y")

    transaction_type = transaction_type.upper()

    # Decide mode
    if transaction_type == "DEPOSIT":

        mode = "Credited"

    elif transaction_type == "WITHDRAW":

        mode = "Debited"

    elif transaction_type == "TRANSFER":

        mode = "Transferred"

    elif transaction_type == "RECEIVED":

        mode = "Credited"

    else:

        mode = "Completed"

    # Transaction status
    status = "Success"

    with open(TRANSACTIONS_FILE, "a") as file:

        file.write(
            f"{account}|"
            f"{date}|"
            f"{transaction_type}|"
            f"{amount}|"
            f"{mode}|"
            f"{status}|"
            f"{balance}\n"
        )

# ==========================================
# CREATE INVOICE
# ==========================================

def create_invoice(
    transaction_type,
    account,
    name,
    amount,
    old_balance,
    new_balance,
    receiver=None
):

    # Simple transaction ID

    transaction_id = 1000

    if os.path.exists("transaction_id.txt"):

        try:

            with open("transaction_id.txt", "r") as file:
                transaction_id = int(file.read().strip()) + 1

        except:
            transaction_id = 1001

    else:

        transaction_id = 1001


    with open("transaction_id.txt", "w") as file:
        file.write(str(transaction_id))


    with open(INVOICES_FILE, "a") as file:

        file.write("\n")
        file.write("========================================\n")
        file.write("          SMART DIGITAL BANK\n")
        file.write("          TRANSACTION INVOICE\n")
        file.write("========================================\n")

        file.write(f"Transaction ID : TXN{transaction_id}\n")
        file.write(f"Account Number : {account}\n")
        file.write(f"Customer Name  : {name}\n")

        if receiver is not None:

            file.write(f"Receiver Acc.  : {receiver}\n")

        file.write(f"Transaction    : {transaction_type}\n")
        file.write(f"Amount         : {amount}\n")
        file.write(f"Previous Bal.  : {old_balance}\n")
        file.write(f"New Balance    : {new_balance}\n")
        file.write("Status         : SUCCESS\n")

        file.write("========================================\n")


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    account_number = data.get("account")
    pin = data.get("pin")

    try:
        account_number = int(account_number)
    except:
        return jsonify({
            "status": "failed",
            "message": "Invalid Account Number"
        })


    accounts = load_accounts()

    account = find_account(accounts, account_number)


    if account is None:

        return jsonify({
            "status": "failed",
            "message": "Account Not Found"
        })


    if account["pin"] != str(pin):

        return jsonify({
            "status": "failed",
            "message": "Incorrect PIN"
        })


    return jsonify({

        "status": "success",

        "name": account["name"],

        "balance": account["balance"]

    })


# ==========================================
# DEPOSIT
# ==========================================

@app.route("/deposit", methods=["POST"])
def deposit():

    data = request.get_json()

    account_number = data.get("account")
    amount = data.get("amount")


    try:

        account_number = int(account_number)
        amount = float(amount)

    except:

        return jsonify({
            "status": "failed",
            "message": "Invalid input"
        })


    if amount <= 0:

        return jsonify({
            "status": "failed",
            "message": "Invalid amount"
        })


    accounts = load_accounts()

    account = find_account(accounts, account_number)


    if account is None:

        return jsonify({
            "status": "failed",
            "message": "Account Not Found"
        })


    old_balance = account["balance"]

    account["balance"] += amount

    save_accounts(accounts)


    save_transaction(
        account_number,
        "DEPOSIT",
        amount,
        account["balance"]
    )


    create_invoice(
        "DEPOSIT",
        account_number,
        account["name"],
        amount,
        old_balance,
        account["balance"]
    )


    return jsonify({

        "status": "success",

        "balance": account["balance"]

    })


# ==========================================
# WITHDRAW
# ==========================================

@app.route("/withdraw", methods=["POST"])
def withdraw():

    data = request.get_json()

    account_number = data.get("account")
    amount = data.get("amount")


    try:

        account_number = int(account_number)
        amount = float(amount)

    except:

        return jsonify({
            "status": "failed",
            "message": "Invalid input"
        })


    if amount <= 0:

        return jsonify({
            "status": "failed",
            "message": "Invalid amount"
        })


    accounts = load_accounts()

    account = find_account(accounts, account_number)


    if account is None:

        return jsonify({
            "status": "failed",
            "message": "Account Not Found"
        })


    if amount > account["balance"]:

        return jsonify({
            "status": "failed",
            "message": "Insufficient Balance"
        })


    old_balance = account["balance"]

    account["balance"] -= amount

    save_accounts(accounts)


    save_transaction(
        account_number,
        "WITHDRAW",
        amount,
        account["balance"]
    )


    create_invoice(
        "WITHDRAW",
        account_number,
        account["name"],
        amount,
        old_balance,
        account["balance"]
    )


    return jsonify({

        "status": "success",

        "balance": account["balance"]

    })


# ==========================================
# TRANSFER
# ==========================================

@app.route("/transfer", methods=["POST"])
def transfer():

    data = request.get_json()

    sender_number = data.get("sender")
    receiver_number = data.get("receiver")
    amount = data.get("amount")


    try:

        sender_number = int(sender_number)
        receiver_number = int(receiver_number)
        amount = float(amount)

    except:

        return jsonify({
            "status": "failed",
            "message": "Invalid input"
        })


    if amount <= 0:

        return jsonify({
            "status": "failed",
            "message": "Invalid amount"
        })


    if sender_number == receiver_number:

        return jsonify({
            "status": "failed",
            "message": "Cannot transfer to your own account"
        })


    accounts = load_accounts()


    sender = find_account(accounts, sender_number)

    receiver = find_account(accounts, receiver_number)


    if sender is None:

        return jsonify({
            "status": "failed",
            "message": "Sender Account Not Found"
        })


    if receiver is None:

        return jsonify({
            "status": "failed",
            "message": "Receiver Account Not Found"
        })


    if amount > sender["balance"]:

        return jsonify({
            "status": "failed",
            "message": "Insufficient Balance"
        })


    old_balance = sender["balance"]


    sender["balance"] -= amount

    receiver["balance"] += amount


    save_accounts(accounts)


    save_transaction(
        sender_number,
        "TRANSFER",
        amount,
        sender["balance"]
    )


    save_transaction(
        receiver_number,
        "RECEIVED",
        amount,
        receiver["balance"]
    )


    create_invoice(
        "TRANSFER",
        sender_number,
        sender["name"],
        amount,
        old_balance,
        sender["balance"],
        receiver_number
    )


    return jsonify({

        "status": "success",

        "balance": sender["balance"]

    })





# ==========================================
# GET INVOICES
# ==========================================

@app.route("/invoices", methods=["GET"])
def get_invoices():

    account_number = request.args.get("account")

    if not account_number:

        return jsonify({
            "success": False,
            "message": "Account number is required"
        })

    if not os.path.exists(INVOICES_FILE):

        return jsonify({
            "success": True,
            "invoices": []
        })

    invoices = []

    with open(INVOICES_FILE, "r") as file:

        content = file.read()

    blocks = content.split("========================================")

    for block in blocks:

        if "Transaction ID" not in block:
            continue

        invoice = {}

        lines = block.strip().splitlines()

        for line in lines:

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            key = key.strip()
            value = value.strip()

            if key == "Transaction ID":
                invoice["transaction_id"] = value

            elif key == "Account Number":
                invoice["account"] = value

            elif key == "Customer Name":
                invoice["name"] = value

            elif key == "Receiver Acc.":
                invoice["receiver"] = value

            elif key == "Transaction":
                invoice["type"] = value

            elif key == "Amount":
                invoice["amount"] = value

            elif key == "Previous Bal.":
                invoice["old_balance"] = value

            elif key == "New Balance":
                invoice["balance"] = value

            elif key == "Status":
                invoice["status"] = value

        if invoice.get("account") == str(account_number):

            invoices.append(invoice)

    invoices.reverse()

    return jsonify({
        "success": True,
        "invoices": invoices
    })


# ==========================================
# MINI STATEMENT
# ==========================================

@app.route("/statement", methods=["GET"])
def get_statement():

    account_number = request.args.get("account")

    if not account_number:
        return jsonify({
            "success": False,
            "message": "Account number is required"
        })

    if not os.path.exists(TRANSACTIONS_FILE):
        return jsonify({
            "success": True,
            "transactions": []
        })

    transactions = []

    with open(TRANSACTIONS_FILE, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            # ==========================================
            # NEW FLASK FORMAT
            # Account | Date | Type | Amount | Mode | Status | Balance
            # ==========================================

            if "|" in line:

                parts = line.split("|")

                # --------------------------------------
                # NEW 7-FIELD FORMAT
                # --------------------------------------

                if len(parts) == 7:

                    account = parts[0].strip()
                    date = parts[1].strip()
                    transaction_type = parts[2].strip()
                    amount = parts[3].strip()
                    mode = parts[4].strip()
                    status = parts[5].strip()
                    balance = parts[6].strip()

                    if account == str(account_number):

                        transactions.append({
                            "date": date,
                            "transaction": transaction_type,
                            "amount": amount,
                            "mode": mode,
                            "status": status,
                            "balance": balance
                        })

                # --------------------------------------
                # OLD DEPOSIT / WITHDRAW FORMAT
                # Account | Type | Amount | Date
                # --------------------------------------

                elif len(parts) == 4:

                    account = parts[0].strip()
                    transaction_type = parts[1].strip()
                    amount = parts[2].strip()
                    date = parts[3].strip()

                    if account != str(account_number):
                        continue

                    if transaction_type.upper() == "DEPOSIT":

                        mode = "Credited"

                    elif transaction_type.upper() == "WITHDRAW":

                        mode = "Debited"

                    else:

                        mode = "Completed"

                    status = "Success"

                    transactions.append({
                        "date": date,
                        "transaction": transaction_type,
                        "amount": amount,
                        "mode": mode,
                        "status": status,
                        "balance": ""
                    })

                # --------------------------------------
                # OLD TRANSFER FORMAT
                # Account | Transfer | Amount | Receiver | Date
                # --------------------------------------

                elif len(parts) == 5:

                    account = parts[0].strip()
                    transaction_type = parts[1].strip()
                    amount = parts[2].strip()
                    receiver = parts[3].strip()
                    date = parts[4].strip()

                    if account != str(account_number):
                        continue

                    if transaction_type.upper() == "TRANSFER":

                        mode = "Transferred"

                    else:

                        mode = "Completed"

                    status = "Success"

                    transactions.append({
                        "date": date,
                        "transaction": transaction_type,
                        "amount": amount,
                        "mode": mode,
                        "status": status,
                        "balance": "",
                        "receiver": receiver
                    })

            # ==========================================
            # OLD SPACE FORMAT
            # Account Type Amount Balance
            # Example:
            # 5001 DEPOSIT 500 31000
            # ==========================================

            else:

                parts = line.split()

                if len(parts) == 4:

                    account = parts[0].strip()
                    transaction_type = parts[1].strip()
                    amount = parts[2].strip()
                    balance = parts[3].strip()

                    if account != str(account_number):
                        continue

                    # Determine transaction mode

                    if transaction_type.upper() == "DEPOSIT":

                        mode = "Credited"

                    elif transaction_type.upper() == "WITHDRAW":

                        mode = "Debited"

                    elif transaction_type.upper() == "TRANSFER":

                        mode = "Transferred"

                    elif transaction_type.upper() == "RECEIVED":

                        mode = "Credited"

                    else:

                        mode = "Completed"

                    transactions.append({

                        # Old records did not store date
                        "date": "Date not recorded",

                        "transaction": transaction_type,

                        "amount": amount,

                        "mode": mode,

                        "status": "Success",

                        "balance": balance

                    })


    # ==========================================
    # NEWEST TRANSACTIONS FIRST
    # ==========================================

    transactions.reverse()


    return jsonify({

        "success": True,

        "transactions": transactions

    })


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
