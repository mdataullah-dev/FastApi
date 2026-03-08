from pydantic import BaseModel


class productDTO(BaseModel):
    id: int
    title: str
    name: str
    price: int = 0 
    count: int = 0

