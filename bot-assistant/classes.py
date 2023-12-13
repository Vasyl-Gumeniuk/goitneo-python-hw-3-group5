import pickle
from datetime import datetime, date



class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)



class Name(Field):
    def __init__(self, value: str):
        super().__init__(value)



class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:    
            raise ValueError("The phone number must consist of 10 digits")
        

class Birthday(Field):
    def __init__(self, value: str):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            super().__init__(value)
        except ValueError:
            raise ValueError("The date must be in format: 'DD.MM.YYYY'!")



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_phone(self, phone):
        self.phones.append(Phone(phone))


    def remove_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)
                return f'The number "{i}" was succesfuly removed!'
        return f'The number "{phone}" does not exist!'
    

    def edit_phone(self, old_phone, new_phone):
        for i in self.phones:
            if i.value == old_phone:
                i.value =  Phone(new_phone).value
                return f'The number "{old_phone}" was succesfuly updated to "{new_phone}"!'
        return f'The number "{old_phone}" does not exist!'


    def find_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                print(f'Success! The number "{phone}" in your contacts!')
                return i
        return f'The number "{phone}" does not exist!'
    

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return f'Success! The birthday data: {self.birthday} was added!'
       

    def __str__(self):
        birthday_str = self.birthday.value if self.birthday else "No date of birth is specified!"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday_str}"




class AddressBook():
    def __init__(self, filename: str):
        self.users = {}
        self.filename = filename

    def add_record(self, record):
        self.users[record.name.value] = record


    def find(self, name):
        return self.users.get(name)


    def delete(self, name):
        if self.users.get(name):
            self.users.pop(name)
            return f'The record with name: "{name}" was succesfuly deleted!'
        else:
            return f'The record with name: "{name}" not found!'


    def get_birthdays_per_week(self):
        current_date = date.today()
        people_with_birthday_next_week = []
        people_with_birthday_next_week_dict = {}
        message = (f'Today is {current_date.strftime("%A %d %B %Y")}\n')
        message += ('The following people have their birthdays next week:\n')

        for key, val in self.users.items():
            if not val.birthday:
                continue
            name = key
            birthday_date = datetime.strptime(val.birthday.value, '%d.%m.%Y').date()
            birthday_this_year = birthday_date.replace(year=current_date.year)

            if birthday_this_year < current_date:
                birthday_this_year = birthday_date.replace(year=current_date.year + 1)
            
            delta_days = (birthday_this_year - current_date).days

            if 0 <= delta_days <= 7:
                if birthday_this_year.weekday() in (5, 6):
                    people_with_birthday_next_week.append(["Monday", name])
                else:
                    day_of_week = birthday_this_year.strftime('%A')
                    people_with_birthday_next_week.append((day_of_week, key))

        for day, name in people_with_birthday_next_week:
            if day not in people_with_birthday_next_week_dict:
                people_with_birthday_next_week_dict[day] = []
            people_with_birthday_next_week_dict[day].append(name)


        for key, value in people_with_birthday_next_week_dict.items():
            message += "{:<15}: {:<}\n".format(key, ', '.join(value))

        return message
    
    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        with open(self.filename, "rb") as file:
            contacts_book = pickle.load(file)
        return contacts_book
