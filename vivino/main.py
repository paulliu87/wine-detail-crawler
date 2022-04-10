import requests
import csv

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
        "order_by":"price",
        "order":"asc",
        "page": 1,
        "price_range_max":"500",
        "price_range_min":"0",
        "wine_type_ids":["1", "2", "3", "24", "4", "7"]
    },
    headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
)

results = [
    (
        wine_types.get(int(t["vintage"]["wine"]["style"]["wine_type_id"]), t["vintage"]["wine"]["style"]["wine_type_id"]),
        t["vintage"]["wine"]["style"]["varietal_name"]
    )
    for t in r.json()["explore_vintage"]["matches"] if t["vintage"]["wine"]["style"] != None
]

# write csv file
with open('wines.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(results)

