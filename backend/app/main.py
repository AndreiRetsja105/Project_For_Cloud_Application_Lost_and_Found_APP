# Import Fast API <Creating backend API>
# Libratyes for version v0.1
#update <from fastapi import FastAPI to from fastapi import FastAPI, HTTPException, status>
from fastapi import FastAPI, HTTPException, Response, status
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
# Updates libraries for version v0.2
from pydantic import BaseModel, Field
from typing import Literal
# update Librays for v0.3
from contextlib import asynccontextmanager
# add database SQLite
from . import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create an SQLite table when the FastAPI server starts"""
    database.initialse_database()
    yield ## FastAPI processes requests until the application stop run 

    
# Create Application and set its name and current version 
app = FastAPI(title="NCI_Lost_And_Found_API", version="0.3.0", lifespan=lifespan)


# Allow the local Frontend and Backend comunnicate together
# GET request to the API <other requests are under development>
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=False, allow_methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["*"],)

# Class ItemCreate for version v0.3
class ItemCreate(BaseModel):
    """
    Validate the information submitted by a student
    when reporting a lost or found item.
    """

    # item title must contain between 3 and 100 characters.
    title: str = Field(min_length=3, max_length=100)

    # description provides more details about the item.
    description: str = Field(min_length=5, max_length=500)

    # only two report categories are allowed.
    category: Literal["lost", "found"]

    # location where the item was lost or found.
    location: str = Field(min_length=2, max_length=120)

    # current status of the reported item.
    status: str


class Item(ItemCreate):
    """"Information a saved item, include unique numeric identifier """

    id:int 

# use a temporary memory , not database  
#Information will disaper when backend resatrts 
#Database comes SQlite in new version block v0.3
#items: list[Item] = [] 
#next_item_id = 1


# GET for version v0.1
@app.get("/health", tags=["health"])
def health():
    """Cheack whether the API is running and return a simple JSON response"""
    return {"status": "ok", "application": "NCI_Lost_And_Found_API"}


@app.get("/items", response_model= list[Item], tags=["items"])
def get_items(category: Literal ["lost", "found" ]| None= None):
    """fingd all reports, if lost or found filter is suplied  """
    #was in the version 2 
    #if category is None:
       # return items 
    # The list generator selects elements matching the requested category.
    #return [item for item in items if item.category == category ]
    
    # version 3 connect to the data base
    # list items from category on databse  
    return database.list_items(category)


@app.get("/items/(item_id)", response_model= Item, tags=["items"])
def get_item(item_id: int):
    """find one report by the ID and return HTTP 404 if not exist"""
    # it was in the version 2 
    #for item in items:
    #   if item.id == item_id:
    #        return item

    # version 3
    # loking Item in data base , if item is none it will show 404 
    item = database.find_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail= "Item not found")
    return item


@app.post("/items", response_model=Item, status_code=201, tags=["items"])
def create_item(payload: ItemCreate):
    #version 2
    #"""VAlidation a new report , generate Its ID, and store temporally """
    #global next_item_id
  
    # pydantic CAlidation Payload Automaticly brfore this function run
    #item = Item(id=next_item_id, **payload.model_dump()) 
    #items.append(item)
    #next_item_id += 1
    #return item

    # version 3
    """Validate the new lost/found report and save it to SQLite."""
    return database.insert_item(payload.model_dump())   


@app.put("/items/{item_id}", response_model=Item, tags=["items"])
def update_item(item_id: int, payload: ItemCreate):
    """replace the information about the existing report/respond with an HTTP 404"""
    
    updated = database.replace_item(item_id, payload.model_dump())
    
    # Return 404 if the ID does not exist.
    if updated is None:
    
        raise HTTPException(status_code= 404, detail="Item not found")
    
    return updated



@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["items"])
def remove_item(item_id: int):
    """delete an existing report/return an HTTP 404 response if it not exist"""
    if not database.delete_item(item_id):
        raise HTTPException(status_code=404, detail="item not was found")
    
    # return HTTP 204 without a response body
    return Response(status_code=status.HTTP_204_NO_CONTENT)