"""
BOFA APP
"""
import random
from datetime import datetime, timedelta

class Name:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

class ContactInfo:
    def __init__(self, email, number):
        self.email = email
        self.number = number

class AuthInfo:
    data = set()
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.data.add(self)

    def __hash__(self):
        return hash(f'{self.username} and {self.password}')
    
    def __eq__(self, object):
        if isinstance(object, AuthInfo):
            return self.username == object.username and self.password == object.password




class User:
    def __init__(self, name:Name, contact_info:ContactInfo, auth_info:AuthInfo):
        self.name = name
        self.contact_info = contact_info
        self.auth_info = auth_info

    def __hash__(self):
        return f'{self.last_name}, {self.first_name}'


class Date:
    def __init__(self):
        self.date = datetime.today()

    def future_date(self, years):
        return self.date + timedelta(years=years)
    
    def is_new_month(self):
        return self.day == 1


class Card:
    data = {}
    def __init__(self, user:User):
        self.user = user
        self.card_number = Card.__get_new_number(self)
        self.expiration_date = Date().future_date(5)
    @classmethod
    def __get_new_number(cls, card):
        while True:
            number = ''
            for _ in range(16):
                number += str(random.randInt(0, 9))
            if number not in cls.data:
                cls.data[number] = card
                return number
    
    def __hash__(self):
        return hash(f'{self.user}, {self.card_number}, {self.expiration_date}')
    
    def __eq__(self, object):
        if (isinstance(object, DebitCard) or isinstance(object, CreditCard)) and isinstance(object, self.__class__):
            return self.card_number == object.card_number

    
class DebitCard(Card):
    data = {}
    def __init__(self, user:User):
        super().__init__(user)
    

class CreditCard(Card):
    data = {}
    def __init__(self, user:User):
        super().__init__(user)
    


class Account:
    data = {}
    def __init__(self, user: User, balance):
        self.account_number = Account.__get_new_number(self)
        self.user = user
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance
    
    @classmethod
    def __get_new_number(cls, account):
        length = random.randint(12, 18)
        while True:
            number = ''
            for _ in range(length):
                number += str(random.randInt(0, 9))
            if number not in cls.data:
                cls.data[number] = account
                return number

class CheckingAccount(Account):
    data = {}
    def __init__(self, user:User, balance):
        super().__init__(user, balance)
        self.card = DebitCard(user)

    def deposit(self, amount, card):
        if self.card == card:
            self.balance += amount
            return self.balance
    
    def widthraw(self, amount, card):
        if self.card == card and amount < self.balance:
            self.balance-= amount
            return self.balance
    
    def transfer(self):
        ''
    
    def get_monthly_fee(self):
        if Date().is_new_month():
            if self.balance < 400:
                self.balance -= 20
    
    def is_under(self):
        return self.balance < 0
    
    @classmethod
    def remove_under_accounts(cls):
        for key, value in cls.data.items():
            if value.is_under():
                del cls.data[key]
        

    
    

class SavingAccont(Account):
    data = {}
    def __init__(self, user:User, interest, balance):
        super().__init__(user, balance)
        self.interest = interest
    

    

    



    


    




    
