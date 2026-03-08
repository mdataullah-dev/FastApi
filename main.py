from mockData import products
from dtos import productDTO
# import fastapi

# print(fastapi.__version__)

#? this will give : 0.135.1



from fastapi import FastAPI, Request

app = FastAPI()




# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}
#?  if "/" then => http://127.0.0.1:8000 is pr hi chal jayega 
@app.get("/")    #* yahan pr "/home kr diya then => http://127.0.0.1:8000/home pr hi run karega "
def home():
    return "Welcome Md Ataullah"

# @app.get("/contact")
# def contact():
#     return "you can connect with me"
@app.get("/products")
def get_products():
    return products


#? path params:
@app.get("/product/{product_id}")
def getOneProduct( product_id:int ):
    
    ##? if product available with the id, return product , else return error message
    
    for oneProduct in products:
        if oneProduct.get("id") == product_id:
            return oneProduct
    return {
        "error": f"Product not Found for this id:{product_id}"
    }
    
    
##? query-params:
# http://127.0.0.1:8000/greet?name=nazish&age=2
# @app.get("/greet")
# def greetUser(name:str, age:int):
#     return{
#         "greet":f"Hi!! {name} How are u and age {age}"
#     }

@app.get("/greet")
def greetUser(req:Request):
    query_params = dict(req.query_params)
    #print(query_params)
    return{
        "greet":f"Hi!!{query_params.get("name")} How are u and age is {query_params.get("age")}"
    }
    
##? http methods :

#get : to Get something from server
#post : to sent something to the database from server 


#? different types of http methods 

@app.post("/create_product")
def createProduct(body:productDTO):
    #?print(body) => pydantic ki madad se forntend se postman se jo bheja humne data => vo is body mein recieve mein hua 
    product_data = body.model_dump()
    #print(product_data)#? pydantic => id=4 title='pen' name='Likho Pikho' price=5 count=7  using model_dump() converted into => {'id': 4, 'title': 'pen', 'name': 'Likho Pikho', 'price': 5, 'count': 7} dictionary
    products.append(product_data)
    return {"status":"Product Created Successfully...200", "data":products}



##? backend ko kaise pata chalega data ayega kaise :
#=> then we use pydantic => body mein jo data ayega usko kaise handle krna hai 

#? and how to validate the data 
##? jo v data frontend se backend mein aata hai => ya backend se frontend mein bheja jata hai =>
##? ya client <=> server communication mein us data mein validation v implement kr skte hain hum 
##! ye hota hai isko we call as=> DTOS => data transfer objects


#? update : put 
@app.put("/update_product/{product_id}")
def update_product(body:productDTO, product_id:int ):
    for index, oneProduct in enumerate(products):
        
        if oneProduct.get("id") == product_id:
            products[index] = body.model_dump()
            return {"status":200, "product": body}
        
    return {"status":404, "msg": "Product not found"}



#? delete 
@app.delete("/delete_product/{product_id}")
def delete_product(product_id:int):
    
    for index, oneProduct in enumerate(products):
        
        if oneProduct.get("id") == product_id:
            deleted_product = products.pop(index)
            return {"status":200, "product":deleted_product}
    
    return {"status":404}


#?





    
    




