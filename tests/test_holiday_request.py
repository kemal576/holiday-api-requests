import pytest
import requests

from src.config import Settings

holidays_json = {
    "status": 200,
    "warning": "These results do not include state and province holidays. For more information, please visit https:\/\/holidayapi.com\/docs",
    "requests": {
        "used": 27,
        "available": 9973,
        "resets": "2022-08-01 00:00:00"
    },
    "holidays": [
        {
            "name": "New Year's Day",
            "date": "2021-01-01",
            "observed": "2021-01-01",
            "public": "true",
            "country": "TR",
            "uuid": "d8fdec4a-8316-40c8-99d1-28e1d3503ed4",
            "weekday": {
                "date": {
                    "name": "Friday",
                    "numeric": "5"
                },
                "observed": {
                    "name": "Friday",
                    "numeric": "5"
                }
            }
        }
    ]
}
holidays_error_json = {
    "status": 400,
    "requests": {
        "used": 42,
        "available": 9958,
        "resets": "2022-08-01 00:00:00"
    },
    "error": "The requested country (INVALID_COUNTRY_CODE) is invalid. For more information, please visit https:\/\/holidayapi.com\/docs"
}

key = Settings.API_KEY


@pytest.mark.parametrize(
    "country_code, expected_status, expected_json",
    [
        ("TR", 200, holidays_json),
        ("INVALID_COUNTRY_CODE", 400, holidays_error_json)
    ],
)
def test_get_holidays(country_code, expected_status, expected_json, mocker):
    mock = mocker.patch("src.main.requests.get")
    mock.return_value.json = expected_json
    mock.return_value.status_code = expected_status

    req = requests.get(f"{Settings.API_URL}/holidays",
                       params={"key": key, "country": country_code})

    assert req.json == expected_json
    assert req.status_code == expected_status


# def test_get_holidays_fail(mocker):
#     country = "INVALID_COUNTRY_CODE"
#
#     mock = mocker.patch("src.main.requests.get")
#     mock.return_value.json = holidays_error_json
#     mock.return_value.status_code = 400
#
#     req = requests.get(f"{Settings.API_URL}/holidays",
#                        params={"key": key, "country": country})
#
#     assert req.status_code == 400
#     assert req.json == holidays_error_json
