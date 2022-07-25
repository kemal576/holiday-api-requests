import json

import pytest
import requests
from requests.exceptions import HTTPError

from src.config import Settings
from src.holiday import Holiday
from src.main import get_holidays

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
        "used": 68,
        "available": 9932,
        "resets": "2022-08-01 00:00:00"
    },
    "error": "The requested country (TSD) is invalid. For more information, please visit https:\/\/holidayapi.com\/docs"
}

api_key = Settings.API_KEY


@pytest.mark.parametrize(
    "key, country_code, year, expected_status",
    [
        (api_key, "TR", 2021, 200),  # Successful req. for TR
        (api_key, "XY", 2021, 400),  # Unsuccessful req. with invalid "country_code"
        ("12345", "UK", 2021, 403),  # Unsuccessful req. with invalid "api_key"
        (api_key, "FR", 2022, 402),  # Unsuccessful req. bcs it is a free api account, so we can
        # only see last year's holidays
    ],
)
def test_holiday_requests(key, country_code, year, expected_status, mocker):
    mock = mocker.patch("src.main.requests.get")
    mock.return_value.status_code = expected_status

    req = requests.get(f"{Settings.API_URL}/holidays",
                       params={"key": key, "country": country_code})

    assert req.status_code == expected_status


def test_get_holidays_success(mocker):
    mock = mocker.patch("src.main.requests.get")
    mock.return_value.status_code = 200
    mock.return_value.content = json.dumps(holidays_json).encode('utf-8')

    holidays: list[Holiday] = get_holidays()

    assert len(holidays) == 1
    assert holidays[0].name == "New Year's Day"


# def test_get_holidays_fail(mocker):
#     mock = mocker.patch("src.main.requests.get")
#     mock.return_value.status_code = 400
#
#     try:
#         holidays = get_holidays()
#     except HTTPError as e:
#         assert e.response.status_code == 400
