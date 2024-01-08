class UsersManager:
    def __init__(self):
        self.__users = {}

    def add_user(self, user):
        self.__users[user] = []

    def delete_user(self, user):
        if user in self.__users:
            del self.__users[user]

    def add_address_to_user(self, user, address):
        self.__users[user].append(address)

    def delete_address_from_user(self, user, address):
        if user in self.__users and address in self.__users[user]:
            self.__users[user].remove(address)

    def is_user_using_address(self, user, address):
        if user in self.__users and address in self.__users[user]:
            return True
        return False

    def get_user_by_address(self, address):
        for user in self.__users:
            if address in self.__users[user]:
                return user
        return None
