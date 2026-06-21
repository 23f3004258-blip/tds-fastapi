from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv("q-fastapi.csv")

@app.get("/api")
def get_students(class_: list[str] | None = Query(None, alias="class")):
    data = df

    if class_:
        data = data[data["class"].isin(class_)]

    return {
        "students": data.to_dict(orient="records")
    }
