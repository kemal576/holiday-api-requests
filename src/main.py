import json
import requests
from src.config import Settings
from src.holiday import Holiday


def main():
    url = Settings.API_URL
    key = Settings.API_KEY
    # country = input("Type the code of the country whose holidays you want to list? like US,FR,TR :")
    country = "TR"
    year = 2021

    res = requests.get(url=url + "/holidays",
                       params={"key": key, "country": country, "year": year})

    if res.status_code == 200:
        response = json.loads(res.content)
        holidays_json = response["holidays"]
        holiday_list = [Holiday(**holiday) for holiday in holidays_json]

        print("%d holidays found for %s:" % (len(holiday_list), country))
        for holiday in holiday_list:
            print(holiday)
        exit(1)

    print(f"An error occurred. Status Code: {res.status_code}")
    exit(1)


if __name__ == '__main__':
    main()
