from random import randint

from faker import Faker


faker = Faker("ru_RU")

class Generation:


    @staticmethod
    def email():
        return faker.email()

    @staticmethod
    def password():
        return faker.password(randint(6, 10))

    @staticmethod
    def user_name():
        return faker.user_name()
