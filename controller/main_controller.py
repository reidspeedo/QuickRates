from fastapi import FastAPI, status
from pydantic import BaseModel
import uvicorn
from services import prequote as cd
from services import model as smd

app = FastAPI()

class PreQuote(BaseModel):
    name: str
    zip: int
    dob: str
    gender: str
    dwelling: str
    deductible: str

#Create new prequote
@app.get("/")
async def get_prequote():
    response = cd.get_prequote()
    return response

@app.post("/get-quickrate")
async def create_prequote(prequote: PreQuote):
    quickrate = cd.create_prequote(dict(prequote))
    return {'quickrate': quickrate}

# #Read new prequote
# @app.get("/")
# async def get_prequote(prequote: PreQuote):
#     return dict(prequote)
#
# #Update prequote
# @app.put("/")
# async def update_prequote(prequote: PreQuote):
#     return dict(prequote)
#
# #Delete prequote
# @app.delete("/")
# async def delete_prequote(prequote: PreQuote):
#     return dict(prequote)

#Update/Create linear regression model

@app.post("/linear-regression")
async def update_model(file=r'/Users/reidrelatores/PycharmProjects/QuickRate/linear_model/training_data.csv'):
    id = smd.update_model(file)
    return id

if __name__ == "__main__":
    uvicorn.run("main_controller:app", host='127.0.0.1', port=8000)