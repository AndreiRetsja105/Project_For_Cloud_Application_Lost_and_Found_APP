# Import Fast API <Creating backend API>
# Libratyes for version v0.1
#update <from fastapi import FastAPI to from fastapi import FastAPI, HTTPException, status>
from fastapi import FastAPI, HTTPException, status
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
# Updates libraries for version v0.2
from pydantic import BaseModel, Field
from typing import Literal

# Create Application and set its name and current version 
app = FastAPI(title="NCI_Lost_And_Found_API", version="0.2.0")


# Allow the local Frontend and Backend comunnicate together
# GET request to the API <other requests are under development>
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=False, allow_methods=["GET"], allow_headers=["*"],)

# Class ItemCreate for version v0.2
class ItemCreate(BaseModel):
    """"Validate data send by student when reporting """
    title: str=Field (min_lenght=3, max_lengh=100)
    description: str = Field (min_lenght=5, max_leght=500)
    category: Literal ["lost", "found"]
    Location: str = Field(min_lenght=2, max_leght=120)


class Item (ItemCreate):
    """"Information a saved item, include unique numeric identifier """

    id:int 

# use a temporary memory , not database  
#Information will disaper when backend resatrts 
#Database comes SQlite in new version block v0.3
items: list[Item] = [] 
next_item_id = 1


# GET for version v0.1
@app.get("/health", tags=["health"])
def health():
    """Cheack whether the API is running and return a simple JSON response"""
    return {"status": "ok", "application": "NCI_Lost_And_Found_API"}

@app.get("/items", response_model= list[Item], tags=["items"])
def get_items(category: Literal ["lost", "found" ]| None= None):
    """fingd all reports, if lost or found filter is suplied  """
    if category is None:
        return items 

    # The list generator selects elements matching the requested category.
    return [item for item in items if item.category == category ]

@app.get("/items/(item_id)", response_model= Item, tags=["items"])
def get_item(item_id: int):
    """find one report by the ID and return HTTP 404 if not exist"""

    for item in items:
        if item.id == item_id:
            return item

    raise HTTPException(status_code=404, details= "item not was found")

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["items"])
def create_item(payload: ItemCreate):
    """VAlidation a new report , generate Its ID, and store temporally """
    global next_item_id
    
    # pydantic CAlidation Payload Automaticly brfore this function run
    item = Item(id=next_item_id, **payload.model_dump()) 
    items.append(item)
    next_item_id += 1
    return item