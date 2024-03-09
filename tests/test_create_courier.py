import pytest
import requests
import allure
from data import TestData
from helpers import random_word, login_courier, create_courier, delete_courier


class TestCreateCourier:
    user_id = None

    @classmethod
    def setup_method(cls):
        cls.login = random_word()
        cls.password = random_word()
        cls.name = random_word()

    @classmethod
    def teardown_method(self):
        delete_courier(self.user_id)

    @allure.title('Проверка создания курьера c валидными значениями login, password, name')
    def test_create_courier_with_valid_credentials(self):
        response_create = create_courier(self.login, self.password, self.name)
        response_login = login_courier(self.login, self.password)
        self.user_id = response_login.json()['id']
        assert response_create.status_code == 201 and response_create.json()['ok'] == True
        assert response_login.status_code == 200

    @allure.title('Проверка ошибки создания курьера c занятыми login, password, name')
    def test_create_double_courier_returns_error(self):
        response_first = create_courier(self.login, self.password, self.name)
        self.user_id = login_courier(self.login, self.password).json()['id']
        response_second = create_courier(self.login, self.password, self.name)
        assert response_second.status_code == 409
        assert response_second.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Проверка ошибки создания курьера без одного из обязательных полей login, password')
    @pytest.mark.parametrize('payload', [({'login': random_word(), 'password': ''}),
                                         ({'login': random_word()}),
                                         ({'login': '', 'password': random_word()}),
                                         ({'password': random_word()})])
    def test_create_courier_without_one_field_returns_error(self, payload):
        response = requests.post(TestData.BASE_URL + TestData.COURIER_URL, data=payload)
        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для создания учетной записи'

    @allure.title('Проверка ошибки создания курьера если такой login уже занят')
    def test_create_courier_with_existing_login_returns_error(self):
        response_first = create_courier(self.login, self.password, self.name)
        response_second = create_courier(self.login, random_word(), random_word())
        assert response_first.status_code == 201
        assert response_second.status_code == 409
        assert response_second.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'
