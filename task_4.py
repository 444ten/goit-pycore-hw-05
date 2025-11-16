def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError:
            return "Give me name and phone please."

        except IndexError:
            return "Not enough arguments."

        except KeyError:
            return "No such contact."

    return inner

def parse_input(user_input):
    parts = user_input.split()
    if not parts:
        return None, []
    cmd, *args = parts
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, contacts):
    if len(args) == 1:
        raise IndexError
    
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    if len(args) == 1:
        raise IndexError

    name, phone = args
    
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    name = args[0]
    return contacts[name]

def show_all(contacts):
    if not contacts:
        return "No contacts found."
    result = ["Contacts list:"]
    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")
    return "\n".join(result)


def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if not command:
            print("Please enter a command.")
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
