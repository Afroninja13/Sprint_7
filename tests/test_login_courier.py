import pytest
import requests
import allure
from data import TestData
from helpers import (random_word, login_courier, register_new_courier_and_return_login_password,
                     delete_courier)


class TestLoginCourier:

    login, password, name = register_new_courier_and_return_login_password()
    user_id = login_courier(login, password).json()['id']

    @classmethod
    def teardown_class(cls):
        delete_courier(cls.user_id)

    @allure.title('Проверка логина курьера с валидными значениями login, password')
    def test_login_courier_with_valid_credentials(self):
        response = login_courier(self.login, self.password)
        assert response.status_code == 200
        assert response.json()['id']

    @allure.title('Проверка ошибки логина курьера без одного из обязательных полей login, password')
    @pytest.mark.parametrize('payload', [({'login': login}),
                                         ({'login': login, 'password': ''}),
                                         ({'password': password}),
                                         ({'login': '', 'password': password})])
    def test_login_courier_without_one_field_returns_error(self, payload):
        response = requests.post(TestData.BASE_URL + TestData.LOGIN_COURIER_URL, data=payload)
        assert response.status_code == 400
        # Баг. Сервер возвращает статус 504 вместо 400 если не передать поле password
        assert response.json()['message'] == TestData.NOT_ENOUGHT_DATA_ERROR

    @allure.title('Проверка ошибки логина курьера c невалидными значениями полей login, password')
    @pytest.mark.parametrize('name, password', [(name, random_word()),
                                                (random_word(), password),
                                                (random_word(), random_word())])
    def test_login_courier_with_invalid_credentials_return_error(self, name, password):
        response = login_courier(name, password)
        assert response.status_code == 404
        assert response.json()['message'] == TestData.ACCOUNT_NOT_FOUND_ERROR
