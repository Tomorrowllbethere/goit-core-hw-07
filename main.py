from collections import UserDict
import re   
import datetime as dt
from datetime import datetime as dtdt
# основа
class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    def get_name(self):
        
        return Name(self.name)

class Phone(Field):                   
    def __init__(self, value): # реалізація класу Phone:
         self.value = value                              
# довести до пуття. лише імпортовано/ update: прописано. потребує тестування
    def get_phone(self):
        if  self.value.isdigit():
            pattern_delete = r"[^\d]"   # створення патерну для відкидання зайвих елементів
            replacement_symbol = "" 
            number_just = re.sub(pattern_delete, replacement_symbol, self.value) #видалення будь-яких знаків, окрім цифр
            number_just = number_just.split("0", maxsplit=1) #розділення рядків за 0
            number_just[0] = "+380" # заміна першого підрядка
            self.value = "".join(number_just) #об'єднання рядків
            return self.value
        else:
            print('Inwalid phone number')
    


# тільки база класу. 
# class Birthday(Field):
    # def __init__(self, value):
    #     try:
    #         # Додайте перевірку коректності даних
    #         # та перетворіть рядок на об'єкт datetime
    #     except ValueError:
    #         raise ValueError("Invalid date format. Use DD.MM.YYYY")


# додати функцію запису дн
class Record():
    # реалізація класу
    def __init__(self, name):
        self.name = Name(name)  # Реалізовано зберігання об'єкта Name в окремому атрибуті.
        self.phones = []  # Реалізовано зберігання списку об'єктів Phone в окремому атрибуті.
        self.birthday = None

# додавання 
    def add_phone(self, phone):
        phone_valid = Phone(phone).get_phone() #
        if phone_valid: #
            self.phones.append(phone_valid)
            
# видалення
    def remove_phone(self, phone): 
        phone_obj = Phone(phone).get_phone()
        self.phones.remove(phone_obj)

# редагування 
    def edit_phone(self, phone, new_phone): 
        new_phone_obj = Phone(new_phone).get_phone()
        if phone in self.phones: #
            self.phones.remove(phone) 
            self.phones.append(new_phone_obj)
            print("Changes made")
            return self.phones
        else:
            print(" Phone is not in list")
            return None
                
# пошук об'єктів Phone
    def find_phone(self, phone):
        phone_obj = Phone(phone).get_phone()
        if phone_obj in self.phones:
            return self.phones
        else:
            print ("Don't find this number")

    def __str__(self):
        return f"\nIt's automatically printed.\nContact name: {self.name}, phones: {self.phones}\n"


# додати функцію з пошуком найближчих днів народжень
class AddressBook(UserDict):
    def __init__(self):
        self.data={} # словник- книга контактів

 # Реалізовано метод add_record, який додає запис до self.data.  
    def add_record(self, contact):
        self.data[str(contact.name)] = contact.phones
        print(f"Contact added. \nName: {contact.name}, phones: {contact.phones}")
        return self.data
    
# Реалізовано метод find, який знаходить запис за ім'ям.
    def find(self, name):
        self.name = name
        for key, value in self.data.items():
            if self.name in str(key):
                print(f"Contact found. \nName: {name}, phones: {value}")
                p = Record(name) #реалізація Record-обєкту
                p.name = name 
                p.phones = value
                return p       # повернення Record() обєкту
            else:
                print (f"Don't find this name: {name}")
                return None
    
# Реалізовано метод delete, який видаляє запис за ім'ям.
    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
            print(f"Record for '{name}' deleted successfully.")
        else:
            print(f"Record for '{name}' not found in the address book.")
        
# зразки виклику класів. потребує стоврення нормальної комунікації без лишніх викликів
# book = AddressBook()
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("0004567890")
# # Додавання запису John до адресної книги
# book.add_record(john_record)
# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)
# # Виведення всіх записів у книзі
# for name, record in book.data.items():
#     print(name," ----",record)
# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")
# print(john)  # Виведення: Contact name: John, phones: ['0004567890', '1112223333']
# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("1112223333")
# print(f"{john.name}: {found_phone}")  # Виведення: John: ['0004567890', '1112223333']
# # Видалення запису Jane
# book.delete("Jane")
# print(book)






