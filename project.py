from shelve import BsdDbShelf
from pymongo import MongoClient

from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import datetime, time
    
client = MongoClient('mongodb://localhost', 27017) 

# TODO fill in database name
db = client["project"]

# TODO fill in collection name
toilet = db["toilet"]
toilet_savetime = db["toilet_savetime"]

app = FastAPI()

# TODO complete all endpoint.
@app.get("/")
def get_root():  
    return "toilet"

@app.get("/get_room/{room_No}")
def get_room(room_No: int):  
    room = toilet.find_one({"room_No":room_No},{"_id":0})
    if room != None :
        return room
    raise HTTPException( status_code = 405 , detail = { "msg" : "no room" } )

@app.get("/get_time")
def get_time():  
    roomtime = toilet_savetime.find({},{"_id":0})
    if roomtime != [] :
        alltime = 0
        people = 0
        for i in roomtime :
            alltime += i["time"]
            people += i["number"]
        if people == 0 :
            return 0
        return alltime/people
    raise HTTPException( status_code = 405 , detail = { "msg" : "no room" } )

@app.get("/get_time/{room_No}")
def get_time(room_No: int):  
    roomtime = toilet_savetime.find_one({"room_No":room_No},{"_id":0})
    if roomtime != None :
        return roomtime
    raise HTTPException( status_code = 405 , detail = { "msg" : "no room" } )
    
    
@app.post("/make/{room_No}")
def make(room_No : int):
    room = toilet.find_one({"room_No":room_No},{"_id":0})
    if room != None :
        return room
    raise HTTPException( status_code = 405 , detail = { "msg" : "already have this room" } )
    


@app.put("/update_in/{room_No}")
def update_in(room_No: int):
    room = toilet.find_one({"room_No":room_No},{"_id":0})
    if(room["status"]==1):
        return {
            "result" : "Not Empty"
    }
    myquery = {"room_No":room_No}
    newvalues = { "$set": { "status": 1,"datetime" : datetime.datetime.now() } }
    toilet.update_one(myquery, newvalues)
    return {
        "result" : "Success"
    }
    
@app.put("/update_out/{room_No}")
def update_out(room_No: int):
    room = toilet.find_one({"room_No":room_No},{"_id":0})
    room_savetime = toilet_savetime.find_one({"room_No":room_No},{"_id":0})
    if(room["status"]==0):
        return {
            "result" : "Error"
        }
    myquery = {"room_No":room_No}
    x = (datetime.datetime.now() - room["datetime"]) 
    #print(type(x)) print(x)    print(y)
    y = x.total_seconds() 
    
    x = y + room_savetime["time"]
    newvalues1 = { "$set": { "status": 0} }
    newvalues2 = { "$set": { "time" : x, "number" : room_savetime["number"]+1 } }
    toilet.update_one(myquery, newvalues1)
    toilet_savetime.update_one(myquery,newvalues2)
    return{
        "result" : "success"
    }

'''toilet
_id : ...
room_No : int
status : ...
datetime : ...
'''

'''savetime
_id : ...
room_No : int
time : ...
number : ...
'''