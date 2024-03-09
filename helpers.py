import json
import random
import string
import allure
import requests
from data import TestData


@allure.step('Создаем рандомное слово из 6 символов')
def random_word():
    return str(''.join(random.choice(string.ascii_letters) for x in range(6)))


@allure.step('Логинимся курьером')
def login_courier(login=None, password=None):
    payload = {'login': login, 'password': password}
    response_login = requests.post(TestData.BASE_URL + TestData.LOGIN_COURIER_URL, data=payload)
    return response_login


@allure.step('Создаем курьера')
def create_courier(login, password, name):
    payload = {'login': login, 'password': password, 'name': name}
    response_create = requests.post(TestData.BASE_URL + TestData.COURIER_URL, data=payload)
    return response_create


@allure.step('Удаляем курьера')
def delete_courier(user_id):
    response_delete = requests.delete(TestData.BASE_URL + TestData.COURIER_URL + '/' + str(user_id))
    return response_delete


@allure.step('Создаем заказ')
def create_order(first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment,
                 color_list=None):

    payload = {'firstName': first_name,
               'lastName': last_name,
               'address': address,
               'metroStation': metro_station,
               'phone': phone,
               'rentTime': rent_time,
               'deliveryDate': delivery_date,
               'comment': comment,
               'color': color_list}

    response_create = requests.post(TestData.BASE_URL + TestData.ORDER_URL, data=json.dumps(payload))
    return response_create


@allure.step('Создаем курьера и возвращаем его login, password, name')
def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
    return login_pass
