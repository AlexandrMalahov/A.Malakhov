"""Bank account."""


class BankAccount(object):
    """Creation and management of personal bank account."""

    balance = 0
    # bank account balance

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "%s's account. Balance: $%.2f" % (self.name, self.balance)

    def show_balance(self):
        """ Balance display."""

        print "Balance: $%.2f" % (self.balance)

    def deposit(self, amount):
        """Taking deposits."""

        if amount <= 0:
            print "Some error message here"
            return
        else:
            print "Deposit balance: $%.2f" % (amount)
            self.balance += amount
            self.show_balance()

    def withdraw(self, amount):
        """Withdrawal authorization."""

        if amount > self.balance:
            print "Some error message here"
            return
        else:
            print "Amount: $%.2f" % (amount)
            self.balance -= amount
            self.show_balance()


MY_ACCOUNT = BankAccount('Stephen')
print MY_ACCOUNT
MY_ACCOUNT.show_balance()
MY_ACCOUNT.deposit(2000)
MY_ACCOUNT.withdraw(1000)
print MY_ACCOUNT
