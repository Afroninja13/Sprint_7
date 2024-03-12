import allure
import requests
from data import TestData


class TestOrderList:

    @allure.title('Проверка что при запросе списка заказов в тело ответа возвращается список заказов')
    def test_get_order_list_returns_order_list(self):
        response = requests.get(TestData.BASE_URL + TestData.ORDER_URL)
        assert response.status_code == 200
        assert type(response.json()['orders']) == list
