from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import run_pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class InputText(BaseModel):
    text: str

@app.post("/predict")
def predict_api(input: InputText):
    return run_pipeline(input.text)