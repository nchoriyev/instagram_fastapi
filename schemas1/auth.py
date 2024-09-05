from pydantic import BaseModel
from typing import Optional

class Settings(BaseModel):
    authjwt_secret_key: str ='94e05900db3740c4b77e00f6daccc66d3190faf6a0526295b82473e543ca548d'