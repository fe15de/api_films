from pydantic import BaseModel

class Film(BaseModel):
    url_name: list[str]
    showtimes: dict[str, str]