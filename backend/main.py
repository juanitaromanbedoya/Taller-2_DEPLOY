from fastapi import FastAPI, HTTPException
from backend.models.producto import Producto
from backend.models.pedido import Pedido
from database import productos_collection, pedidos_collection
from bson import ObjectId

app = FastAPI(
    title="API de Productos y Pedidos",
    description="API REST para gestionar productos y pedidos",
    version="1.0.0"
)


@app.get("/")
async def inicio():
    return {
        "mensaje": "API funcionando correctamente"
    }

@app.post("/productos", tags=["Crud Para Productos"])
async def crear_producto(producto: Producto):
    producto_dict = producto.model_dump()

    resultado = await productos_collection.insert_one(producto_dict)

    return {
        "mensaje": "Producto creado correctamente",
        "id": str(resultado.inserted_id)
    }

@app.get("/productos", tags=["Crud Para Productos"])
async def Mostrar_producto ():
     productos=[]

     mostrar=productos_collection.find()

     async for producto in mostrar:
        producto ["id"] = str(producto["_id"])
        del producto["_id"]
        productos.append(producto)

     return productos

@app.get("/productos/{producto_id}", tags=["Crud Para Productos"])
async def Mostrar_producto(producto_id: str):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="El ID del producto no es válido"
        )

    producto = await productos_collection.find_one(
        {"_id": ObjectId(producto_id)}
    )

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto["id"] = str(producto["_id"])
    del producto["_id"]

    return producto

@app.put("/productos/{producto_id}", tags=["Crud Para Productos"])
async def actualizar_producto(producto_id: str, producto: Producto):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="El ID del producto no es válido"
        )

    producto_dict = producto.model_dump()

    resultado = await productos_collection.update_one(
        {"_id": ObjectId(producto_id)},
        {"$set": producto_dict}
    )

    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto actualizado correctamente",
        "id": producto_id
    }


@app.delete("/productos/{producto_id}", tags=["Crud Para Productos"])
async def eliminar_producto(producto_id: str):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="El ID del producto no es válido"
        )

    resultado = await productos_collection.delete_one(
        {"_id": ObjectId(producto_id)}
    )

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto eliminado correctamente",
        "id": producto_id
    }

@app.post("/pedidos")
async def crear_pedido(pedido: Pedido):

    pedido_dict = pedido.model_dump()

    resultado = await pedidos_collection.insert_one(pedido_dict)

    return {
        "mensaje": "Pedido creado correctamente",
        "id": str(resultado.inserted_id)
    }