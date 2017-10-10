class Spy:
    __spy_name = "James Bond"
    __spy_salutation = "Mr."
    __spy_age = 25
    __spy_rating = 5.0
    __spy_is_online = True
    __spy_friends = []
    __chats = []

    def get_spy_name(self):
        return self.__spy_name

    def set_spy_name(self, spy_name):
        self.__spy_name = spy_name

    def get_spy_salutation(self):
        return self.__spy_salutation

    def set_spy_salutation(self, spy_salutation):
        self.__spy_salutation = spy_salutation

    def get_spy_age(self):
        return self.__spy_age

    def set_spy_age(self, spy_age):
        self.__spy_age = spy_age

    def get_spy_rating(self):
        return self.__spy_rating

    def set_spy_rating(self, spy_rating):
        self.__spy_rating = spy_rating

    def get_spy_is_online(self):
        return self.__spy_is_online

    def set_spy_is_online(self, spy_is_online):
        self.__spy_is_online = spy_is_online

    def get_spy_friends(self):
        return self.__spy_friends

    def add_friend(self, spy_friend):
        self.__spy_friends.append(spy_friend)

    def remove_friend(self, spy_friend):
        self.__spy_friends.remove(spy_friend)

    def get_chats(self):
        return self.__chats


class ChatMessage:
    __message = None
    __time = None
    __sender = None
    __receiver = None
    __target_path = None
    __output_path = None

    # def __init__(self, message, sent_by_me):
    #     self.__message = message
    #     self.__time = datetime.now()
    #     self.__sent_by_me = sent_by_me

    def get_message(self):
        return self.__message

    def set_message(self, message):
        self.__message = message

    def get_time(self):
        return self.__time

    def set_time(self, time):
        self.__time = time

    def get_sender(self):
        return self.__sender

    def set_sender(self, sender):
        self.__sender = sender

    def get_receiver(self):
        return self.__receiver

    def set_receiver(self, receiver):
        self.__receiver = receiver

    def get_target_path(self):
        return self.__target_path

    def set_target_path(self, target_path):
        self.__target_path = target_path

    def get_output_path(self):
        return self.__output_path

    def set_output_path(self, output_path):
        self.__output_path = output_path
