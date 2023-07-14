import json
import random
from datetime import datetime


class InvalidArgumentError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

    def __eq__(self, other):
        return self.message == other.message

    def __hash__(self):
        return hash(self.message)

class Bank:
    def __init__(self, name, date_of_birth, balance=0, offical=False):
        self.user_config = {}
        self.name = name
        self.date_of_birth = date_of_birth
        self.balance = balance
        self.depo_rate = None

        if offical:
            self.json = 'officals'
        else:
            self.json = 'users'

        self.pk = None  # Initialize pk to None

        if self.verify():
            self.pk = self.verify()  # Assign the correct pk if the user is found
        else:
            self.register()  # Register the user if not found
        
        self.bal_check()
        self.sus_check()
        self.depo_rate = self.depo_check()

    def __repr__(self) -> str:
        return self.name

    def depo_check(self):
        if self.show('deposit') == "False":
            return random.randint(50, 60)
        else:
            return 5

    def sus_check(self):
        if self.show('sus') > 5:
            self.change('deposit', 'False')
        elif self.show('sus') == 5:
            self.change('deposit', 'False')
        elif self.show('sus') < 5:
            self.change('deposit', 'True')

    def bal_check(self):
        if self.show_balance() <= 50000:
            self.change('loan_payble', 'False')
        else:
            self.change('loan_payble', 'True')

    def fine(self):
        val = self.gst_add(self.show_balance(), 60, add=True)
        trans = Transaction(self, Bank_Officals["fine"], val)
        trans.transfer(self.upi_pin_show(), m=True)
        self.change('sus', 0)

    def online_payment(self, amount, wendor):
        with open('core/storage/users.json', 'r') as fs:
            user_data = json.load(fs)
            name = input('Enter Your Name: ')
            pin = input('Enter your PIN: ')
            for user in user_data:
                if user_data[user]["name"] == name and user_data[user]["pin"] == pin:
                    user = Bank(name, user_data[user]["date_of_birth"])
                    trans = Transaction(user, wendor, amount)
                    trans.transfer(user.upi_pin_show())
                    print(f'Transaction Successful!')
               

    def loan_status(self):
        with open('core/storage/users.json', 'r') as f:
            users = json.load(f)
        
        if users[self.pk]['loan_payble'] == "False":
            return False
        elif users[self.pk]['loan_payble'] == "True":
            return True

    def upi_pin_generate(self, **kwargs):
        """
        Generates a 4 digit UPI PIN
        """
        pin = None
        if 'pin' in kwargs:
            pin = str(kwargs['pin'])
            if len(pin) == 4:
                pin = str(pin)
            else:
                raise ValueError('Invalid pin Pin Should Be 4 Digits')
        else:
            pin = str(random.randint(1000, 9000))

        with open(f'core/storage/{self.json}.json', 'r') as users:
            user = json.load(users)
            user[self.pk]["pin"] = pin
        with open(f'core/storage/{self.json}.json', 'w') as users:
            json.dump(user, users, indent=5)

        return pin

    def upi_pin_show(self):
        """
        Generates a 4 digit UPI PIN
        """
        with open(f'core/storage/{self.json}.json', 'r') as users:
            user = json.load(users)
            return user[self.pk]["pin"]

    def verify(self):
        with open(f'core/storage/{self.json}.json', 'r') as f:
            self.user_config = json.load(f)
            for i in self.user_config:
                if self.user_config[i]["name"] == self.name and self.user_config[i]["date_of_birth"] == self.date_of_birth:
                    return i  # Return the found primary key

    def to_json(self):
        return {
            'name': self.name,
            'date_of_birth': self.date_of_birth,
            'balance': self.balance,
            "sus": 0,
            "loan_payble": "True",
            "deposit": "True",
            "pin": 0000
        }

    def register(self):
        with open(f'core/storage/{self.json}.json', 'r') as f:
            self.user_config = json.load(f)

            # Generate a new primary key
            self.pk = str(len(self.user_config) + 1)

            self.user_config[self.pk] = self.to_json()

            with open(f'core/storage/{self.json}.json', 'w') as f:
                json.dump(self.user_config, f, indent=5, default=str)


    def change(self, change, value, add=False, sub=False):
        with open(f'core/storage/{self.json}.json', 'r') as f:
            self.user_config = json.load(f)

        if add:
            self.user_config[self.pk][change] += value
        elif sub:
            self.user_config[self.pk][change] -= value
        else:
            self.user_config[self.pk][change] = value

        with open(f'core/storage/{self.json}.json', 'w') as f:
            json.dump(self.user_config, f, indent=5)


    def show(self, value):
        with open(f'core/storage/{self.json}.json', 'r') as f:
            data = json.load(f)

        return data[self.pk][f"{value}"]

        
    def gst_add(self, amount, rate,  add=False, sub=False):
        percent =  (rate / 100) * amount
        result = None
        with open('core/storage/Gst.json', 'r') as f:
            self.gst = json.load(f)
            self.gst["amount"] += round(percent)
        with open('core/storage/Gst.json', 'w') as f:
            json.dump(self.gst, f, indent=5)

        if add:
            result = round(amount + percent)
        elif sub:
            result = round(amount - percent)


        return result

    def deposit(self, amount, no_gst=False):
        if self.show('deposit') == "True":
            if amount >= 100000 and amount < 300000:
                self.change('sus', 1, add=True)
                if no_gst:
                    self.change('balance', amount, add=True)
                else:
                    amount_to_be_added = self.gst_add(amount, 5, sub=True)
                    self.change('balance', amount_to_be_added, add=True)
            elif amount > 300000:
                self.change('sus', 5, add=True)
                if no_gst:
                    self.change('balance', amount, add=True)
                else:
                    amount_to_be_added = self.gst_add(amount, 10, sub=True)
                    self.change('balance', amount_to_be_added, add=True)
            else:
                self.change('balance', amount, add=True)
        else:
            amount_to_be_added = self.gst_add(amount, self.depo_rate, sub=True)
            self.change('balance', amount_to_be_added, add=True)

    def withdraw(self, amount, m=False):
        if m == False:
            if amount <= self.show_balance():
                self.change('balance', amount, sub=True)
            else:
                raise ValueError('Insufficient Balance')
        else:
            self.change('balance', amount, sub=True)

    def show_balance(self):
        with open(f'core/storage/{self.json}.json', 'r') as f:
            self.user_config = json.load(f)
            balance = self.user_config[self.pk]['balance']
            return balance

    def show_transactions(self):
        with open('core/storage/transaction.json', 'r') as f:
            self.trasactions = json.load(f)
            transactions = []
            for _ in self.trasactions:
                if self.trasactions[_]["sender"] == self.name or self.trasactions[_]["receiver"] == self.name:
                    transactions.append(self.trasactions[_])

            if len(transactions) != 0:
                for i in transactions:
                    print(i)
            else:
                print('No transactions found')

            return 'It Already Have Print Function In It'

    def info_change(self, value_to_be_chaged, value, pin):
        if pin == self.upi_pin_show():
            if value_to_be_chaged != 'balance':
                self.change(value_to_be_chaged, value)
            else:
                raise InvalidArgumentError(
                    "In Vaild Value To Be Changed (Balance Can't Be Changed)")
        else:
            raise ValueError('Invalid Pin')


