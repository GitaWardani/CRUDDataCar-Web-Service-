from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

app = FastAPI()


cars_db = []


class Car(BaseModel):
    brand: str
    model: str
    year: int
    color: str



@app.post("/cars/", response_model=Car)
def create_car(car: Car):
    cars_db.append(car)
    return car


@app.get("/cars/", response_model=List[Car])
def read_cars():
    return cars_db


@app.get("/cars/{car_id}", response_model=Car)
def read_car(car_id: int):
    if car_id < 0 or car_id >= len(cars_db):
        raise HTTPException(status_code=404, detail="Car not found")
    return cars_db[car_id]

@app.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: int, updated_car: Car):
    if car_id < 0 or car_id >= len(cars_db):
        raise HTTPException(status_code=404, detail="Car not found")
    
    current_car = cars_db[car_id]
    current_car.brand = updated_car.brand
    current_car.model = updated_car.model
    current_car.year = updated_car.year
    current_car.color = updated_car.color
    
    return current_car


@app.delete("/cars/{car_id}", response_model=Car)
def delete_car(car_id: int):
    if car_id < 0 or car_id >= len(cars_db):
        raise HTTPException(status_code=404, detail="Car not found")
    
    deleted_car = cars_db.pop(car_id)
    return deleted_car


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)
