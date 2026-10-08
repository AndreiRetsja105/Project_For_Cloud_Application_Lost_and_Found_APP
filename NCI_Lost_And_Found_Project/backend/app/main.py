# Import Fast API <Creating backend API>

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create Application and set its name and current version 
app = FastAPI(title="NCI_Lost_And_Found_API", version="0.1.0")

# Allow the local Frontend and Backend comunnicate together
# GET request to the API <other requests are under development>
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=False, allow_methods=["GET"], allow_headers=["*"],)

@app.get("/health", tags=["health"])
def health():
    """Cheack whether the API is running and return a simple JSON response"""
    return {"status": "ok", "application": "NCI_Lost_And_Found_API"}