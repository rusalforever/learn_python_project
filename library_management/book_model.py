from pydantic import BaseModel

class BookModel(BaseModel):
    title: str
    author: str
    year_of_publication: int
    