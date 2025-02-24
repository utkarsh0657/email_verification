from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from source_code import verify_email
import csv
import shutil
import os

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve templates
templates = Jinja2Templates(directory="templates")

os.makedirs("uploads", exist_ok=True)

class EmailRequest(BaseModel):
    email: str

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    """Serves the frontend UI."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/verify/")
async def verify_email_endpoint(request: EmailRequest):
    """Handles single email verification."""
    result = verify_email(request.email)
    return {"email": request.email, "status": "Valid" if result else "Invalid"}

@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    """Handles CSV uploads for bulk verification."""
    file_location = f"uploads/{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = []
    
    with open(file_location, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            email = row[0].strip()
            if email:
                status = "Valid" if verify_email(email) else "Invalid"
                results.append({"email": email, "status": status})

    return {"results": results}
