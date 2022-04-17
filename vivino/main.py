import requests
import csv
import time

vivino_base_url = 'https://www.vivino.com/api'
request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
}

def get_request(path, params, sleep):
    if (sleep == True):
        time.sleep(5)
    return requests.get(f"{vivino_base_url}{path}", params = params, headers = request_headers)

# api for structure
# https://www.vivino.com/api/wines/1695288/tastes\?language\=en
def get_structure(wine_id):
    response = get_request(
        f"/wines/{wine_id}/tastes", 
        params = {"language": "en"}, 
        sleep = True
    )
    print(f"Got structure response: status={response.status_code} wine_id: {wine_id}")
    if response.status_code == 200:
        data = response.json()["tastes"]["structure"]
        if (data != None):
            structure = dict()
            structure['acidity'] = data["acidity"]
            structure['intensity'] = data["intensity"]
            structure['sweetness'] = data["sweetness"]
            structure['tannin'] = data["tannin"]
            return structure
        else:
            return None
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

r = get_request(
    "/explore/explore",
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
    sleep = False
)

print(f"Completed Explore API request: status={r.status_code}")

# api
# https://www.vivino.com/api/explore/explore\?country_code\=US\&currency_code\=USD\&grape_filter\=varietal\&min_rating\=1\&order_by\=\&order\=\&price_range_max\=500\&price_range_min\=0\&wine_type_ids%5B%5D\=1\&wine_type_ids%5B%5D\=2\&wine_type_ids%5B%5D\=3\&wine_type_ids%5B%5D\=24\&wine_type_ids%5B%5D\=4\&wine_type_ids%5B%5D\=7\&page\=1\&language\=en
# wine type, wine name, producer name (winery name), bold, tannic, sweet, acidic

results = []
# write csv file
with open('wines.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows([('wine id', 'wine type', 'vintage year', 'varietal name', 'winery name', 'structure')])

    for i, t in enumerate(r.json()["explore_vintage"]["matches"]):
        wine_id = t["vintage"]["wine"]["id"]
        print(f"Wine index={i} with id={wine_id} on page")
        if t["vintage"]["wine"]["style"] != None and i < 10:
            results.append(
                (
                    wine_id,
                    wine_types.get(int(t["vintage"]["wine"]["style"]["wine_type_id"]), t["vintage"]["wine"]["style"]["wine_type_id"]),
                    t["vintage"]["year"],
                    t["vintage"]["wine"]["style"]["varietal_name"],
                    t["vintage"]["wine"]["winery"]["name"],
                    get_structure(wine_id)
                )   
            )
        else:
            print("Wine does not have a style")
    
    writer.writerows(results)

