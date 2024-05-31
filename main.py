"""
Have these endpoints:

GET / -> list[airline_name]
GET /:airline_name -> list[flight_num]
GET /:airline_name/:flight_num -> Flight

POST /:airline
PUT /:airline/:flight_num
DELETE /:airline/:flight_num

"""
import json

from fastapi import FastAPI

from modules import Flight, Airlines_list


with open("airlines.json", "r") as f:
    flights_list = json.load(f)

app = FastAPI()

@app.get("/")
def get_airline():
    return list(flights_list.keys())

@app.get("/{airline_name}")
def get_flights(airline_name: Airlines_list):
    if airline_name.value in flights_list:
        flights = flights_list[airline_name.value]
        flight_numbers = [flight["flight_num"] for flight in flights]
        return flight_numbers

@app.get("/{airline_name}/{flight_num}")
def get_flight(airline_name: Airlines_list, flight_num: str):
    if airline_name.value in flights_list:
        airline_flights = flights_list[airline_name.value]
        for flight in airline_flights:
            if flight["flight_num"] == flight_num:
                return flight
            
@app.post("/{airline_name}")
def add_flight(airline_name: Airlines_list, flight: Flight):
    if airline_name.value in flights_list:
        flights_list[airline_name.value].append(flight.model_dump())

@app.put("/{airline_name}/{flight_num}")
def update_flight(airline_name: Airlines_list, flight_num: str, updated_flight: Flight):
    if airline_name.value in flights_list:
        for index, flight in enumerate(flights_list[airline_name.value]):
            if flight["flight_num"] == flight_num:
                flights_list[airline_name.value][index] = updated_flight.model_dump()


@app.delete("/{airline_name}/{flight_num}")
def delete_flight(airline_name: Airlines_list, flight_num: str):
    if airline_name.value in flights_list:
        for flight in flights_list[airline_name.value]:
            if flight["flight_num"] == flight_num:
                flights_list[airline_name.value].remove(flight)