"""
ss.py - SchoolSoft API

This file leverages the SchoolSoft API to check for new work in the form of assignments, quizzes, and tests.
"""

import helper_schoolsoftapi as schoolsoft
from cryptography.fernet import Fernet
from typing import Any

key = Fernet.generate_key()
cipher_suite = Fernet(key)


def ask_for_login() -> Any:
    with open("credentials.key", "w+") as file:
        username = input("Enter your SchoolSoft username: ")
        password = input("Enter your SchoolSoft password: ")
        school = input("Enter your SchoolSoft school: ")
        eusername = cipher_suite.encrypt(username.encode())
        epassword = cipher_suite.encrypt(password.encode())
        eschool = cipher_suite.encrypt(school.encode())
        file.write(key.decode() + "\n")
        file.write(eusername.decode() + "\n")
        file.write(epassword.decode() + "\n")
        file.write(eschool.decode())
        return username, password, school

def cache_login() -> Any:
    with open("credentials.key", "r") as file:
        if file.read():
            # decrypt the credentials
            file.seek(0)
            pkey = file.readline().strip() # pkey, or past key is the key used to encrypt the credentials
            cipher_suite = Fernet(pkey.encode())
            username = cipher_suite.decrypt(file.readline().strip().encode())
            password = cipher_suite.decrypt(file.readline().strip().encode())
            school = cipher_suite.decrypt(file.readline().strip().encode())
        return username.decode(), password.decode(), school.decode()

def check_cache():
    with open("credentials.key", "r") as file:
        return file.read(1) != ''


if check_cache():
    apikey = schoolsoft.get_app_key(*cache_login())
else:
    apikey = schoolsoft.get_app_key(*ask_for_login())


print(apikey["orgs"][0]["name"])
print(apikey)
