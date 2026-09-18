#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

using namespace std;

// ===============================
// ACCOUNT CLASS
// ===============================

class Account
{
public:
    int accNo;
    string name;
    string pin;
    double balance;

    Account()
    {
        accNo = 0;
        name = "";
        pin = "";
        balance = 0;
    }

    Account(int a, string n, string p, double b)
    {
        accNo = a;
        name = n;
        pin = p;
        balance = b;
    }
};

// Store all accounts
vector<Account> accounts;


// ===============================
// LOAD ACCOUNTS
// ===============================

void load()
{
    accounts.clear();

    ifstream file("accounts.txt");

    Account a;

    while(file >> a.accNo >> a.name >> a.pin >> a.balance)
    {
        accounts.push_back(a);
    }

    file.close();
}


// ===============================
// SAVE ACCOUNTS
// ===============================

void save()
{
    ofstream file("accounts.txt");

    for(auto &a : accounts)
    {
        file << a.accNo << " "
             << a.name << " "
             << a.pin << " "
             << a.balance << endl;
    }

    file.close();
}


// ===============================
// FIND ACCOUNT
// ===============================

int findAcc(int number)
{
    for(int i = 0; i < accounts.size(); i++)
    {
        if(accounts[i].accNo == number)
        {
            return i;
        }
    }

    return -1;
}


// ===============================
// GET TRANSACTION NUMBER
// ===============================

int getTransactionNumber()
{
    ifstream file("transaction_id.txt");

    int number = 1000;

    if(file >> number)
    {
        number++;
    }

    file.close();

    ofstream out("transaction_id.txt");

    out << number;

    out.close();

    return number;
}


// ===============================
// CREATE INVOICE
// ===============================

void createInvoice(
    string type,
    int accountNumber,
    string customerName,
    double amount,
    double oldBalance,
    double newBalance,
    int receiverAccount = 0)
{
    int transactionNumber = getTransactionNumber();

    cout << "\n";
    cout << "========================================\n";
    cout << "          SMART DIGITAL BANK\n";
    cout << "          TRANSACTION INVOICE\n";
    cout << "========================================\n";

    cout << "Transaction ID : TXN" << transactionNumber << endl;
    cout << "Account Number : " << accountNumber << endl;
    cout << "Customer Name  : " << customerName << endl;

    if(type == "TRANSFER")
    {
        cout << "Receiver Acc.  : " << receiverAccount << endl;
    }

    cout << "Transaction    : " << type << endl;
    cout << "Amount         : " << amount << endl;
    cout << "Previous Bal.  : " << oldBalance << endl;
    cout << "New Balance    : " << newBalance << endl;
    cout << "Status         : SUCCESS\n";

    cout << "========================================\n";
    cout << "       Thank You for Banking With Us\n";
    cout << "========================================\n";


    // Save invoice in file

    ofstream file("invoices.txt", ios::app);

    file << "========================================\n";
    file << "          SMART DIGITAL BANK\n";
    file << "          TRANSACTION INVOICE\n";
    file << "========================================\n";

    file << "Transaction ID : TXN" << transactionNumber << endl;
    file << "Account Number : " << accountNumber << endl;
    file << "Customer Name  : " << customerName << endl;

    if(type == "TRANSFER")
    {
        file << "Receiver Acc.  : " << receiverAccount << endl;
    }

    file << "Transaction    : " << type << endl;
    file << "Amount         : " << amount << endl;
    file << "Previous Bal.  : " << oldBalance << endl;
    file << "New Balance    : " << newBalance << endl;
    file << "Status         : SUCCESS\n";

    file << "========================================\n\n";

    file.close();
}


// ===============================
// SAVE TRANSACTION
// ===============================

void saveTransaction(
    int accountNumber,
    string type,
    double amount,
    double balance)
{
    ofstream file("transactions.txt", ios::app);

    file << accountNumber << " "
         << type << " "
         << amount << " "
         << balance << endl;

    file.close();
}


// ===============================
// REGISTER ACCOUNT
// ===============================

void reg()
{
    load();

    int no;
    string n;
    string p;
    double bal;

    cout << "\n";
    cout << "========================================\n";
    cout << "          ACCOUNT REGISTRATION\n";
    cout << "========================================\n";

    cout << "Account Number : ";
    cin >> no;


    // Check duplicate account

    if(findAcc(no) != -1)
    {
        cout << "\nAccount already exists!\n";
        return;
    }


    cout << "Name : ";
    cin >> n;


    // PIN validation

    cout << "Create 4-digit PIN : ";
    cin >> p;

    while(p.length() != 4)
    {
        cout << "PIN must contain exactly 4 digits.\n";
        cout << "Enter PIN again : ";
        cin >> p;
    }


    // Opening balance

    cout << "Opening Balance : ";
    cin >> bal;

    if(bal < 0)
    {
        cout << "Balance cannot be negative.\n";
        return;
    }


    // Create account

    accounts.push_back(Account(no, n, p, bal));

    save();


    cout << "\n";
    cout << "========================================\n";
    cout << "       ACCOUNT CREATED SUCCESSFULLY\n";
    cout << "========================================\n";

    cout << "Account Number : " << no << endl;
    cout << "Customer Name  : " << n << endl;
    cout << "Balance        : " << bal << endl;
}


