"""
Тесты базового слоя http-запросов
"""

import pytest
import json

deck_id = "111111111111"
value = "4"
suit = "CLUBS"

@pytest.fixture
def mock_get_200(mocked, test_ext_api_request) -> None:
	mocked.get(
        f"{test_ext_api_request.ext_api_base_url}{deck_id}/shuffle/",
        status=200, 
        body=json.dumps({"success": True, "deck_id": deck_id, "remaining": 52, "shuffled": True})
    )


@pytest.fixture
def mock_get_404(mocked, test_ext_api_request) -> None:
	mocked.get(
        f"{test_ext_api_request.ext_api_base_url}{deck_id}/shuffle/",
        status=404, 
        body=json.dumps({"success": False, "error": "Deck ID does not exist."})
    )


@pytest.fixture
def mock_get_500(mocked, test_ext_api_request) -> None:
	mocked.get(
        f"{test_ext_api_request.ext_api_base_url}{deck_id}/shuffle/",
        status=500, 
        body=json.dumps({"success": False, "error": "Internal error."})
    )


@pytest.fixture
def mock_get_params_200(mocked, test_ext_api_request) -> None:
	mocked.get(
        f"{test_ext_api_request.my_api_url}?card_suit={suit}&card_value={value}",
        status=200, 
        body=json.dumps({"value": value, "suit": suit, "count": 1})
    )


@pytest.fixture
def mock_get_params_404(mocked, test_ext_api_request) -> None:
	mocked.get(
        f"{test_ext_api_request.my_api_url}?card_suit={suit}&card_value={value}",
        status=404, 
        body=json.dumps({"detail": "Card not found"})
    )


@pytest.fixture
def mock_get_params_500(mocked, test_ext_api_request) -> None:
	mocked.get(
        f"{test_ext_api_request.my_api_url}?card_suit={suit}&card_value={value}",
        status=500, 
        body=json.dumps({"detail": "Internal error."})
    )



@pytest.fixture
def mock_post_200(mocked, test_ext_api_request) -> None:
	mocked.post(
        test_ext_api_request.my_api_url,
        status=200, 
        body=json.dumps({"value": value, "suit": suit, "count": 1})
    )


@pytest.fixture
def mock_post_500(mocked, test_ext_api_request) -> None:
	mocked.post(
        test_ext_api_request.my_api_url,
        status=500, 
        body=json.dumps({"detail": "Internal error."})
    )


@pytest.fixture
def mock_put_200(mocked, test_ext_api_request) -> None:
	mocked.put(
        f"{test_ext_api_request.my_api_url}?card_count=2&card_suit={suit}&card_value={value}",
        status=200, 
        body=json.dumps({"value": value, "suit": suit, "count": 2})
    )


@pytest.fixture
def mock_put_404(mocked, test_ext_api_request) -> None:
	mocked.put(
        f"{test_ext_api_request.my_api_url}?card_count=2&card_suit={suit}&card_value={value}",
        status=404, 
        body=json.dumps({"detail": "Card not found"})
    )


@pytest.fixture
def mock_put_500(mocked, test_ext_api_request) -> None:
	mocked.put(
        f"{test_ext_api_request.my_api_url}?card_count=2&card_suit={suit}&card_value={value}",
        status=500, 
        body=json.dumps({"detail": "Internal error."})
    )



@pytest.mark.asyncio
async def test_get_url_200(mock_get_200, test_session_requests, test_ext_api_request) -> None:
	res = await test_session_requests.get_url(f"{test_ext_api_request.ext_api_base_url}{deck_id}/shuffle/")
	assert res == {"status": 200, "json": {"success": True, "deck_id": deck_id, "remaining": 52, "shuffled": True}, "msg": None}



@pytest.mark.asyncio
async def test_get_url_404(mock_get_404, test_session_requests, test_ext_api_request) -> None:
	res = await test_session_requests.get_url(f"{test_ext_api_request.ext_api_base_url}{deck_id}/shuffle/")
	assert res == {"status": 404, "json": None, "msg": "Not found"}
	


@pytest.mark.asyncio
async def test_get_url_500(mock_get_500, test_session_requests, test_ext_api_request) -> None:
	res = await test_session_requests.get_url(f"{test_ext_api_request.ext_api_base_url}{deck_id}/shuffle/")
	assert res == {"status": 500, "json": None, "msg": '{"success": false, "error": "Internal error."}'}



@pytest.mark.asyncio
async def test_get_url_params_200(mock_get_params_200, test_session_requests, test_ext_api_request) -> None:
	res = await test_session_requests.get_url_params(test_ext_api_request.my_api_url, {"card_value": value, "card_suit": suit})
	assert res == {"status": 200, "json": {"value": value, "suit": suit, "count": 1}, "msg": None}



@pytest.mark.asyncio
async def test_get_url_params_404(mock_get_params_404, test_session_requests, test_ext_api_request) -> None:
	res = await test_session_requests.get_url_params(test_ext_api_request.my_api_url, {"card_value": value, "card_suit": suit})
	assert res == {"status": 404, "json": None, "msg": "Not found"}



@pytest.mark.asyncio
async def test_get_url_params_500(mock_get_params_500, test_session_requests, test_ext_api_request) -> None:
	res = await test_session_requests.get_url_params(test_ext_api_request.my_api_url, {"card_value": value, "card_suit": suit})
	assert res == {"status": 500, "json": None, "msg": '{"detail": "Internal error."}'}



@pytest.mark.asyncio
async def test_post_url_200(mock_post_200, test_session_requests, test_ext_api_request) -> None:
	res = await test_session_requests.post_url(test_ext_api_request.my_api_url, {"value": value, "suit": suit})
	assert res == {"status": 200, "json": {"value": value, "suit": suit, "count": 1}, "msg": None}



@pytest.mark.asyncio
async def test_post_url_500(mock_post_500, test_session_requests, test_ext_api_request) -> None:
	res = await test_session_requests.post_url(test_ext_api_request.my_api_url, {"value": value, "suit": suit})
	assert res == {"status": 500, "json": None, "msg": '{"detail": "Internal error."}'}



@pytest.mark.asyncio
async def test_put_url_200(mock_put_200, test_session_requests, test_ext_api_request) -> None:
	res = await test_session_requests.put_url(test_ext_api_request.my_api_url, {"card_value": value, "card_suit": suit, "card_count": 2})
	assert res == {"status": 200, "json": {"value": value, "suit": suit, "count": 2}, "msg": None}



@pytest.mark.asyncio
async def test_put_url_404(mock_put_404, test_session_requests, test_ext_api_request) -> None:
	res = await test_session_requests.put_url(test_ext_api_request.my_api_url, {"card_value": value, "card_suit": suit, "card_count": 2})
	assert res == {"status": 404, "json": None, "msg": "Not found"}



@pytest.mark.asyncio
async def test_put_url_500(mock_put_500, test_session_requests, test_ext_api_request) -> None:
	res = await test_session_requests.put_url(test_ext_api_request.my_api_url, {"card_value": value, "card_suit": suit, "card_count": 2})
	assert res == {"status": 500, "json": None, "msg": '{"detail": "Internal error."}'}