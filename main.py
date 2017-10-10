from spy_details import Spy, ChatMessage
import csv
from datetime import datetime
from stegano import lsb
from termcolor import colored
# from steganography.steganography import Steganography

"""
NOTE: Since this project was built using Python 3.5 and not Python 2.7, Stegano module has been used instead of
the steganography module.
"""
# Creating a Spy object referring to the user
spy = Spy()

# Some default status messages
status_messages = ["In desperate need of a new Bond Girl.",
                   "I have a one-dimensional character, but I also have cool gadgets so who cares anyway?",
                   "Willing to fight any evil genius/warlord/maniac with a cliche plan involving world domination."
                   ]

print("Welcome! Let's get started.\n")


# The main function that controls the application by displaying a menu of the possible actions a user can perform
def start_chat():
    current_status_message = None

    show_menu = True

    name = spy.get_spy_salutation() + " " + spy.get_spy_name()

    # Perform some checks on the user's details
    if 12 < spy.get_spy_age() < 50:
        print("Authentication complete. Welcome, " + name + ", spy rating: ", spy.get_spy_rating())
    else:
        print("Sorry, you are not the appropriate age to be a spy")
        return

    while show_menu:
        menu_choices = '''\nWhat do you wish to do?\n1. Add a status update \n2. Close Application
3. Add a friend\n4. Send a message\n5. Read a message\n6. Read chat history\n'''
        menu_choice = eval(input(menu_choices))

        if menu_choice == 1:
            print("\nYou chose to update your status.")
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


# Function to add status messages
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


# Function to add a friend
def add_friend():

    # Create a new Spy object
    spy_friend = Spy()
    spy_friend.set_spy_name(input("\nPlease enter your friend's name: "))
    spy_friend.set_spy_salutation(input("Is your friend a Mr., a Ms. or a Mrs.? "))
    spy_friend.set_spy_age(int(input("How old is your friend? ")))
    spy_friend.set_spy_rating(float(input("What is your friend's rating? ")))

    # Perform some checks on the details entered
    if(len(spy_friend.get_spy_name()) > 0 and 12 < spy_friend.get_spy_age() < 50
       and spy_friend.get_spy_rating() >= spy.get_spy_rating()):

        # Add the friend to the list of friends
        spy.add_friend(spy_friend)

        # Also, write the friend's details to friends.csv
        with open("friends.csv", "a") as friends_data:
            writer = csv.writer(friends_data)
            writer.writerow([spy_friend.get_spy_name(), spy_friend.get_spy_salutation(), spy_friend.get_spy_age(),
                            spy_friend.get_spy_rating()])

    else:
        print("Sorry! Some of the details you provided for your friend might have been invalid.")

    return len(spy.get_spy_friends())


# Utility function to select a friend
def select_friend():
    friends = spy.get_spy_friends()
    count = 1

    # Print all friends, indexing starting at 1
    for friend in friends:
        print("%d. %s %s aged %d rating %f" % (count, friend.get_spy_salutation(), friend.get_spy_name(),
                                               friend.get_spy_age(), friend.get_spy_rating()))
        count += 1

    # Select an index from the printed list
    selected = int(input("Enter the no. of the friend to select: "))

    # If the friend is found, return its index in the printed list, otherwise return -1
    if 0 < selected <= count:
        return selected
    else:
        return -1


# Function to load all friends when the application starts
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


# Function to load all the chats involving the user when the application starts
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


