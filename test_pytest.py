import requests
import pytest
import requests_mock

@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        # Simulamos la respuesta para obtener todas las películas
        m.get('http://localhost:5000/peliculas', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201, json={'id': 3, 'titulo': 'Pelicula de prueba', 'genero': 'Acción'})

        # Simulamos la respuesta para obtener detalles de una película específica
        m.get('http://localhost:5000/peliculas/1', json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200, json={'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'})

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200)

        # Simulamos la respuesta para buscar películas por título
        m.get('http://localhost:5000/peliculas/buscar?titulo=in', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
            {'id': 4, 'titulo': 'Lord of the Rings', 'genero': 'Fantasía'}
        ])

        # Simulamos la respuesta para obtener pelicula aleatorio por su genero
        m.get('http://localhost:5000/peliculas/sugerir/Drama', json=
            {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'
        })

        yield m

def test_obtener_peliculas(mock_response):
    response = requests.get('http://localhost:5000/peliculas')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_agregar_pelicula(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3

def test_obtener_detalle_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'

def test_actualizar_detalle_pelicula(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/1', json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'

def test_eliminar_pelicula(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    
def test_pelicula_aleatoria_genero(mock_response):
    # Hacer una solicitud GET al servidor para obtener la película según el género
    response = requests.get('http://localhost:5000/peliculas/sugerir/Drama')
    assert response.status_code == 200

    # Verificamos si encontro coincidencia 
    assert response.json()['genero'] == 'Drama'

def test_buscar_por_titulo(mock_response):
    termino_busqueda = 'in'
    response = requests.get(f'http://localhost:5000/peliculas/buscar?titulo={termino_busqueda}')
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_filtrar_por_genero(mock_response):
    # Mock de respuesta con datos reales
    mock_response.get(
        'http://localhost:5000/peliculas/genero/Acción',
        json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ]
    )
    
    response = requests.get('http://localhost:5000/peliculas/genero/Acción')
    assert response.status_code == 200
    assert len(response.json()) == 2  # Verificar que hay 2 películas de Acción


def test_recomendar_feriado(mock_response):

    mock_response.get(
        'http://localhost:5000/recomendar/Acción',
        json={
            'feriado': 'Día de la Independencia',
            'fecha': '9/7',
            'tipo': 'Feriado Nacional',
            'pelicula': {
                'id': 1, 
                'titulo': 'Indiana Jones', 
                'genero': 'Acción'
            }
        }
    )

    response = requests.get('http://localhost:5000/recomendar/Acción')
    assert response.status_code == 200
    
    data = response.json()
    assert 'feriado' in data
    assert 'fecha' in data
    assert 'tipo' in data
    assert 'pelicula' in data
    assert data['pelicula']['genero'] == 'Acción'

def test_sugerir_pelicula_aleatoria(mock_response):

    mock_response.get(
        'http://localhost:5000/peliculas/sugerir',
        json={
            'id': 1, 
            'titulo': 'Indiana Jones', 
            'genero': 'Acción'
        }
    )
    
    response = requests.get('http://localhost:5000/peliculas/sugerir')
    
    assert response.status_code == 200
    
    pelicula = response.json()
    assert 'id' in pelicula
    assert 'titulo' in pelicula
    assert 'genero' in pelicula

    assert pelicula['titulo'] == 'Indiana Jones'
    assert pelicula['genero'] == 'Acción'