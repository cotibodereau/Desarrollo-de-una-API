# test.py

import pytest
from main import app

@pytest.fixture
def client():
    app.testing = True  # activa el modo de testing de Flask
    with app.test_client() as client:
        yield client

def test_obtener_peliculas(client):
    response = client.get('/peliculas')
    assert response.status_code == 200
    data = response.get_json()
    # Dependiendo del estado inicial de 'peliculas', ajustar la cantidad de elementos esperados
    assert isinstance(data, list)
    # Ejemplo: verificar que haya al menos 12 películas
    assert len(data) >= 12

def test_agregar_pelicula(client):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = client.post('/peliculas', json=nueva_pelicula)
    assert response.status_code == 201
    data = response.get_json()
    assert data['titulo'] == 'Pelicula de prueba'
    # Puedes agregar más aserciones según la lógica de 'obtener_nuevo_id'

def test_obtener_detalle_pelicula(client):
    response = client.get('/peliculas/1')
    # Esto dependerá de que la función 'obtener_pelicula' esté implementada correctamente
    # Aquí se espera un 200 y los detalles de la película con id 1
    assert response.status_code == 200
    data = response.get_json()
    assert data['titulo'] == 'Indiana Jones'

def test_actualizar_detalle_pelicula(client):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = client.put('/peliculas/1', json=datos_actualizados)
    # Verifica el status code y los cambios realizados
    assert response.status_code == 200
    data = response.get_json()
    assert data['titulo'] == 'Nuevo título'

def test_eliminar_pelicula(client):
    response = client.delete('/peliculas/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'mensaje' in data
    response = client.get('/peliculas/1')
    assert response.status_code == 404

def test_buscar_por_titulo(client):
    response = client.get('/peliculas/buscar?titulo=in')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Verifica que la búsqueda devuelva al menos una película
    assert len(data) > 0

def test_sugerir_por_genero(client):
    response = client.get('/peliculas/sugerir/Drama')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert 'Drama' in data['genero']

def test_sugerir_aleatoria(client):
    response = client.get('/peliculas/sugerir/Drama')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'titulo' in data
    assert 'genero' in data
    assert 'Drama' in data['genero']
    # Verifica que la película sugerida sea del género correcto

def test_sugerir_aleatoria_genero(client):
    response = client.get('/peliculas/sugerir/Drama')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'titulo' in data
    assert 'genero' in data
    assert 'Drama' in data['genero']
    # Verifica que la película sugerida sea del género correcto


def test_recomendar_feriado_genero(client):
    response = client.get('/recomendar/Drama')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    # Verifica que la recomendación devuelva al menos una película
    assert len(data) > 0