# Function to send an encoded message
def send_message():
    print("\nSelect a friend to send a message to:")

    friend_choice = select_friend()

    # If the friend is not found, end the function
    if friend_choice == -1:
        print("Sorry! You entered an incorrect index.")
        return

    friend = spy.get_spy_friends()[friend_choice - 1]

    message, target_path, output_path = None, None, None

    # Input the message
    while True:
        message = input("Enter message below:\n")

        if len(message) > 0:
            break
        else:
            print("Please enter a message.")

    # Input the target image
    while True:
        target_path = input("Enter the directory of the target image:\n")

        if len(target_path) > 0:
            break
        else:
            print("Please enter a target directory.")

    # Input the output image
    while True:
        output_path = input("Enter the directory of the output image:\n")

        if len(output_path) > 0:
            break
        else:
            print("Please enter an output directory.")

    try:
        print("Encoding your message...")
        # Steganography.encode(target_path, output_path, message)

        # Encode the message and then save it at the output path
        secret = lsb.hide(target_path, message)
        secret.save(output_path)
        print("Done!")

        # Now add the message to the chat list as well
        chat_message = ChatMessage()
        chat_message.set_message(message)
        chat_message.set_time(datetime.now().strftime("%H:%M:%S"))
        chat_message.set_sender(spy.get_spy_name())
        chat_message.set_receiver(friend.get_spy_name())
        chat_message.set_target_path(target_path)
        chat_message.set_output_path(output_path)
        spy.get_chats().append(chat_message)

        # Write the message details into chats.csv
        with open("chats.csv", "a") as chats_data:
            writer = csv.writer(chats_data)
            writer.writerow([chat_message.get_message(), chat_message.get_time(), chat_message.get_sender(),
                            chat_message.get_receiver(), chat_message.get_target_path(),
                             chat_message.get_output_path()])

    except IOError:
        pass


# Function for reading the last message sent to or received from a selected friend
def read_message():

    friend_choice = select_friend()

    if friend_choice == -1:
        return

    friend_name = spy.get_spy_friends()[friend_choice - 1].get_spy_name()
    message, time, sender, receiver = None, None, None, None

    # Get all the messages in the log
    chats = spy.get_chats()

    # Reverse the list of chats so that the last message sent/received can be easily retrieved
    chats.reverse()

    # If there are no messages, end the function
    if len(chats) == 0:
        print("No messages here.")
        return

    for chat in chats:

        # If the message was sent by the user and received by the selected friend,
        # or if the message was sent by the friend and received by the user

        if (chat.get_sender() == spy.get_spy_name() and chat.get_receiver() == friend_name) or \
                (chat.get_sender() == friend_name and chat.get_receiver() == spy.get_spy_name()):
            try:
                # message = Steganography.decode(chat.get_output_path())

                # Decode the message hidden in the image specified by the output path
                message = lsb.reveal(chat.get_output_path())

                # Also, get the time, the sender and the receiver
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

    # Print the message in proper format.
    print(colored("From: " + sender, "red"))
    print(colored("To: " + receiver, "green"))
    print(colored("[" + time + "]", "blue"))
    print(message)


# Optional objective 2: Print the chat history for a particular friend.
# Print it using different colors for different details of the chat: Time in Blue, Spy Name in Red, Message in Black.
def read_chat():
    print("\nEnter the number of one of the following friends:")

    # First get the friend

    friend_choice = select_friend()
    friend_name = spy.get_spy_friends()[friend_choice - 1].get_spy_name()

    print("\nYour chat history with " + friend_name + ":")

    chat_history = []
    all_chats = spy.get_chats()

    # Search the entire chat log for any messages involving the user and the selected friend as sender and receiver
    # Then add only those messages to chat_history

    for chat in all_chats:
        if (chat.get_sender() == spy.get_spy_name() and chat.get_receiver() == friend_name) or \
                (chat.get_sender() == friend_name and chat.get_receiver() == spy.get_spy_name()):
            chat_history.append(chat)

    # If there are no messages between the user and the friend
    if len(chat_history) == 0:
        print("There are no chats to be found here.")
        return

    # Print the entire chat history between the user and the friend in the desired coloured format
    for chat in chat_history:
        sender = colored(chat.get_sender() + ": ", "red")
        time = colored(" [" + chat.get_time() + "]", "blue")
        message = chat.get_message()

        print(sender + message + time)


# Ask for user details upon starting the application
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

# Optional objective 4: When the application starts it should automatically load the friends from friends.csv
load_friends()
# Optional objective 3: When the application starts it should automatically load the chats from chats.csv
load_chats()
# Start the chat
start_chat()
