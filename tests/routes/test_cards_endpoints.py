"""
Тесты ручек работы с БД
"""

import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "parameters, result_status_code, result_data",[
        (
            {"card_value": "4", "card_suit": "CLUBS", "for_testing": "Ok"}, 
            200, 
            {"value": "4", "suit": "CLUBS", "count": 2}
        ),
        (
            {"card_value": "4", "card_suit": "CLUBS", "for_testing": "Err"}, 
            404, 
            {"detail": "Card not found"}
        )
    ]
)
async def test_get_card_count(async_client, parameters, result_status_code, result_data) -> None:
    response = await async_client.get("http://testserver/cards_api/cards", params=parameters)
    assert response.status_code == result_status_code
    data = response.json()
    assert data == result_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "parameters, result_status_code, result_data",[
        (
            {"card_value": "4", "card_suit": "CLUBS", "for_testing": "Ok"}, 
            200, 
            {"value": "4", "suit": "CLUBS", "count": 2}
        ),
        (
            {"card_value": "4", "card_suit": "CLUBS", "for_testing": "Err"}, 
            404, 
            {"detail": "Card not found"}
        )
    ]
)
async def test_service_route_get_card(async_client, parameters, result_status_code, result_data) -> None:
    response = await async_client.get("http://testserver/cards_api/_service_route/cards", params=parameters)
    assert response.status_code == result_status_code
    data = response.json()
    assert data == result_data



@pytest.mark.asyncio
async def test_service_route_add_card(async_client) -> None:
    response = await async_client.post(
        "http://testserver/cards_api/_service_route/cards", 
        json={"value": "4", "suit": "CLUBS", "count": 1}, 
        params={"for_testing": "Ok"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {"value": "4", "suit": "CLUBS", "count": 2} 



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "parameters, result_status_code, result_data",[
        (
            {"card_value": "4", "card_suit": "CLUBS", "card_count": 2, "for_testing": "Ok"}, 
            200, 
            {"value": "4", "suit": "CLUBS", "count": 2}
        ),
        (
            {"card_value": "4", "card_suit": "CLUBS", "card_count": 2, "for_testing": "Err"}, 
            404, 
            {"detail": "Card not found"}
        )
    ]
)
async def test_service_route_update_card(async_client, parameters, result_status_code, result_data) -> None:
    response = await async_client.put("http://testserver/cards_api/_service_route/cards", params=parameters)
    assert response.status_code == result_status_code
    data = response.json()
    assert data == result_data