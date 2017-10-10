from spy_details import Spy, ChatMessage
import csv
from datetime import datetime
# from steganography.steganography import Steganography
from stegano import lsb
from termcolor import colored

spy = Spy()

status_messages = ["In desperate need of a new Bond Girl.",
                   "I have a one-dimensional character, but I also have cool gadgets so who cares anyway?",
                   "Willing to fight any evil genius/warlord/maniac with a cliche plan involving world domination."
                   ]

print("Welcome! Let's get started.\n")
#
# existing = input("Do you wish to continue as " + spy.get_spy_salutation() + " " + spy.get_spy_name() + " (Y/N)? ")


def start_chat():
    current_status_message = None

    show_menu = True

    name = spy.get_spy_salutation() + " " + spy.get_spy_name()

    if 12 < spy.get_spy_age() < 50:
        print("Authentication complete. Welcome, " + name + ", spy rating: ", spy.get_spy_rating())
    else:
        print("Sorry, you are not the appropriate age to be a spy")
        return

    while show_menu:
        menu_choices = '''\nWhat do you wish to do?\n1. Add a status update \n2. Close Application
3. Add a friend\n4. Send a message\n5. Read a message\n6. Read chat history'''
        menu_choice = eval(input(menu_choices))

        if menu_choice == 1:
            print("You chose to update your status.")
            current_status_message = add_status(current_status_message)
        elif menu_choice == 2:
            show_menu = False
            exit(0)
        elif menu_choice == 3:
            add_friend()
        elif menu_choice == 4:
            send_message()
        elif menu_choice == 5:
            read_message()
        elif menu_choice == 6:
            read_chat()


def add_status(current_status_message):
    new_status_message = ""
    updated_status_message = ""

    if current_status_message is not None:
        print("Your current status message is" + current_status_message)
    else:
        print("You do not currently have any status message.")

    default = input("Do you want to select a default status message? (Y/N) ")

    if default.upper() == 'N':
        new_status_message = input("Please enter your new status message:\n")
    elif default.upper() == 'Y':
        item_position = 1
        for status_message in status_messages:
            print(str(item_position) + ". " + status_message)
            item_position += 1
        message_selection = int(input("Choose one of the above messages: "))

        if len(status_messages) >= message_selection:
            updated_status_message = status_messages[message_selection - 1]
            status_messages.append(updated_status_message)

    if len(new_status_message) > 0:
        updated_status_message = new_status_message
        status_messages.append(updated_status_message)

    return updated_status_message


def add_friend():
    spy_friend = Spy()
    spy_friend.set_spy_name(input("Please enter your friend's name: "))
    spy_friend.set_spy_salutation(input("Is your friend a Mr., a Ms. or a Mrs.? "))
    spy_friend.set_spy_age(int(input("How old is your friend? ")))
    spy_friend.set_spy_rating(float(input("What is your friend's rating? ")))

    if(len(spy_friend.get_spy_name()) > 0 and 12 < spy_friend.get_spy_age() < 50
       and spy_friend.get_spy_rating() >= spy.get_spy_rating()):

        spy.add_friend(spy_friend)

        with open("friends.csv", "a") as friends_data:
            writer = csv.writer(friends_data)
            writer.writerow([spy_friend.get_spy_name(), spy_friend.get_spy_salutation(), spy_friend.get_spy_age(),
                            spy_friend.get_spy_rating()])

    else:
        print("Sorry! Some of the details you provided for your friend might have been invalid.")

    return len(spy.get_spy_friends())


def select_friend():
    friends = spy.get_spy_friends()
    count = 1
    for friend in friends:
        print("%d. %s %s aged %d rating %f" % (count, friend.get_spy_salutation(), friend.get_spy_name(),
                                               friend.get_spy_age(), friend.get_spy_rating()))
        count += 1

    selected = int(input("Enter the no. of the friend to select: "))

    if 0 < selected <= count:
        return selected
    else:
        return -1


def load_friends():
    with open("friends.csv", "r") as friends_data:
        reader = csv.reader(friends_data)
        for row in reader:
            spy_friend = Spy()
            spy_friend.set_spy_name(row[0])
            spy_friend.set_spy_salutation(row[1])
            spy_friend.set_spy_age(int(row[2]))
            spy_friend.set_spy_rating(float(row[3]))
            spy.get_spy_friends().append(spy_friend)


def load_chats():
    with open("chats.csv", "r") as chats_data:
        reader = csv.reader(chats_data)
        for row in reader:
            if row[2] == spy.get_spy_name() or row[3] == spy.get_spy_name():
                chat_message = ChatMessage()
                chat_message.set_message(row[0])
                chat_message.set_time(row[1])
                chat_message.set_sender(row[2])
                chat_message.set_receiver(row[3])
                chat_message.set_target_path(row[4])
                chat_message.set_output_path(row[5])
                spy.get_chats().append(chat_message)


