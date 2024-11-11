import random
import string
import sys


class IdGenerator:
   def __init__(self):
       self.id_list = set()
       self.workers_id = set()
       self.number = 0


   def __create_new_id(self):
       id = ''
       for _ in range(3):
           id += str (random.randint(0, 9))
       for _ in range (4):
           letters = string.ascii_letters
           id += letters[random.randint(0, 51)]
       return id


   def get_validated_id(self):
       id = self.__create_new_id()
       while id in self.id_list:
           id = self.__create_new_id()
       self.id_list.add(id)
       return id
  
   def __create_worker_id(self):
       id = ''
       for _ in range(9):
           id += str (random.randint(0, 9))
       return id
   def get_validated_worker_id(self):
       id = self.__create_worker_id()
       while id in self.workers_id:
           id = self.__create_worker_id()
       self.workers_id.add(id)
       return id


  
   def create_new_store_number(self):
       self.number += 1
       return self.number
  
class Store:
   id_generator = IdGenerator()
   types = {}
   def __init__(self):
       self.number = self.id_generator.create_new_store_number()
       self.types[self.number] = self
       self.departments = set()




   @classmethod
   def create_or_get(cls, store):
       if store not in cls.types:  
           cls.types[store] = Store()
       return cls.types[store]
  
  
   def __eq__(self, object):
       if isinstance(object, Store):
           return self.number == object.number
      
   def __hash__(self) -> int:
       return hash(self.number)
  
   def __repr__(self) -> str:
       return f'Store #{self.number}'




class ProductSection:
   types = {}
   def __init__(self, name, store):
       self.name = name
       self.store = Store.create_or_get(store)
       self.sections = set()
       self.store.departments.add(self)
  
   @classmethod
   def create_or_get(cls, name, store):
       if name not in cls.types:  
           cls.types[name] = ProductSection(name, store)
       return cls.types[name]


   def __str__(self):
       return f'{self.name}: {self.sections}'
  
   def __eq__(self, object):
       if isinstance(object, ProductSection):
           if self.name == object.name and self.store == object.store:
               return True
       return False
  
   def __hash__(self) -> int:
       return hash(self.name)
  
   def __repr__(self) -> str:
       return f'{self.name}'
  




class ProductType:
   types = {}
   def __init__(self, name, section, store):
       self.name = name
       self.section = ProductSection.create_or_get(section.lower(), store)
       self.products = set()
       self.types[name] = self
       self.section.sections.add(self)
  
   @classmethod
   def create_or_get(cls, name, section, store):
       if name not in cls.types:  
           cls.types[name] = ProductType(name, section, store)
       return cls.types[name]


   def __str__(self):
       return f'{self.name}: {self.products}'
  
   def __eq__(self, object):
       if isinstance(object, ProductType):
           if self.name == object.name:
               return True
       return False
  
   def __hash__(self) -> int:
       return hash(self.name)
  
   def __repr__(self) -> str:
       return f'{self.name}'
  
  
  
class Product:
   id_generator = IdGenerator()
   def __init__(self, name, price, parent, brand, section, store):
       self.id = self.id_generator.get_validated_id()
       self.name = name
       self.price = price
       self.brand = brand
       self.parent = ProductType.create_or_get(parent.lower(), section, store)
       self.parent.products.add(self)
       self.section = ProductSection.create_or_get(section.lower(), store)
       self.store = Store.create_or_get(store)


   def __hash__(self) -> int:
       return hash((self.name, self.brand))
  
   def __eq__(self, value: object) -> bool:
       if self.name == value.name and self.brand == value.brand:
           return True
       return False


   def __repr__(self) -> str:
       return f'{self.brand} {self.name}'


   def __str__(self):
       return f'Product Id: {self.id} -> {self.name} costs ${self.price}'
  