class Transaction(Bank):
    def __init__(self, sender, receiver, amount, no_gst=False):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.no_gst = no_gst
        self.pk = self.make_pk(

        )

    def make_pk(self):
        with open('core/storage/transaction.json', 'r') as transaction:
            transactions = json.load(transaction)
            pk = str(len(transactions) + 1)
            return pk

    def transfer(self, upi_pin = '', m=False, u=False):
        if u == False:
            if str(upi_pin) == self.sender.upi_pin_show():
                    if m:
                        self.sender.withdraw(self.amount, m=True)
                    else:
                        self.sender.withdraw(self.amount, m=False)
                        self.receiver.deposit(self.amount)
                        
            else:
                raise ValueError('Invaild Pin')
        else:
            self.sender.withdraw(self.amount, m=False)
            self.receiver.deposit(self.amount)
            self.to_json()

    def __repr__(self) -> str:
        return f'{self.sender.name} -> {self.receiver.name}: {self.amount}'

    def to_json(self):
        with open('core/storage/transaction.json', 'r') as f:
            self.transaction_config = json.load(f)

        self.transaction_config[self.pk] = {
            'sender': self.sender.name,
            'receiver': self.receiver.name,
            'amount': self.amount
        }

        with open('core/storage/transaction.json', 'w') as f:
            json.dump(self.transaction_config, f, indent=5)


