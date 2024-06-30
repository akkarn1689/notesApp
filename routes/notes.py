from fastapi import APIRouter, FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from models.note import Note
from config.db import connection
from schemas.note import note_entity, notes_entity
import logging


note = APIRouter()
templates = Jinja2Templates(directory="templates")
db = connection.notes_database


@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    logging.debug("hello from get")
    print("this is get request")
    docs = db.notes.find({})
    new_docs = []

    for doc in docs:
        new_docs.append({
            "id": doc["_id"],
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"],
        })

    return templates.TemplateResponse(
        name="templates/index.html",
        context={"request": request, "newDocs": new_docs}
    )


@note.post("/")
async def create_item(request: Request):
    logging.debug("hello from post")
    form = await request.form()
    print(form)
    form_dict = dict(form)
    form_dict["important"] = True if form_dict.get("important") == "on" else False
    print(form_dict)
    inserted_note = db.notes.insert_one(form_dict)
    return {"Success": True}

# @note.post("/")
# async def create_item(
#     title: str = Form(...),
#     desc: str = Form(...),
#     important: str = Form(...),
# ):
#     try:
#         important_flag = important == "on"
#         note_data = {
#             "title": title,
#             "desc": desc,
#             "important": important_flag
#         }
#         print(note_data)  # Debugging print statement
#         inserted_note = db.notes.insert_one(note_data)
#         return {"Success": True, "InsertedID": str(inserted_note.inserted_id)}
#     except Exception as e:
#         return {"Success": False, "Error": str(e)}
