import requests


def request_geo_info(addrr):
    return requests.get("https://ipwhois.app/json/" + addrr)
