from flask import Flask, request
from flask_smorest import abort
from db import items, stores
import uuid

app = Flask(__name__)

#To use the next config, add import Api in flask_smorest
"""
app.config["API_TITLE"] = "Mi API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
api = Api(app) 
"""


# OBTENER DATA DE TODAS LAS TIENDAS
@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


# CREAR UNA NUEVA TIENDA
@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(404, message="Bad request. Enusre 'name' is included in the JSON payload.")

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(404, message="Store already exits.")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


# CREAR UN NUEVO ITEM
@app.post("/item")
def create_item():
    item_data = request.get_json()

    if ("price" not in item_data or 
        "store_id" not in item_data or 
        "name" not in item_data):
        abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSOM payload.")

    for item in items.values():
        if(item_data["name"] == item["name"] and 
           item_data["store_id"] == item["store_id"]):
            abort(400, message="Item already exists.")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201
    

# OBTENER DATA DE UNA TIENDA EN ESPECIFICO
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")


# OBTENER INFORMACION DE UN ITEM EN ESPECIFICO
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")


# ELIMINAR UN ITEM EN ESPECIFICO
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found")


#ACTUALIZAR DATA DE UN ITEM
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()

    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")

    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message="Item not found.")

    

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}