def parse_input(user_input): #функція, яка приймає введений рядок. ділить та сортує дані.
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func): # декоратор- обробка помилок при введенні
    def inner(args, contacts):
        try:
            name:str = args[0]
            if name in contacts:
                print("\nThis name is in your contacts\n") 
                if len(args) == 1:
                    return func(args, contacts)
                else:
                    if args[1].isdigit():
                        return func(args, contacts)
                    else:
                        return "\n->Phone number must contain only numbers."
            else:
                return func(args, contacts) 
            
        except ValueError:
            return "\n->Give me name and phone please."
        except KeyError:
            return "\n->Is a key error. You should check it and repeat."
        except IndexError:
            return "\n->What's wrong?\nRepeat this, correctly please."
            # return "Phone must be a number"
    return inner

 

def main():#основна функція
    contacts  = AddressBook()
    help: list=[
        ['add (name) (phone)   ->for add a new contacts to me'],
        ['change (name) (old_phone) (new phone) -> for change contacts i have'],
        ['all                  -> to see all contacts i save'],
        ['delete (name)        -> to delete one contact'],
        ['show (name)          -> to see number of somebody']
        ]
    print("_____________\nHello. \nI'm glad to see you")
    print("\nI have some list of commands. If you need this - enter help\n")
    while True:
        # try:
            user_input  = input("\n>>>Enter a command: ")
            command, *args = parse_input(user_input)
            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                sm_record = Record(args[0])
                sm_record.add_phone(args[1])
                # Додавання запису John до адресної книги
                contacts.add_record(sm_record)
            elif command == "change":
                search = contacts.find(args[0])
                search.edit_phone(args[1], args[2])
            elif command == "all":
                for name, record in contacts.data.items():
                    print(name," ----",record)
            elif command == "show":
                print (show_phone(args, contacts))
            elif command == "delete":
                
                print(delete_name(args, contacts))
            elif command == "help":
                for el in help:
                    print(el)
            else:
                print("Invalid command.\nTry one more time")
        # except Exception as e:
            # print("there are something wrong",f" \n{e}", "\n Plese, try again.")


# \\\\\\ код привітання з дн на 7 днів вперед з різницею від словника з датами

def get_upcoming_birthdays(users=None):
    tdate=dtdt.today().date() # беремо сьогоднішню дату
    upcoming_birthdays=[] # створюємо список для результатів
    for user in users: # перебираємо користувачів
        bdate=user["birthday"] # отримуємо дату народження людини у вигляді рядка
        bdate=str(tdate.year)+bdate[4:] # Замінюємо рік на поточний
        bdate=dtdt.strptime(bdate, "%Y.%m.%d").date() # перетворюємо дату народження в об’єкт date
        week_day=bdate.isoweekday() # Отримуємо день тижня (1-7)
        days_between=(bdate-tdate).days # рахуємо різницю між зараз і днем народження цьогоріч у днях
        if 0<=days_between<7: # якщо день народження протягом 7 днів від сьогодні
            if week_day<6: #  якщо пн-пт
                upcoming_birthdays.append({'name':user['name'], 'birthday':bdate.strftime("%Y.%m.%d")}) 
                # Додаємо запис у список.
            else:
                if (bdate+dt.timedelta(days=1)).weekday()==0:# якщо неділя
                    upcoming_birthdays.append({'name':user['name'], 'birthday':(bdate+dt.timedelta(days=1)).strftime("%Y.%m.%d")})
                    #Переносимо на понеділок. Додаємо запис у список.
                elif (bdate+dt.timedelta(days=2)).weekday()==0: #якщо субота
                    upcoming_birthdays.append({'name':user['name'], 'birthday':(bdate+dt.timedelta(days=2)).strftime("%Y.%m.%d")})
                    #Переносимо на понеділок. Додаємо запис у список.
    return upcoming_birthdays


# \\\\


if __name__ == "__main__":
    main()