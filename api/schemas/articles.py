from pydantic import BaseModel
from typing import Optional

class ArticleBase(BaseModel):
    """Modelo base para artículos de noticias"""
    title: str
    summary: Optional[str] = None
    source: str


class ArticleCreate(ArticleBase):
    """Modelo para creación de artículos"""

    class Config:
        schema_extra = {
            "example": {
                "title": "NASA anuncia misión a Marte",
                "summary": "La NASA confirmó que enviará una nueva misión tripulada a Marte en 2030.",
                "source": "NASA News",
            }
        }


class Article(ArticleBase):
    """Modelo que representa un artículo completo en la BD"""
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "NASA anuncia misión a Marte",
                "summary": "La NASA confirmó que enviará una nueva misión tripulada a Marte en 2030.",
                "source": "NASA News",
                
            }
        }
