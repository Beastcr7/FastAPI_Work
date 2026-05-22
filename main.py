from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine
import database_model 
from sqlalchemy.orm import Session

app = FastAPI()

#giving persmission
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)


database_model.Base.metadata.create_all(bind = engine)

@app.get("/")
def home():
    return {"message": "Server is working"}

products = [
    Product(id = 101 , name = "Laptop" , description = "Gamin Laptop", price = 999.99 , quantity = 10) ,
    Product(id = 102 , name = "Mobile" , description = "Gamin Mobile", price = 100.99 , quantity = 10) ,
    Product(id = 103 , name = "Ipad" , description = "top version", price = 299 , quantity = 10) ,
    Product(id = 104 , name = "LapTabtop" , description = "Gorilla glass v4", price = 800.99 , quantity = 10)
    ]


def init_db():
    db = session()
    
    count = db.query(database_model.Product).count
    
    if count==0:
    
     for product in products:
        db.add(database_model.Product(**product.model_dump()))
        
     db.commit()
        
init_db()


def get_db():
    db = session()
    try:
        yield db
        
    finally:
        db.close()
        
    


@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    db_products = db.query (database_model.Product).all()
    return db_products

    
@app.get("/product/{id}")
def get_product_by_id (id:int, db:Session = Depends(get_db)):
    db_products = db.query (database_model.Product).filter(database_model.Product.id == id).first()
    if db_products:
            return db_products
        
    return "Product not found"


@app.post("/products")
def add_product(product:Product, db:Session = Depends(get_db)):
   db.add(database_model.Product(**product.model_dump())) 
   db.commit()
   return product

    
@app.put("/products/{id}")
def update_product(id:int, product:Product , db:Session = Depends(get_db)):
   db_products = db.query (database_model.Product).filter(database_model.Product.id == id).first()
   if db_products:
       db_products.name = product.name
       db_products.description = product.description
       db_products.price = product.price
       db_products.quantity = product.quantity
       db.commit()
       return "Product added sucessfully"
   else:
    return "No Product Found"
            
            
@app.delete("/products/{id}")
def _delete_product(id:int, db:Session = Depends(get_db)):
   db_products = db.query (database_model.Product).filter(database_model.Product.id == id).first()
   if db_products:
    db.delete(db_products)
    db.commit()
    return "Product Deleted Sucessfully"
   else:
     return "Product not found"