import requests
import matplotlib.pyplot as plt
import pandas as pd

API_KEY = "e0a1bf2c844edb9084efc764c089dd748676cc14"
API_URL = "https://api.jcdecaux.com/vls/v3/stations"

def fetch_station_data():
    # 
    # Fonction pour récupérer les données des stations de vélos depuis l'API JCDecaux.
    # Affiche dans la console pour chaque station:
    #   - Le nom de la station.
    #   - L'état de la station (Ouvert ou fermé).
    #   - Le nombre total de vélos qui peuvent se garer à la station.
    #   - Le nombre de vélos disponibles.
    #   - Le nombre de vélos mécaniques.
    #   - Le nombre de vélos électriques.
    #   - Le nombre de places de stationnement disponibles.
    #   - La ville de la station.
    #   - L'adresse de la station.
    # Retourne les données sous forme de liste de dictionnaires.
    # 
    params = {"apiKey": API_KEY}
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        for station in data:
            print("Station:", station["name"])
            print("Etat de la station:", station["status"])
            print("Nombres de vélos:", station["totalStands"]["capacity"])
            print("Vélos disponibles:", station["mainStands"]["availabilities"]["bikes"])
            print("Vélos mécaniques:", station["totalStands"]["availabilities"]["mechanicalBikes"])
            print("Vélos électriques:", station["totalStands"]["availabilities"]["electricalBikes"])
            print("Places de stationnement disponibles:", station["mainStands"]["availabilities"]["stands"])
            print("Ville:", station["contractName"])
            print("Adresse:", station["address"])
        return data
    else:
        print("Erreur lors de la récupération des données depuis l'API JCDecaux")
        return None

def count_stations_by_city(station_data):
    # 
    # Fonction pour compter le nombre de stations par ville.
    # Retourne un dictionnaire avec les villes comme clés et le nombre de stations comme valeurs.
    # 
    city_station_count = {}

    for station in station_data:
        city = station["contractName"]
        if city in city_station_count:
            city_station_count[city] += 1
        else:
            city_station_count[city] = 1

    return city_station_count

def plot_city_station_count(city_station_count):
    # 
    # Fonction pour tracer un graphique barres du nombre de stations par ville.
    # 
    cities = list(city_station_count.keys())
    station_counts = list(city_station_count.values())

    plt.figure(figsize=(10, 6))
    plt.barh(cities, station_counts, color='skyblue')
    plt.xlabel('Nombre de stations')
    plt.ylabel('Ville')
    plt.title('Nombre de stations de vélos par ville')
    plt.show()


def main():
    station_data = fetch_station_data()
    if station_data:
        city_station_count = count_stations_by_city(station_data)
        sorted_city_station_count = dict(sorted(city_station_count.items(), key=lambda item: item[1], reverse=True))
        plot_city_station_count(sorted_city_station_count)

if __name__ == "__main__":
    main()