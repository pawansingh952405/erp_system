import requests 
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware 
from sqlalchemy.orm import Session
from pydantic import BaseModel # Added for data validation
from typing import List # Added for list of items
import models
from database import engine, get_db


# Create tables in Postgres
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 1. MIDDLEWARE (Keep this at the top)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. SCHEMAS (Required to receive data from your HTML form)
class ItemSchema(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class POSchema(BaseModel):
    reference_no: str
    vendor_id: int
    items: List[ItemSchema]

# 3. STATIC FILES & ROUTES
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")

@app.get("/create")
def read_create():
    return FileResponse("static/create_po.html")

# 4. API ENDPOINTS

@app.get("/vendors")
def get_vendors(db: Session = Depends(get_db)):
    return db.query(models.Vendor).all()

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.PurchaseOrder).all()

# THE SUBMIT LOGIC (This makes your form work!)
@app.post("/orders")
def create_order(po: POSchema, db: Session = Depends(get_db)):
    subtotal = 0
    for item in po.items:
        subtotal += (item.unit_price * item.quantity)
    
    # 5% Tax Calculation (Assignment Requirement)
    tax = subtotal * 0.05
    final_total = subtotal + tax

    new_order = models.PurchaseOrder(
        reference_no=po.reference_no,
        vendor_id=po.vendor_id,
        total_amount=final_total,
        status="Submitted"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"status": "success", "total_with_tax": final_total}


# Ensure this is at the top (pip install requests)

# Replace with your actual key from Google AI Studio
GEMINI_API_KEY = "YOUR_ACTUAL_KEY_HERE"

@app.get("/ai-description/{product_name}")
def get_ai_description(product_name: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    # The "Prompt" tells the AI exactly what to do
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Write a professional 2-sentence marketing description for a product named '{product_name}'."
            }]
        }]
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        # Navigate the JSON response to get the text
        description = data['candidates'][0]['content']['parts'][0]['text']
        return {"description": description.strip()}
    except Exception as e:
        # Fallback if the API fails or key is wrong
        return {"description": f"High-quality {product_name} for professional business use."}