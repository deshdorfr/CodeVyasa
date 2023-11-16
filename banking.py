import random

# Domain Layer
class Account:
    def __init__(self, account_id, customer_id, account_number, balance=0):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than 0.")
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Insufficient funds")

    def get_balance(self):
        return self.balance


class Customer:
    def __init__(self, customer_id, name, email, phone_number):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone_number = phone_number


class CreateAccountUseCase:
    def generate_account_id(self):
        # Generate a random 16-digit account_id
        return str(random.randint(10**15, 10**16 - 1))

    def generate_account_number(self):
        # Generate a random 16-digit account_number
        return str(random.randint(10**15, 10**16 - 1))

    def create_account(self, customer_id, name, email, phone_number):
        if not name or not email or not phone_number:
            raise ValueError("Name, email, and phone number are required for creating an account.")
        
        account_id = self.generate_account_id()
        account_number = self.generate_account_number()
        # account_holder_name = self.get_account_holder_name(name)
        customer = Customer(customer_id, name, email, phone_number)
        return Account(account_id, customer_id, account_number)


class TransactionUseCase:
    def make_transaction(self, account, amount, transaction_type):
        if amount <= 0:
            raise ValueError("Transaction amount must be greater than 0.")
        
        if transaction_type not in ['deposit', 'withdraw']:
            raise ValueError("Invalid transaction type. Supported types: 'deposit' and 'withdraw'.")
        
        if transaction_type == 'withdraw' and account.get_balance() < amount:
            raise ValueError("Insufficient funds for withdrawal.")
        
        if transaction_type == 'deposit':
            account.deposit(amount)
        elif transaction_type == 'withdraw':
            account.withdraw(amount)


# Use Case Layer
class AccountStatementUseCase:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def generate_account_statement(self, account_id):
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise ValueError("Account not found.")
        
        # Logic to retrieve transaction details for the account and format as a statement
        statement = "Account Statement for Account ID: {}\n".format(account_id)
        # Add transaction details here
        return statement


# Infrastructure Layer
class AccountRepository:
    def __init__(self):
        self.accounts = []

    def save_account(self, account):
        self.accounts.append(account)

    def find_account_by_id(self, account_id):
        for account in self.accounts:
            if account.account_id == account_id:
                return account
        return None

    def find_accounts_by_customer_id(self, customer_id):
        return [account for account in self.accounts if account.customer_id == customer_id]


# Test Scenario
def test_banking_system():
    # Create an instance of the Repository class
    account_repository = AccountRepository()

    # Create instances of Use Case classes with dependencies
    create_account_use_case = CreateAccountUseCase()
    transaction_use_case = TransactionUseCase()

    # Pass the account_repository to the AccountStatementUseCase constructor
    account_statement_use_case = AccountStatementUseCase(account_repository)

    try:
        # Create a new account
        customer_details = Customer(1, "deshdeepak", "desh13031992@gmail.com", "8756166528")
        new_account = create_account_use_case.create_account(
            customer_id=1,
            name=customer_details.name,
            email=customer_details.email,
            phone_number=customer_details.phone_number
        )

        # Save the account to the repository
        account_repository.save_account(new_account)

        # Make a deposit
        transaction_use_case.make_transaction(new_account, amount=1000, transaction_type='deposit')

        # Generate account statement
        statement = account_statement_use_case.generate_account_statement(new_account.account_id)

        # Display results
        print("==================== Account Details ==========================")
        print("name:", customer_details.name)
        print("email:", customer_details.email)
        print("email:", customer_details.phone_number)
        print("Balance after transactions:", new_account.get_balance())
        print(statement)
        print("===============================================================")

    except ValueError as error:
        print(f"Error: error")


# Run the test scenario
test_banking_system()
