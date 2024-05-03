from pydantic import BaseModel, ConfigDict
from typing import List


class ProductBase(BaseModel):
    name: str
    desc: str
    price: int
    is_actual: bool

    model_config = ConfigDict(from_attributes=True)


class SellerCreate(BaseModel):
    sellername: str
    products: List[ProductBase]

    model_config = ConfigDict(from_attributes=True)


class SellerRead(BaseModel):
    sellername: str

    model_config = ConfigDict(from_attributes=True)

class SellerProducts(BaseModel):
    sellername: str
    products: List[ProductBase]

    model_config = ConfigDict(from_attributes=True)