// ===============================
// LOGIN
// ===============================

int login()
{
    load();

    int no;
    string p;

    cout << "\n";
    cout << "========================================\n";
    cout << "                 LOGIN\n";
    cout << "========================================\n";

    cout << "Account Number : ";
    cin >> no;

    cout << "PIN            : ";
    cin >> p;


    int index = findAcc(no);


    if(index == -1)
    {
        cout << "\nAccount not found!\n";
        return -1;
    }


    if(accounts[index].pin != p)
    {
        cout << "\nIncorrect PIN!\n";
        return -1;
    }


    cout << "\nLogin Successful!\n";
    cout << "Welcome " << accounts[index].name << "!\n";


    return index;
}


// ===============================
// PROFILE
// ===============================

void profile(Account &a)
{
    cout << "\n";
    cout << "========================================\n";
    cout << "             MY PROFILE\n";
    cout << "========================================\n";

    cout << "Account Number : " << a.accNo << endl;
    cout << "Customer Name  : " << a.name << endl;
    cout << "Current Balance: " << a.balance << endl;

    cout << "========================================\n";
}


// ===============================
// TRANSACTION HISTORY
// ===============================

void transactionHistory(int accountNumber)
{
    ifstream file("transactions.txt");

    string line;

    bool found = false;


    cout << "\n";
    cout << "========================================\n";
    cout << "          TRANSACTION HISTORY\n";
    cout << "========================================\n";


    while(getline(file, line))
    {
        if(line.empty())
        {
            continue;
        }


        // New space-separated format

        stringstream ss(line);

        int acc;
        string type;
        double amount;
        double balance;


        if(ss >> acc >> type >> amount >> balance)
        {
            if(acc == accountNumber)
            {
                found = true;

                cout << "\n";
                cout << "Type       : " << type << endl;
                cout << "Amount     : " << amount << endl;
                cout << "Balance    : " << balance << endl;

                cout << "----------------------------------------\n";
            }
        }
    }


    file.close();


    if(!found)
    {
        cout << "No transactions found.\n";
    }
}


// ===============================
// DEPOSIT
// ===============================

void deposit(Account &a)
{
    double amount;

    cout << "\n";
    cout << "========== DEPOSIT ==========\n";

    cout << "Enter Amount : ";
    cin >> amount;


    if(amount <= 0)
    {
        cout << "Invalid amount!\n";
        return;
    }


    double oldBalance = a.balance;


    a.balance = a.balance + amount;


    saveTransaction(
        a.accNo,
        "DEPOSIT",
        amount,
        a.balance
    );


    save();


    cout << "\nAmount Deposited Successfully!\n";

    cout << "Current Balance : "
         << a.balance << endl;


    // Generate invoice

    createInvoice(
        "DEPOSIT",
        a.accNo,
        a.name,
        amount,
        oldBalance,
        a.balance
    );
}


// ===============================
// WITHDRAW
// ===============================

void withdraw(Account &a)
{
    double amount;

    cout << "\n";
    cout << "========== WITHDRAW ==========\n";

    cout << "Enter Amount : ";
    cin >> amount;


    if(amount <= 0)
    {
        cout << "Invalid amount!\n";
        return;
    }


    if(amount > a.balance)
    {
        cout << "Insufficient Balance!\n";
        return;
    }


    double oldBalance = a.balance;


    a.balance = a.balance - amount;


    saveTransaction(
        a.accNo,
        "WITHDRAW",
        amount,
        a.balance
    );


    save();


    cout << "\nWithdrawal Successful!\n";

    cout << "Remaining Balance : "
         << a.balance << endl;


    // Generate invoice

    createInvoice(
        "WITHDRAW",
        a.accNo,
        a.name,
        amount,
        oldBalance,
        a.balance
    );
}


// ===============================
// TRANSFER MONEY
// ===============================

