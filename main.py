from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10),
    Timestamp(id=3, timestamp=110)
]

# путь /
@app.get('/')
def root():
    return JSONResponse(content={"message": "Welcome to veterinary clinic service!"})

# путь /post
@app.post('/post')
def create_post(timestamp: Timestamp):
    post_db.append(timestamp)
    return timestamp

# запись собак
@app.post("/dog")
def create_dog(dog: Dog):
    if dog.pk in list(dogs_db.keys()):
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists.')
    dogs_db[dog.pk] = dog
    return dog

# получение списка собак
@app.get("/dog")
def get_dogs(kind: DogType = None):
    if kind is not None:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return list(dogs_db.values())

# получение собаки по id
@app.get('/dog/{pk}')
def get_dog(pk: int):
    return dogs_db.get(pk)

# получение собак по типу
@app.get('/dog')
def get_dogs_by_type(kind: DogType):
    return [dog for dog in dogs_db.values() if dog.kind == kind]

# обновление собаки по id
@app.patch('/dog/{pk}')
def update_dog(pk: int, updated_dog: Dog):
    if pk in dogs_db:
        dogs_db[pk] = updated_dog
        return updated_dog
    return None
