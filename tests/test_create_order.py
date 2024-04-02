import pytest
import allure
from helpers import create_order


class TestCreateOrder:

    @allure.title('Проверка создания заказа с разными значениями поля color')
    @pytest.mark.parametrize('color_list', [
        (['BLACK']),
        (['GRAY']),
        (['BLACK', 'GRAY']),
        ([])
    ])
    def test_create_order_with_any_color_positive_result(self, color_list):
        response = create_order('Naruto', 'Uchiha', 'Konoha, 142 apt.', 4,
                                '88003553535', 5, '2024-03-15',
                                'Saske, come back to Konoha', color_list)
        assert response.status_code == 201
        assert response.json()['track']
