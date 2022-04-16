import requests
import csv
import time

vivino_base_url = 'https://www.vivino.com/api'
request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
}
# api for structure
# https://www.vivino.com/api/wines/1695288/tastes\?language\=en
def get_structure(wine_id):
    print(f"Get structure for wine id {wine_id}")
    url = f"{vivino_base_url}/wines/{wine_id}/tastes"
    print(url)
    response = requests.get(url, params = {"language": "en"}, headers = request_headers)
    print(f"Got structure response: status={response.status_code} wine_id: {wine_id}")
    if response.status_code == 200:
        return response.json()["tastes"]["structure"]
    else:
        return None

"""
https://www.vivino.com/api/explore/explore\?country_code\=US\&currency_code\=USD\&grape_filter\=varietal\&min_rating\=1\&order_by\=\&order\=\&price_range_max\=500\&price_range_min\=0\&wine_type_ids%5B%5D\=1\&wine_type_ids%5B%5D\=2\&wine_type_ids%5B%5D\=3\&wine_type_ids%5B%5D\=24\&wine_type_ids%5B%5D\=4\&wine_type_ids%5B%5D\=7\&page\=1\&language\=en 
"""
wine_types = {
    1: 'Red',
    2: 'White',
    3: 'Sparkling',
    4: 'Rosé',
    7: 'Dessert',
    24: 'Fortified'
}

r = requests.get(
    "https://www.vivino.com/api/explore/explore",
    params = {
        "country_code": "US",
        "currency_code":"USD",
        "grape_filter":"varietal",
        "min_rating":"1",
        "order_by":"",
        "order":"",
        "page": 1,
        "price_range_max":"500",
        "price_range_min":"0",
        "wine_type_ids":["1", "2", "3", "24", "4", "7"]
    },
    headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
)

print(f"Completed Explore API request: status={r.status_code}")

# api
# https://www.vivino.com/api/explore/explore\?country_code\=US\&currency_code\=USD\&grape_filter\=varietal\&min_rating\=1\&order_by\=\&order\=\&price_range_max\=500\&price_range_min\=0\&wine_type_ids%5B%5D\=1\&wine_type_ids%5B%5D\=2\&wine_type_ids%5B%5D\=3\&wine_type_ids%5B%5D\=24\&wine_type_ids%5B%5D\=4\&wine_type_ids%5B%5D\=7\&page\=1\&language\=en
# wine type, wine name, producer name (winery name), bold, tannic, sweet, acidic


results = []
for i, t in enumerate(r.json()["explore_vintage"]["matches"]):
    wine_id = t["vintage"]["wine"]["id"]
    print(f"Wine index={i} with id={wine_id} on page")
    if t["vintage"]["wine"]["style"] != None and i < 100:
        print("Sleeping for 5 seconds")
        time.sleep(5)
        print("Woke up after 5 seconds")
        results.append(
            (
                wine_types.get(int(t["vintage"]["wine"]["style"]["wine_type_id"]), t["vintage"]["wine"]["style"]["wine_type_id"]),
                t["vintage"]["wine"]["style"]["varietal_name"],
                t["vintage"]["wine"]["winery"]["name"],
                get_structure(wine_id)
            )   
        )
    else:
        print("Wine does not have a style")
        


# write csv file
with open('wines.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(results)

