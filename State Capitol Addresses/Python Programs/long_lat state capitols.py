import json
import requests
import time

INPUT_FILE  = "state_capitals.json"   
OUTPUT_FILE = "state_capitals_with_coords.json"


CENSUS_GEOCODE_URL = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"

# Manual coordinates for addresses the Census Geocoder can't resolve
MANUAL_COORDS = {
    "Ohio":       (39.9612, -82.9988),   # 1 Capitol Square, Columbus
    "Delaware":   (39.1582, -75.5244),   # 410 Legislative Avenue, Dover
    "Tennessee":  (36.1672, -86.7816),   # 600 Dr. M.L.K. Jr. Boulevard, Nashville
    "Washington": (47.0379, -122.9007),  # 416 Sid Snyder Avenue Southwest, Olympia
}

def get_coordinates(address, city):
    """Look up latitude and longitude using the Census Geocoder API."""
    full_address = f"{address}, {city}"
    params = {
        "address": full_address,
        "benchmark": "Public_AR_Current",
        "format": "json"
    }

    try:
        response = requests.get(CENSUS_GEOCODE_URL, params=params, timeout=10)
        data = response.json()
        matches = data.get("result", {}).get("addressMatches", [])

        if matches:
            coords = matches[0]["coordinates"]
            return coords["y"], coords["x"]  # latitude, longitude
        else:
            print(f"  No match found for: {full_address}")
            return None, None

    except Exception as e:
        print(f"  Error geocoding {full_address}: {e}")
        return None, None


def add_coordinates(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        capitals = json.load(f)

    print(f"Processing {len(capitals)} records...\n")

    for entry in capitals:
        state   = entry.get("state", "Unknown")
        address = entry.get("StateCapitolAddress", "")
        city    = entry.get("StateCapitolCity", "")

        print(f"Geocoding: {state} — {address}, {city}")

        # Use manual coordinates for addresses the Census Geocoder can't resolve
        if state in MANUAL_COORDS:
            lat, lon = MANUAL_COORDS[state]
            print(f"  Using manual coordinates for {state}")
        else:
            lat, lon = get_coordinates(address, city)

        entry["latitude"]  = lat
        entry["longitude"] = lon

        time.sleep(0.5)
        
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(capitals, f, indent=4, ensure_ascii=False)

    success = sum(1 for e in capitals if e["latitude"] is not None)
    print(f"\nDone! {success}/{len(capitals)} addresses geocoded successfully.")
    print(f"Output saved to '{output_file}'")


if __name__ == "__main__":
    add_coordinates(INPUT_FILE, OUTPUT_FILE)
