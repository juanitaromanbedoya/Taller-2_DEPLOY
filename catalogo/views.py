from django.http import JsonResponse
import requests
def catalogo(request):
    url = "https://fakestoreapi.com/products"

    respuesta = requests.get(url)

    productos = respuesta.json()

    return JsonResponse(productos, safe=False)
