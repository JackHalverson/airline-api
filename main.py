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

@app.get("/airline")
def get_airline():
    return list(flights_list.keys())

@app.get("/airline/{airline_name}")
def get_flights(airline_name: Airlines_list):
    return flights_list[airline_name.value]

@app.get("/airline/{airline_name}/{flight_num}")
def get_flight(airline_name: Airlines_list, flight_num: str):
    if airline_name.value in flights_list:
        airline_flights = flights_list[airline_name.value]
        for flight in airline_flights:
            if flight["flight_num"] == flight_num:
                return flight

@app.post("/airline")
def create_flight(flight: Flight):
    flights_list.append(flight)

@app.put("/airline/{airline_name}/{flight_num}")
def update_flight(airline_name: Airlines_list, flight: Flight, flight_num: str):
    if airline_name.value in flights_list:
        airline_flights = flights_list[airline_name.value]
        for i, existing_flight in enumerate(airline_flights):
            if existing_flight["flight_num"] == flight_num:
                airline_flights[i] = flight.model_dump()
                return {"message": "Flight updated successfully"}

@app.delete("/airline/{airline_name}/{flight_num}")
def delete_flight(airline_name: Airlines_list, flight: Flight, flight_num: str):
    if airline_name.value in flights_list:
        airline_flights = flights_list[airline_name.value]
        for i, existing_flight in enumerate(airline_flights):
            if existing_flight["flight_num"] == flight_num:
                del airline_flights[i]
                return {"message": "Flight updated successfully"}