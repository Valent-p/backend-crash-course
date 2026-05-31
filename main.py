from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Data Model (the order form) ---
class BookmarkIn(BaseModel):
    url: str
    title: str
    description: str = ""

# --- In-Memory Storage (the pantry) --
bookmarks = {}
next_id = 1


@app.get("/bookmarks")
def get_bookmarks():
    return list(bookmarks.values())

@app.get("/bookmarks/{bookmark_id}")
def get_bookmark(bookmark_id: int):
    if bookmark_id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmarks[bookmark_id]

@app.post("/bookmarks", status_code=201)
def create_bookmark(bookmark: BookmarkIn):
    global next_id
    record = {"id": next_id, **bookmark.model_dump()}
    bookmarks[next_id] = record
    next_id += 1
    return record

@app.put("/bookmarks/{bookmark_id}")
def update_bookmark(bookmark_id: int, bookmark: BookmarkIn):
    if bookmark_id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    record = {"id": bookmark_id, **bookmark.model_dump()}
    bookmarks[bookmark_id] = record
    return record

@app.delete("/bookmarks/{bookmark_id}")
def delete_bookmark(bookmark_id: int):
    if bookmark_id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    del bookmarks[bookmark_id]
    return {"detail": "Bookmark deleted"}
