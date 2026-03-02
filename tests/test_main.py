
from app.main import app
from fastapi.testclient import TestClient

# El TestClient permite simular peticiones HTTP sin levantar un servidor real
client = TestClient(app)

def test_read_health():
    """
    Prueba crítica: El Health Check debe devolver 200 para que 
    Azure Container Apps no reinicie el contenedor.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_item_success():
    """
    Prueba la creación exitosa verificando que Pydantic 
    serializa correctamente los datos.
    """
    payload = {
        "id": 1,
        "name": "Componente Frontend",
        "description": "Un plugin para React",
        "price": 25.5
    }
    response = client.post("/items/", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Componente Frontend"

def test_create_item_invalid_price():
    """
    Prueba de validación: El precio debe ser > 0 según nuestro esquema.
    """
    payload = {
        "id": 2,
        "name": "Item Gratis",
        "price": -10.0  # Esto debería disparar un error 422
    }
    response = client.post("/items/", json=payload)
    assert response.status_code == 422  # Unprocessable Entity