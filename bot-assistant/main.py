from classes import Record, AddressBook



def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "The contact does not exist"
        except IndexError:
            return "Enter contact's name"
        except AttributeError:
            return "No contacts found"

    return inner


@input_error
def add_contact(args, book):
    name, phone = args
    user_record = Record(name)
    user_record.add_phone(phone)
    book.add_record(user_record)
    return (f"Contact with name '{name}' added.")


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    book.find(name).edit_phone(old_phone, new_phone)
    return f"Contact with name '{name}' was updated and has new number: {new_phone}. The prior phone number was: {old_phone}"

    
@input_error
def show_phone(args, book): 
    name = args[0]
    user_phones = book.find(name).phones
    return f"Contact with name '{name}' has phone numbers: {'; '.join(p.value for p in user_phones)}."


@input_error
def show_all(book):
    if not book:
        raise ValueError
       
    message_all_contacts = "\n".join(f"{contact_info}" for name, contact_info in book.users.items())   
    return message_all_contacts


@input_error
def add_birthdays(args, book):
    name, birthday = args
    user = book.find(name)
    user.add_birthday(birthday)
    return (f"Birthday for'{name}' added!")


@input_error
def show_birthdays(args, book): 
    name = args[0]
    user_birthdays = book.find(name)
    return (f"Contact with name '{name}' has birthdays on '{user_birthdays.birthday.value}'.")


@input_error
def all_birthdays(book):
    if not book:
        raise ValueError
    birthdays_per_week = book.get_birthdays_per_week()  
    return birthdays_per_week
    




def main():
    book = AddressBook("saved-contacts")
    print("Welcome to the assistant bot!")

    try:
        book = book.read_from_file()
        print("  ==> Notification: 'Contacts successfully downloaded from the storage!'")
    except Exception:
        print("  ==> Notification: 'The contact storage is still empty!'")


    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            if book.users:
                book.save_to_file()
                print("  ==> Notification: 'Contacts saved to the storage successfully!'")
                print("Good bye!")
                break
            else:
                print("Good bye!")
                break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthdays(args, book))
        elif command == "show-birthday":
            print(show_birthdays(args, book))
        elif command == "birthdays":
            print(all_birthdays(book))
        else:
            print("Invalid command.")
    


if __name__ == "__main__":
    main()