def send_message():
    friend_choice = select_friend()

    if friend_choice == -1:
        return

    friend = spy.get_spy_friends()[friend_choice - 1]

    message, target_path, output_path = None, None, None

    while True:
        message = input("Enter message below:\n")

        if len(message) > 0:
            break
        else:
            print("Please enter a message.")

    while True:
        target_path = input("Enter the directory of the target image:\n")

        if len(target_path) > 0:
            break
        else:
            print("Please enter a target directory.")

    while True:
        output_path = input("Enter the directory of the output image:\n")

        if len(output_path) > 0:
            break
        else:
            print("Please enter an output directory.")

    try:
        print("Encoding your message...")
        # Steganography.encode(target_path, output_path, message)
        secret = lsb.hide(target_path, message)
        secret.save(output_path)
        print("Done!")

        chat_message = ChatMessage()
        chat_message.set_message(message)
        chat_message.set_time(datetime.now().strftime("%H:%M:%S"))
        chat_message.set_sender(spy.get_spy_name())
        chat_message.set_receiver(friend.get_spy_name())
        chat_message.set_target_path(target_path)
        chat_message.set_output_path(output_path)
        spy.get_chats().append(chat_message)

        with open("chats.csv", "a") as chats_data:
            writer = csv.writer(chats_data)
            writer.writerow([chat_message.get_message(), chat_message.get_time(), chat_message.get_sender(),
                            chat_message.get_receiver(), chat_message.get_target_path(),
                             chat_message.get_output_path()])

    except IOError:
        pass


def read_message():
    friend_choice = select_friend()

    if friend_choice == -1:
        return

    message, time, sender, receiver = None, None, None, None
    chats = spy.get_chats()
    chats.reverse()

    for chat in chats:
        if chat.get_receiver() == spy.get_spy_friends()[friend_choice - 1].get_spy_name():
            try:
                # message = Steganography.decode(chat.get_output_path())

                message = lsb.reveal(chat.get_output_path())
                time = chat.get_time()
                sender = chat.get_sender()
                receiver = chat.get_receiver()

            except IOError:
                message = chat.get_message()
                time = chat.get_time()
                sender = chat.get_sender()
                receiver = chat.get_receiver()

            finally:
                break

    print(message + " " + time + " " + sender + " " + receiver)


def read_chat():
    print("\nEnter the number of one of the following friends:")
    friend_choice = select_friend()
    friend_name = spy.get_spy_friends()[friend_choice - 1].get_spy_name()

    print("\nYour chat history with " + friend_name + ":")

    chat_history = []
    all_chats = spy.get_chats()
    for chat in all_chats:
        if (chat.get_sender() == spy.get_spy_name() and chat.get_receiver() == friend_name) or \
                (chat.get_sender() == friend_name and chat.get_receiver() == spy.get_spy_name()):
            chat_history.append(chat)

    if len(chat_history) == 0:
        print("There are no chats to be found here.")
        return

    for chat in chat_history:
        sender = colored(chat.get_sender() + ": ", "red")
        time = colored(" [" + chat.get_time() + "]", "blue")
        message = chat.get_message()

        print(sender + message + time)

# if existing == 'Y':
#     start_chat()
# else:
#     spy.set_spy_name("")
#     spy.set_spy_salutation("")
#     spy.set_spy_age(0)
#     spy.set_spy_rating(0.0)
#     spy.set_spy_is_online(False)
#
# spy_name = input("Welcome to SpyChat! Please tell me your name: ")
#
# if len(spy_name) > 0:
#     spy.set_spy_name(spy_name)
#     spy.set_spy_salutation(input("Should I call you Mr. or Mrs. : "))
#     spy.set_spy_age(int(input("What is your age?")))
#     spy.set_spy_rating(float(input("What is your spy rating?")))
#     spy.set_spy_is_online(True)
#     start_chat()
# else:
#     print("Please enter a valid spy name")


while True:
    spy_name = input("Please tell me your name: ")

    if len(spy_name) > 0:
        spy.set_spy_name(spy_name)
        spy.set_spy_salutation(input("Should I call you Mr. or Mrs. : "))
        spy.set_spy_age(int(input("What is your age?")))
        spy.set_spy_rating(float(input("What is your spy rating?")))
        spy.set_spy_is_online(True)
        break
    else:
        print("Please enter a valid spy name.")

load_friends()
load_chats()
start_chat()
