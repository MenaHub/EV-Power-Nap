import json
import requests
import boto3
from typing import List
from contextlib import suppress
import random

def get_price(provider, power):
        # Source: https://www.neogy.it/en/public-network-charging/direct-payment.html
        if provider in ["DOLOMITI", "ALPERIA", "NEOGY"]:
            if power >= 75: # Uses DC
                return 0.89
            else: # Uses AC
                return 0.65
        elif provider == "route220": # Only uses AC
            if power <= 22:
                return 0.45
            return None
        else:
            return None

def calculate_distance(departure_coordinates: List[float], destination_coordinates: List[float]) -> float:
        client = boto3.client('location', region_name='eu-west-1')
        calculator_name = 'powernap'
        response = client.calculate_route(
            CalculatorName=calculator_name,
            DeparturePosition=departure_coordinates,
            DestinationPosition=destination_coordinates,
            TravelMode='Walking',  # or 'Truck', 'Walking', 'Bicycle'
            DistanceUnit='Kilometers'
        )

        return response["Legs"][0]["Distance"]

def percentage_to_kW(percentage, capacity):
    return percentage * capacity / 100

def calculate_heuristic(station, distance, max_power, cost_per_kwh, socket_compatibility, stop_duration, battery_current, battery_desired, weights):
    distance_weight, charging_weight, cost_weight = weights
    battery_desired = percentage_to_kW(battery_desired, 100)
    battery_current = percentage_to_kW(battery_current, 100)
    eng_required = battery_desired - battery_current
    eng_charged = max_power * stop_duration

    socket_compatibility = socket_compatibility  #it can be either 0 (non-compatible) or 1 (compatible)
    H = ((distance_weight / distance) + (charging_weight * min(1, eng_charged/eng_required)) - (cost_weight * cost_per_kwh)) * socket_compatibility
    return H

class Response:
    def __init__(self, departure_coordinates):
        self.departure_coordinates = departure_coordinates
        self.longitude = self.departure_coordinates[0]
        self.latitude = self.departure_coordinates[1]
    
    def api_response(self, limit=200, distance=1000):
        URL = f"https://mobility.api.opendatahub.com/v2/tree/EChargingPlug?limit={limit}&offset=0&where=scoordinate.dlt.%28{distance}%2C{self.longitude}%2C{self.latitude}%2C4326%29&shownull=false&distinct=true"
        print(URL)
        r = requests.get(URL).json()
        data = r["data"]["EChargingPlug"]["stations"].items()
        return data
    
    def create_response(self):
        stations = {}
        with suppress(KeyError):
            for station, station_content in self.api_response():
                coordinate = station_content["scoordinate"]
                station_coordinates = [coordinate['x'], coordinate['y']]
                distance = calculate_distance(
                    departure_coordinates = self.departure_coordinates,
                    destination_coordinates = station_coordinates
                )
                provider = station_content["sorigin"]
                plugs = []
                for plug in station_content["smetadata"]["outlets"]:
                    max_power = plug["maxPower"]
                    max_current = plug["maxCurrent"]
                    socket_type = plug["outletTypeCode"]
                    cost_per_kwh = get_price(provider, max_power)
                    if max_power > 350:
                        if max_current == 10:
                            max_power = max_power/1000
                        else:
                            print(f"current: {max_current}, power: {max_power}")
                    plugs.append({
                        "max_power": max_power,
                        "max_current": max_current,
                        "cost_per_kwh": cost_per_kwh,
                        "socket_type": socket_type
                    })
                stations[station] = {
                    "distance": distance,
                    "provider": provider,
                    "plugs": plugs,
                    "location": {
                        "latitude": coordinate['x'],
                        "longitude": coordinate['y']
                    }}
            return stations

def get_map_pins_and_heuristic(stations):
    stop_duration = 10
    battery_current = 20
    battery_desired = 80
    heuristic_list = []
    for station in stations:
        distance = stations[station]['distance']
        location = (stations[station]['location']['latitude'], stations[station]['location']['longitude'])
        for plug in stations[station]['plugs']:
            max_power = plug['max_power']
            cost_per_kwh = plug['cost_per_kwh']
            socket_compatibility = 1
            rank = calculate_heuristic(station, distance, max_power, cost_per_kwh, socket_compatibility, stop_duration = stop_duration, battery_current = battery_current, battery_desired = battery_desired, weights = (1, 1, 1))
            heuristic_list.append({
                "location": location,
                "rank": rank,
                "station_id": station
            })
    return (heuristic_list) #TODO: Sort by heuristic

def lambda_handler(event, context):
    query_params = event.get('queryStringParameters', {})
    
    longitude = float(query_params.get('longitude', 11.324950653648349))
    latitude = float(query_params.get('latitude', 46.494720780246034))

    departure_coordinates = [longitude, latitude]
    res = Response(departure_coordinates)
    stations = res.create_response()
    return_obj = get_map_pins_and_heuristic(stations)
    
    return {
        'statusCode': 200,
        'body': return_obj
    }