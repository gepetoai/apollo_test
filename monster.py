import requests

url = "https://appsapi.monster.io/jobs-svx-service/v2/monster/search-jobs/samsearch/en-US"

querystring = {"apikey":"AE50QWejwK4J73X1y1uNqpWRr2PmKB3S"}

payload = {
    "jobQuery": {
        "query": "sales development representative"
    },
    "includeJobs": [],
    "jobAdsRequest": {
        "position": [1, 2, 3, 4, 5, 6, 7, 8, 9]
    },
    "placement": {
        "channel": "MOBILE",
        "location": "JobSearchPage",
        "property": "monster.com",
        "type": "JOB_SEARCH"
    },
    "view": "CARD",
    "position": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "jobQuery": {
        "query": "sales development representative"
    },
    "locations": [
        {
            "country": "us",
            "address": "",
            "radius": {
                "unit": "mi",
                "value": 20
            }
        }
    ],
    "offset": 0,
    "pageSize": 9
}

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json; charset=UTF-8",
    "Request-Starttime": "1711397610375",

    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
}

response = requests.post(url, json=payload, headers=headers, params=querystring)

print(response.text)