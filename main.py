from address_book import *


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


def print_phonebook_list(contacts):
    contact_name = 'Contact'
    max_key_len = max(len(key) for key in contacts)
    max_key_len = len(contact_name) if len(contact_name) > max_key_len else max_key_len
    max_key_len = max_key_len + 1 if not max_key_len % 2 else max_key_len

    phone_name = 'Phone'
    max_contact_len = max(len(contacts[key].phone.value) for key in contacts)
    max_contact_len = len(phone_name) if len(phone_name) > max_contact_len else max_contact_len
    max_contact_len = max_contact_len + 1 if not max_contact_len % 2 else max_contact_len

    space_width = 4
    separator = f'|{'-' * ((max_key_len + max_contact_len) + 2 * space_width + 1)}|\n'

    contacts_string = f'\n{separator}'
    title_name = 'PHONEBOOK'
    pound_sign_string_len = int((len(separator) - len(title_name)) / 2)
    contacts_string += f'| {'#' * (pound_sign_string_len - 3)} {title_name} {'#' * (pound_sign_string_len - 3)} |\n'
    contacts_string += separator
        
    contacts_string += '|{name:^{name_width}}|{phone:^{phone_width}}|\n'.format(name=contact_name, name_width=max_key_len + space_width, phone=phone_name, phone_width=max_contact_len + space_width)
    contacts_string += separator * 2

    for key in contacts:
        contacts_string += '|{name:^{name_width}}|{phone:^{phone_width}}|\n'.format(name=key, name_width=max_key_len + 4, phone=contacts[key].phone.value, phone_width=max_contact_len + 4)
        contacts_string += separator

    return contacts_string


def input_error(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except ValueError:
            return '\nWrong arguments!\n'\
                'For "add" and "change" give me name and phone (10 digits).\n'\
                'For "phone" give me name.\n'\
                'For "all" give me no arguments.\n'
        except KeyError:
            return 'Contact does not exists!'
        except PhoneFormatException:
            return 'Number should contain 10 digits!'
        except ContactExistsError:
            return 'Contact already exists!'
    return inner


@input_error
def add_contact(args, contacts):
    name, phone = args

    if contacts.find(name) == -1:
        contact = Record(name)
        contact.add_phone(phone)
        contacts.add_record(contact)
        return 'Contact added.'
    
    raise ContactExistsError


@input_error      
def change_contact(args, contacts):
    name, phone = args 
    contacts[name].add_phone(phone)

    return 'Contact changed.'
          

@input_error
def get_phone(args, contacts):
    (name,) = args
    
    return f'Phone number for {name}: {contacts[name].phone}'


@input_error   
def get_all(args, contacts):
    if len(args) != 0:
        return 'You should not put any arguments in "all" command!'
    
    if not contacts:
        return 'No contacts in phonebook!!!'
    
    return print_phonebook_list(contacts)


def main():
    contacts = AddressBook()
    print('Welcome to the assistant bot!')
    while True:
        try:
            user_input = input('Enter a command: ')
            command, *args = parse_input(user_input)

            if command in ['close', 'exit']:
                print('Goodbye!')
                break
            elif command == 'hello':
                print('How can I help you?')
            elif command == 'add':
                print(add_contact(args, contacts))
            elif command == 'change':
                print(change_contact(args, contacts))
            elif command == 'phone':
                print(get_phone(args, contacts))
            elif command == 'all':
                print(get_all(args, contacts))
            else:
                print('Invalid command.')   
        except ValueError:
            print('Please use commands!')


if __name__ == '__main__':
    main()
