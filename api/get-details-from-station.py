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

def percentage_to_kW(percentage, capacity):
    return percentage * capacity / 100

def calculate_distance(departure_coordinates: List[float], destination_coordinates: List[float]) -> float:
        client = boto3.client('location', region_name='eu-west-1')
        calculator_name = 'powernap'
        response = client.calculate_route(
            CalculatorName=calculator_name,
            DeparturePosition=departure_coordinates,
            DestinationPosition=destination_coordinates,
            TravelMode='Walking',
            DistanceUnit='Kilometers'
        )

        return response["Legs"][0]["Distance"]

class Response:
    def __init__(self, departure_coordinates, current_battery, desired_battery, station_id):
        self.departure_coordinates = departure_coordinates
        self.longitude = self.departure_coordinates[0]
        self.latitude = self.departure_coordinates[1]
        self.current_battery = current_battery
        self.desired_battery = desired_battery
        self.station_id = station_id
    
    def api_response(self, limit=10, distance=1000):
        URL = f"https://mobility.api.opendatahub.com/v2/tree/EChargingPlug?limit={limit}&offset=0&where=scoordinate.dlt.%28{distance}%2C{self.longitude}%2C{self.latitude}%2C4326%29&shownull=false&distinct=true"
        r = requests.get(URL).json()
        data = r["data"]["EChargingPlug"]["stations"].items()
        return data
        
    def calculate_estimated_charge_time(self, battery_capacity: float, current_battery: float, desired_battery: float, power: float) -> float:
        desired_battery = percentage_to_kW(self.desired_battery, battery_capacity)
        current_battery = percentage_to_kW(self.current_battery, battery_capacity)
        return (desired_battery - current_battery) * 60 / power
    
    def create_response(self):
        stations = {}
        with suppress(KeyError):
            for station, station_content in self.api_response():
                if station == self.station_id:
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
                        charging_time = self.calculate_estimated_charge_time(100, self.current_battery, self.desired_battery, max_power)
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
                        "charging_time": charging_time,
                        "location": {
                            "latitude": coordinate['x'],
                            "longitude": coordinate['y']
                        }}
            return stations

def lambda_handler(event, context):
    query_params = event.get('queryStringParameters', {})
    required_params = ['longitude', 'latitude', 'station_id', 'current_battery', 'desired_battery']
    missing_params = [param for param in required_params if param not in query_params]
    if missing_params:
        return {
            'statusCode': 422,
            'body': json.dumps({'error': f'Missing parameters: {", ".join(missing_params)}'})
        }

    longitude = float(query_params['longitude'])
    latitude = float(query_params['latitude'])
    current_battery = float(query_params['current_battery'])
    desired_battery = float(query_params['desired_battery'])
    station_id = str(query_params['station_id'])
    
    try:
        departure_coordinates = [longitude, latitude]
        res = Response(departure_coordinates, current_battery, desired_battery, station_id)
        if res:
            return_obj = res.create_response().get(station_id)
            if return_obj:
                return {
                    'statusCode': 200,
                    'body': json.dumps(return_obj),
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    }
                }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps("The given station_id did not return a result"),
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    }
                }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps("The given parameters did not find a valid response"),
                'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                }
            }
    except Exception as e:
        return {
            'statusCode': 502,
            'body': json.dumps(f"Exception: {e}"),
            'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
        }