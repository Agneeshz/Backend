from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import data
import pickle
import json
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["https://flood-warning-system.vercel.app/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=['*']
)


class model_input(BaseModel):

    date: str


# loading the saved model
# just need to input ml model file here
waterlevel_model = pickle.load(open('model.sav', 'rb'))


@app.post('/waterlevel_prediction')
def waterlevel_pred(input_parameters: model_input):

    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)

    print(input_dictionary)

    # max = input_dictionary['Max']
    # min = input_dictionary['Min']
    # windspeed = input_dictionary['Windspeed']
    # rainfall = input_dictionary['Rainfall']
    # humidity = input_dictionary['Humidity']

    max = data.date[input_dictionary['date']]['Max']
    min = data.date[input_dictionary['date']]['Min']
    windspeed = data.date[input_dictionary['date']]['Windspeed']
    rainfall = data.date[input_dictionary['date']]['Rainfall']
    humidity = data.date[input_dictionary['date']]['Humidity']

    input_list = [max, min, windspeed, rainfall, humidity]

    prediction = waterlevel_model.predict([input_list])

    return prediction[0]
