import requests
import time
import pandas as pd
from datetime import datetime
from geopy.distance import geodesic
import matplotlib.pyplot as plt

ISS_API = "http://api.open-notify.org/iss-now.json"

data_list = []

def get_iss_location():
    response = requests.get(ISS_API)
    data = response.json()
    lat = float(data["iss_position"]["latitude"])
    lon = float(data["iss_position"]["longitude"])
    timestamp = datetime.fromtimestamp(data["timestamp"])
    return lat, lon, timestamp


print("Tracking ISS every 5 seconds for 1 minute...\n")
for i in range(4):
    lat, lon, ts = get_iss_location()
    print(f"{ts} -> Latitude: {lat}, Longitude: {lon}")

    data_list.append({
        "Time": ts,
        "Latitude": lat,
        "Longitude": lon
    })

    time.sleep(15)

df = pd.DataFrame(data_list)
df.to_csv("iss_tracking.csv", index=False)
print("\nISS locations saved to iss_tracking.csv")


start = (df.iloc[0]["Latitude"], df.iloc[0]["Longitude"])
end = (df.iloc[-1]["Latitude"], df.iloc[-1]["Longitude"])

distance_km = geodesic(start, end).kilometers
print(f"\nDistance travelled by ISS in 1 minute: {distance_km:.2f} km")


plt.figure()
plt.plot(df["Longitude"], df["Latitude"], marker='o')
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("ISS Movement Over 1 Minute")
plt.grid(True)
plt.show()
