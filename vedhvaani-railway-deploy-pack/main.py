from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="VedhVaani Kundali API", description="Hindi/Marathi/English Kundali Generation API", version="1.0.0")

class KundaliRequest(BaseModel):
    name: str
    date_of_birth: str
    time_of_birth: str
    place: str
    language: str

@app.post("/kundali")
def generate_kundali(data: KundaliRequest):
    # Placeholder response
    return {
        "message": f"Kundali generated for {data.name} in {data.language}",
        "details": {
            "dob": data.date_of_birth,
            "time": data.time_of_birth,
            "place": data.place
        }
    }

@app.get("/")
def root():
    return {"status": "VedhVaani Kundali API running"}
