import json
import requests
from requests.exceptions import HTTPError

from src.config import Settings
from src.holiday import Holiday


def get_holidays() -> list:
    url = Settings.API_URL
    key = Settings.API_KEY
    country = "TR"
    year = 2021

    res = requests.get(url=f"{url}/holidays", params={"key": key, "country": country, "year": year})

    try:
        res.raise_for_status()
    except HTTPError as e:
        print(f"An HTTP error occurred. Status Code: {e.response.status_code}")
        raise

    response = json.loads(res.content)
    holidays_json = response["holidays"]
    holiday_list = [Holiday(**holiday) for holiday in holidays_json]

    print("%d holidays found for %s:" % (len(holiday_list), country))
    return holiday_list


def main():
    try:
        holidays = get_holidays()
        for holiday in holidays:
            print(holiday)

    except HTTPError:
        exit()


if __name__ == '__main__':
    main()