void transferMoney(Account &a)
{
    int receiver;
    double amount;


    cout << "\n";
    cout << "========== MONEY TRANSFER ==========\n";


    cout << "Receiver Account Number : ";
    cin >> receiver;


    // Cannot transfer to own account

    if(receiver == a.accNo)
    {
        cout << "You cannot transfer money to your own account!\n";
        return;
    }


    // Find receiver

    int receiverIndex = findAcc(receiver);


    if(receiverIndex == -1)
    {
        cout << "Receiver Account Not Found!\n";
        return;
    }


    cout << "Transfer Amount : ";
    cin >> amount;


    if(amount <= 0)
    {
        cout << "Invalid amount!\n";
        return;
    }


    if(amount > a.balance)
    {
        cout << "Insufficient Balance!\n";
        return;
    }


    double oldBalance = a.balance;


    // Deduct sender balance

    a.balance = a.balance - amount;


    // Add receiver balance

    accounts[receiverIndex].balance =
        accounts[receiverIndex].balance + amount;


    // Save account changes

    save();


    // Save sender transaction

    saveTransaction(
        a.accNo,
        "TRANSFER",
        amount,
        a.balance
    );


    // Save receiver transaction

    saveTransaction(
        accounts[receiverIndex].accNo,
        "RECEIVED",
        amount,
        accounts[receiverIndex].balance
    );


    cout << "\n";
    cout << "Transfer Successful!\n";

    cout << "Amount Transferred : "
         << amount << endl;

    cout << "Remaining Balance  : "
         << a.balance << endl;


    // Generate invoice

    createInvoice(
        "TRANSFER",
        a.accNo,
        a.name,
        amount,
        oldBalance,
        a.balance,
        receiver
    );
}


// ===============================
// USER MENU
// ===============================

void userMenu(int idx)
{
    int accountNumber = accounts[idx].accNo;


    while(true)
    {
        // Reload latest account information

        load();

        idx = findAcc(accountNumber);


        if(idx == -1)
        {
            cout << "Account error!\n";
            return;
        }


        cout << "\n";
        cout << "========================================\n";
        cout << "             SMART DIGITAL BANK\n";
        cout << "========================================\n";

        cout << "Welcome, "
             << accounts[idx].name
             << "!\n";

        cout << "----------------------------------------\n";

        cout << "1. Deposit\n";
        cout << "2. Withdraw\n";
        cout << "3. Transfer Money\n";
        cout << "4. Balance Enquiry\n";
        cout << "5. View Profile\n";
        cout << "6. Transaction History\n";
        cout << "7. Logout\n";

        cout << "----------------------------------------\n";

        cout << "Enter Choice : ";


        int choice;
        cin >> choice;


        // ===============================
        // DEPOSIT
        // ===============================

        if(choice == 1)
        {
            deposit(accounts[idx]);
        }


        // ===============================
        // WITHDRAW
        // ===============================

        else if(choice == 2)
        {
            withdraw(accounts[idx]);
        }


        // ===============================
        // TRANSFER
        // ===============================

        else if(choice == 3)
        {
            transferMoney(accounts[idx]);
        }


        // ===============================
        // BALANCE
        // ===============================

        else if(choice == 4)
        {
            cout << "\n";
            cout << "========== BALANCE ==========\n";

            cout << "Account Number : "
                 << accounts[idx].accNo << endl;

            cout << "Available Balance : "
                 << accounts[idx].balance << endl;
        }


        // ===============================
        // PROFILE
        // ===============================

        else if(choice == 5)
        {
            profile(accounts[idx]);
        }


        // ===============================
        // HISTORY
        // ===============================

        else if(choice == 6)
        {
            transactionHistory(accounts[idx].accNo);
        }


        // ===============================
        // LOGOUT
        // ===============================

        else if(choice == 7)
        {
            cout << "\nLogged Out Successfully!\n";
            break;
        }


        else
        {
            cout << "\nInvalid Choice!\n";
        }
    }
}


// ===============================
// MAIN FUNCTION
// ===============================

int main()
{
    while(true)
    {
        cout << "\n";
        cout << "========================================\n";
        cout << "     SMART DIGITAL BANK MANAGEMENT\n";
        cout << "========================================\n";

        cout << "1. Register New Account\n";
        cout << "2. Login\n";
        cout << "3. Exit\n";

        cout << "----------------------------------------\n";

        cout << "Enter Choice : ";


        int choice;
        cin >> choice;


        // Register

        if(choice == 1)
        {
            reg();
        }


        // Login

        else if(choice == 2)
        {
            int index = login();

            if(index != -1)
            {
                userMenu(index);
            }
        }


        // Exit

        else if(choice == 3)
        {
            cout << "\n";
            cout << "Thank You for Using Smart Digital Bank!\n";
            cout << "Have a Nice Day!\n";

            break;
        }


        else
        {
            cout << "\nInvalid Choice! Please Try Again.\n";
        }
    }


    return 0;
}