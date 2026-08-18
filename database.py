import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

#Inicializa el cliente de MongoDB
client = AsyncIOMotorClient(MONGODB_URL)

#Selecciona la base de datos (se crea auto si no existe )
database = client.base_fasApi

#Seleccionar la colección (se crea auto si no existe)

productos_collection = database.productos
pedidos_collection = database.pedidos

#Función para probar la conexión a la base de datos
async def test_connection():
    try:
        #1. Verficar la conexión al servidor de MongoDB
        await client.admin.command('ping')
        print("Conexión a MongoDB exitosa")

        # 2. Crear un documento de prueba
        doctest = {
            "nombre" : "Juanita Roman ",
            "edad" : "17",
            "genero" : "Femenino",
        }

        # 3. Guarda el documento de prueba en la colección
        print("Guardando documento de prueba en la colección...")
        result = await productos_collection.insert_one(doctest)
        print(f"Documento guardado con ID: {result.inserted_id}")

        # 4. Buscar el dato guardado en la colección
        datarequest = await productos_collection.find_one({"_id": result.inserted_id})
        print(f"Documento encontrado: {datarequest}")
        

    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")

if __name__ == "__main__":
    # Ejecutar la función de prueba de conexión
    asyncio.run(test_connection())