class ProductInventory:
   def __init__(self, store):
       self.__products = {}
       self.store = Store.create_or_get(store)


   @property
   def products(self):
       return self.__products
  
   def view(self, product):
       return self.products[product]
  
   def add(self, product, number):
       quantity = self.products.get(product, 0)
       self.products[product] = number + quantity
  
   def update(self, product, number):
       self.products[product] = number
  
   def delete(self, product, number):
       quantity = self.products.get(product, 0)
       self.products[product] = number - quantity
       if self.products[product] < 0:
           self.products[product] = 0
  
   def destroy(self, product):
       del self.products[product]



'''
end of the inventory clas
staring the worker and the APP class 
'''

class Worker:
    id_generator = IdGenerator()
    workers = set()
    def __init__(self, name, level, store, username, password):
        self.name = name
        self.id = self.id_generator.get_validated_worker_id()
        self.position = Position(level)
        self.auth_info = WorkerAuthInfo(username, password, self)
        self.store = Store.create_or_get(store)
        self.workers.add(self)
    
        @classmethod
        def create_new_worker(cls, name, level, store):
            worker = cls(name, level, store)
    
        @classmethod
        def remove_worker(cls, worker):
            cls.workers.remove(worker)


        def __repr__(self):
            return f'Worker ID#{self.id} -> {self.name} level.{self.position} working for Store#{self.store}'
        
        def __str__(self):
            return f'Worker ID#{self.id} -> {self.name} level.{self.position} working for Store#{self.store}'

        def __hash__(self):
            return hash((self.id, self.name))
        
        def __eq__(self, value):
            if isinstance(value, Worker):
                return self.id == value.id

class AuthInfo:
    database = {}
    auth_info = {'username':set(), 'password': set()}
    def __init__(self, username, password, worker=None):
        self.__username = username
        self.__password = password
        self.worker = worker

    @property
    def username(self):
        return self.__username
    
    @property
    def password(self):
        return self.__password
    
    def __eq__(self, value):
        if isinstance(value, AuthInfo) or isinstance(value, AuthInfoChecker) or isinstance(value, WorkerAuthInfo):
            return self.username == value.username and self.password == value.password
    
    def __hash__(self) -> int:
        return hash((self.username, self.password))

    def __repr__(self) -> str:
        return f'(username: {self.username}, passowrd: {self.password})'
    
    def __str__(self):
        return f'username: {self.username}, passowrd: {self.password}'

class AuthInfoChecker(AuthInfo):
    ''
    def get_worker(self):
        return self.__class__.database.get(self, None) 

class WorkerAuthInfo(AuthInfo):
    def __init__(self, username, password, worker):
        super().__init__(username, password)
        self.worker = worker
        self.__class__.database[self] = worker
        username_set = self.__class__.auth_info['username']
        username_set.add(self.username)
        password_set = self.__class__.auth_info['password']
        password_set.add(self.password)






  


class Position:
   def __init__(self, level):
       self.level = level


   def actions(self):
       action = [Action('view', ProductInventory), Action('add', ProductInventory), Action('update', ProductInventory), Action('delete', ProductInventory), Action('destroy', ProductInventory), Action('add', Worker), Action('remove', Worker)]
       result = []
       for index, act in enumerate(action):
           if self.level >= index:
               result.append(act)
       return result
  
   def __str__(self):
       return f'{self.level}'
  
   def __repr__(self):
       return self.__str__()


class Action:
   def __init__(self, name, data):
       self.name = name
       self.data = data


   def perform_action(self, action, instance, args):
       action_map = {}
       if isinstance(instance, ProductInventory):
           action_map = {
               Action('view', ProductInventory): instance.view,
               Action('add', ProductInventory): instance.add,
               Action('update', ProductInventory): instance.update,
               Action('delete', ProductInventory): instance.delete,
               Action('destroy', ProductInventory): instance.destroy,
           }
       elif isinstance(instance, Worker):
           action_map = {
               Action('add', Worker): instance.create_new_worker,
               Action('remove', Worker): instance.remove_worker,
           }
       action_map[action](*args)


   def __hash__(self):
       return hash((self.name, self.data))


   def __repr__(self) -> str:
       return f'{self.name}'
   def __eq__(self, value):
       if isinstance(value, Action):
           return self.name == value.name and self.data == value.data
      
