import requests
import time
import pandas as pd
from datetime import datetime
from geopy.distance import geodesic
import folium

ISS_API = "http://api.open-notify.org/iss-now.json"

data = []

def get_iss_location():
    response = requests.get(ISS_API)
    result = response.json()
    lat = float(result["iss_position"]["latitude"])
    lon = float(result["iss_position"]["longitude"])
    timestamp = datetime.fromtimestamp(result["timestamp"])
    return lat, lon, timestamp


print("Tracking ISS every 5 seconds for 1 minute...\n")

for i in range(12):
    lat, lon, ts = get_iss_location()
    print(f"{ts} → Latitude: {lat}, Longitude: {lon}")

    data.append({
        "Time": ts,
        "Latitude": lat,
        "Longitude": lon
    })

    time.sleep(5)

df = pd.DataFrame(data)
df.to_csv("iss_1min_tracking.csv", index=False)
print("\nData saved to iss_1min_tracking.csv")


total_distance = 0.0

for i in range(len(df) - 1):
    p1 = (df.iloc[i]["Latitude"], df.iloc[i]["Longitude"])
    p2 = (df.iloc[i + 1]["Latitude"], df.iloc[i + 1]["Longitude"])
    total_distance += geodesic(p1, p2).kilometers

total_time_seconds = 60
speed_km_s = total_distance / total_time_seconds

print(f"\nTotal distance travelled in 1 minute: {total_distance:.2f} km")
print(f"Average ISS speed: {speed_km_s:.2f} km/s")


start_point = [df.iloc[0]["Latitude"], df.iloc[0]["Longitude"]]
iss_map = folium.Map(location=start_point, zoom_start=4)

path = list(zip(df["Latitude"], df["Longitude"]))

folium.PolyLine(path, color="red").add_to(iss_map)

for lat, lon in path:
    folium.CircleMarker(
        location=[lat, lon],
        radius=3,
        color="blue",
        fill=True
    ).add_to(iss_map)

iss_map.save("iss_1min_map.html")

print("\nMap saved as iss_1min_map.html")


