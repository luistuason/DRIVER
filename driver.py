import csv
import requests

# Set to true to output in CSV, false to output in JSON
OUTPUT_IN_CSV = True

headers = {
    "Authorization": "Token adc7bbce935c6b230d40449de40f05d387e78128"
}

get = requests.get("https://roadsafety.gov.ph/api/records/", headers=headers)
csv_fieldnames = [
    "uuid",
    "location",
    "lat",
    "long",
    "time",
    "description",
    "agency",
    "cause",
    "collision_type",
    "severity",
    "city",
    "district",
    "neighborhood",
    "road",
    "weather",
    "light"
]

with open("driver.{0}".format("csv" if OUTPUT_IN_CSV else "json"), "w", encoding='utf-8') as driver_file:
    if OUTPUT_IN_CSV:
        writer = csv.DictWriter(driver_file, fieldnames=csv_fieldnames, lineterminator='\n')
        writer.writeheader()
        while get.json()["next"] is not None:
            for result in get.json()["results"]:
                data = {}
                data["uuid"] = result["uuid"]
                data["location"] = result["location_text"]
                data["lat"] = result["geom"]["coordinates"][1]
                data["long"] = result["geom"]["coordinates"][0]
                data["time"] = result["occurred_from"]
                data["description"] = result["data"].get("incidentDetails", {}).get("Description")
                data["agency"] = result["data"].get("incidentDetails", {}).get("Reporting Agency")
                data["cause"] = result["data"].get("incidentDetails", {}).get("Main cause")
                data["collision_type"] = result["data"].get("incidentDetails", {}).get("Collision type")
                data["severity"] = ','.join(result["data"].get("incidentDetails", {}).get("Severity"))
                data["city"] = result["city"]
                data["district"] = result["county"]
                data["neighborhood"] = result["neighborhood"]
                data["road"] = result["road"]
                data["weather"] = result["weather"]
                data["light"] = result["light"]
                writer.writerow(data)
            get = requests.get(get.json()["next"], headers=headers)
