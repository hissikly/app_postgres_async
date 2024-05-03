from fastapi import FastAPI, Depends, HTTPException
from models import get_session
from sqlalchemy.ext.asyncio import AsyncSession
import schemas
from models import Product, Seller
from sqlalchemy import select
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory="../static/templates")

@app.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    

@app.post("/create-seller", response_model=schemas.SellerCreate)
async def create_seller(seller: schemas.SellerCreate, session: AsyncSession = Depends(get_session)):
    stmt = select(Seller).where(Seller.sellername == seller.sellername)
    double_seller = await session.execute(stmt)
    if double_seller.first():
        raise HTTPException(status_code=400, detail="Seller is already in db")
    
    seller_add = Seller(sellername=seller.sellername)
    session.add(seller_add)
    await session.commit()
    await session.refresh(seller_add)

    for product in seller.products:
        product_add = Product(name=product.name, desc=product.desc, price=product.price, is_actual=product.is_actual, seller_id=seller_add.id)
        session.add(product_add)

    await session.commit()
    raise HTTPException(status_code=200, detail="Success!")


@app.get("/read-seller/{seller_name}", response_model=schemas.SellerRead)
async def read_seller(seller_name: str, session: AsyncSession = Depends(get_session)):
    stmt = select(Seller).where(Seller.sellername == seller_name)
    seller = await session.execute(stmt)

    seller = seller.first()
    if not seller:
        raise HTTPException(status_code=404, detail={"status": "not found"})
    return schemas.SellerRead(sellername=seller_name)
    

@app.get("/read-product/{product_name}", response_model=list[schemas.ProductBase])
async def read_product(product_name: str, session: AsyncSession = Depends(get_session)):
    stmt = select(Product).where(Product.name == product_name)
    products = await session.execute(stmt)
    lst = []
    for product in products.scalars().all():
        lst.append(schemas.ProductBase(name=product_name, desc=product.desc, 
                                        price=product.price, is_actual=product.is_actual))
    if len(lst) == 0:
        raise HTTPException(status_code=404, detail={"status": "not found"})
    return lst

@app.get("/read-seller-products/{seller_name}", response_model=schemas.SellerProducts)
async def read_seller_products(seller_name: str, session: AsyncSession = Depends(get_session)):
    stmt1 = select(Seller.id).where(Seller.sellername == seller_name)
    seller_id = await session.execute(stmt1)

    seller_id = seller_id.first()[0]
    if not seller_id:
        raise HTTPException(status_code=404, detail={"status": "not found"})
    
    stmt2 = select(Product).where(Product.seller_id == seller_id)
    products = await session.execute(stmt2)
    products = products.scalars().all()

    lst = []
    for prod in products:
        lst.append(schemas.ProductBase(name=prod.name, desc=prod.desc, price=prod.price, is_actual=prod.is_actual))

    products: List[dict] = lst

    return schemas.SellerProducts(sellername=seller_name, products=products)
