import requests

def fetch_live_odds(api_key, league=None, date=None):
    url = "https://api.coredataservices.com/odds"
    params = {
        "api_key": api_key,
        "sport": "soccer",
        "market": "1X2,over_under,btts",
        "date": date,
        "league": league,
        "format": "json"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()