class Loan(Bank):
    def __init__(self, person, amount, item_to_be_kept, Bank_Officials):
        self.amount = amount
        self.person = person
        self.item_to_be_kept = item_to_be_kept
        self.Bank_Officials = Bank_Officials
        self.rate = self.rate_generate()

        if self.verify():
            self.pk = self.verify()  # Assign the correct pk if the loan is found
        else:
            self.pk = self.make_pk()  # Generate a new primary key for the loan


    def __repr__(self) -> str:
        return f"Loan: {self.person} ->> {self.amount}"

    def rate_generate(self):
            return random.randint(10, 25)

    def make_pk(self):
        with open('core/storage/loan.json', 'r') as transaction:
            transactions = json.load(transaction)
            pk = str(len(transactions) + 1)
            return pk

    def verify(self):
        with open('core/storage/loan.json', 'r') as loan:
            loans = json.load(loan)
            for i in loans:
                if loans[i]["person"] == self.person.name and loans[i]["loan_remaining"] != 0:
                    return i  # Return the found primary key if the loan is found

    def loan(self):
        if self.person.loan_status():
            Trans = Transaction(self.Bank_Officials['loan'], self.person, self.amount)
            Trans.transfer(self.Bank_Officials['loan'].upi_pin_show())
            self.to_json()
        else:
            raise InvalidArgumentError('You Don"t Have Enough Balance To Take Loans From This Bank')

    def gst_adds(self, amount, rate, add=False, sub=False):
        percent =  (rate / 100) * amount
        with open('core/storage/Gst.json', 'r') as f:
            self.gst = json.load(f)
            self.gst["amount"] += round(percent)
        with open('core/storage/Gst.json', 'w') as f:
            json.dump(self.gst, f, indent=5)

        if add:
            result = round(amount + percent)
        elif sub:
            result = round(amount - percent)

        return result

    def remaining(self):
        with open('core/storage/loan.json', 'r') as f:
            self.loan_config = json.load(f)
            loan_paid = self.loan_config[self.pk]['loan_paid']
            amount = self.gst_adds(self.amount, self.rate, add=True)
            self.loan_config[self.pk]['loan_remaining'] = amount - loan_paid

        with open('core/storage/loan.json', 'w') as f:
            json.dump(self.loan_config, f, indent=5)

    def loan_payment(self, payment):
        with open('core/storage/loan.json', 'r') as f:
            self.loan_config = json.load(f)
            
        if self.pk in self.loan_config:
            if self.loan_config[self.pk]['loan_remaining'] == 0:
                raise ValueError('Loan Already Paid')
            else:
                if self.person.show_balance() >= payment:
                    self.loan_change('loan_remaining', payment, sub=True)
                    self.loan_change('loan_paid', payment, add=True)
                    Transfer = Transaction(self.person, self.Bank_Officials['loan'], payment)
                    Transfer.transfer(self.person.upi_pin_show(), no_gst=False)
                else:
                    raise ValueError('Insufficient Balance')
        else:
            raise ValueError('Loan not found')

    def to_json(self):
        with open('core/storage/loan.json', 'r') as f:
            self.loan_config = json.load(f)

            self.loan_config[self.pk] = {
                'person': self.person.name,
                'amount': self.amount,
                'loan_rate': self.rate,
                'item_to_be_kept': self.item_to_be_kept,
                'loan_paid': 0,
            }

        with open('core/storage/loan.json', 'w') as f:
            json.dump(self.loan_config, f, indent=5)

        self.remaining()

    def loan_change(self, change, value, add=False, sub=False):
        with open('core/storage/loan.json', 'r') as f:
            self.loan_config = json.load(f)

        if add:
            self.loan_config[self.pk][change] += value
        elif sub:
            self.loan_config[self.pk][change] -= value
        else:
            self.loan_config[self.pk][change] = value

        with open('core/storage/loan.json', 'w') as f:
            json.dump(self.loan_config, f, indent=5)



Samad = Bank('Abdus Samad', '09/10/2009', 0)
New_User = Bank('New_User', '10/2/2014', 100)
Golu = Bank('Golu', '3/5/2013', 0)
none = Bank('None', 'N/A', 0)
Hussain = Bank('Hussain', '09/03/2003')
Zainab = Bank('Zainab', '09/12/2014', 0)


# -----------------------------------------------------------------------

Mishra_Ji = Bank('Mishra_Ji', '10/09/2009', 10000000, offical=True)

Chacha = Bank('Chacha', '0/0/0', 100000000, offical=True)

Officer = Bank('Officer', '09/04/2014', 99999999, offical=True)

Bank_Officals = {
    "loan": Chacha,
    "fine": Officer,
}


# -----------------------------------------------------------------------