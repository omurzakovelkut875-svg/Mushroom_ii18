import uvicorn
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Mushroom Classification API")



model = joblib.load("model (4).pkl")
scaler = joblib.load("scaler (6).pkl")
label_encoder = joblib.load("label_encoder.pkl")



class Mushroom(BaseModel):
    cap_shape: str
    cap_surface: str
    cap_color: str
    bruises: str
    odor: str
    gill_size: str
    gill_color: str
    stalk_shape: str


@app.get("/")
def home():
    return {"message": "Mushroom_18 API is running"}



@app.post("/predict")
def predict(data: Mushroom):
    try:

        df = pd.DataFrame([data.dict()])




        scaled_data = scaler.transform(df)


        prediction = model.predict(scaled_data)


        try:
            prob = model.predict_proba(scaled_data).max()
        except AttributeError:
            prob = 1.0


        result_label = label_encoder.inverse_transform(prediction)[0]
        is_poisonous = True if result_label == 'p' else False

        return {
            "poisonous": is_poisonous,
            "probability": round(float(prob), 4),
            "class_label": result_label
        }

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8006)