class Stack:
   def __init__(self):
       self.__data = []
       self.__size = 0
   @property
   def size(self):
       return self.__size
  
   @size.setter
   def size(self, value):
       self.__size += value
      
   def push(self, value):
       self.__data.append(value)
       self.size = 1
   def pop(self):
       self.size = -1
       return self.__data.pop()
   def peek(self):
       return self.__data[self.size-1] if self.size > 0 else None
   def is_empty(self):
       return self.size == 0
    
  
class Page:
   def __init__(self, name, page):
       self.name = name
       self.page = page
   def __eq__(self, value):
       if isinstance(value, Page):
           return self.name == value.name
   def __repr___(self):
       return f'{self.name}'
   def __str__(self) -> str:
       return f'{self.name}'
  
class App:
   def __init__(self):
       self.history = Stack()
   def create_username(self):
       pass
   def create_password(self):
       pass
   def welcome_page(self):
       self.history.push(Page('welcome page', self.welcome_page))
       while True:
           print('Welcome to Inventory Tracker!')
           centinel = input('Enter any key to continue or "leave" to quit: ')
           if centinel == 'leave':
               sys.exit()
           break
   def login(self):
    while True:
       self.history.push(Page('login', self.login)) 
       username = input('Enter your username: ')
       password = input('Enter your password: ')
       auth_info = AuthInfoChecker(username, password)
       worker = auth_info.get_worker()
       if worker is not None:
        print(f'Welcome {worker.name} level.{worker.position} to Inventory. What would you like to do?') 
        break
       else:
        print('Invalid credentials!')  
   def create(self):
       self.history.push(Page('create', self.create))
       name, level, store =  self.__get_new_worker_info()
       while True:
            username = input('Enter your username: ')
            password, re_password = self.__get_passwords()
            if re_password == password:
                'check if the username is in the db and password' 
                if username in AuthInfo.auth_info['username']:
                    print('Username already in use!')
                    username = input('Enter your username: ')
                elif password in AuthInfo.auth_info['password']:
                    print('Password already in use!')
                    password, re_password = self.__get_passwords()
                else:
                    print('New Worker Created!')
                    new_worker = Worker(name, level, store, username, password)
                    print('Login')
                    self.login()
                    break
            else:
                print('Passwords do not match!')
                password, re_password = self.__get_passwords()
   def __get_passwords(self):
        password = input('Enter your password: ')
        re_password = input('Re-enter your password: ')
        return (password, re_password)
   def __get_new_worker_info(self):
    name = input('Enter your name: ')
    level = input('Enter your level: ')
    store = input('Enter your store number: ')
    while True:
        try: 
            level = int(level)
            break
        except TypeError:
            print('Enter level as numbers from 0-6.')
            level = input('Enter your level: ')
    return (name, int(level), int(store))
   def run(self):
       order = [('welcome page', self.welcome_page),('login or create', self.login_or_create_accont)]
       while True:
           for page in order:
               page = Page(page[0], page[1])
               if  self.history.peek() == page:
                    continue
               page.page()


   def login_or_create_accont(self):
       self.history.push(Page('login or create', self.login_or_create_accont))
       choice = input('Enter "login" to login, "create" to create new account, or "cancel" to go back: ')
       choice = choice.lower()
       page = None
       while True:
           if choice == 'login':
               self.login()
               break
           elif choice == 'create':
               self.create()
               break
           elif choice == 'cancel':
               self.history.pop()
               page = self.history.peek()
               break
           else:
               choice = input('Enter a valid Command! Enter "login" to login, "create" to create new account, or "cancel" to go back: ')
       if page != None:
           page.page()
      
      


worker = Worker('mo', '2', 1, 'moman', '1234')

print(AuthInfo.database)

application = App()


application.run()



