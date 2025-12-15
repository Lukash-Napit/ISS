import requests
from geopy.distance import geodesic

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])
print("Location of ISS :")
print(f"Latitude = {iss_latitude} , Longitude = {iss_longitude}")

print("\n\n")

print("Your latitude and longitude are :")
lat,lon = float(input()),float(input())

iss = (iss_latitude,iss_longitude)
loc = (lat,lon)

print(f"Iss is {geodesic(iss,loc).km} km far from your location .")









