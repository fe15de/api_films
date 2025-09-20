from pydantic import BaseModel

class Film(BaseModel):
    url_name: str
    showtimes: dict[str, str]