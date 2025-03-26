import requests

BASE_URL = 'http://localhost:5000'

def print_response(label, response):
    print(f"\n{label} ({response.status_code}):")
    try:
        print(response.json())
    except:
        print(response.text)

# Obtener todas las películas
response = requests.get(f'{BASE_URL}/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post(f'{BASE_URL}/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
# Utiliza el ultimo id de la lista de peliculas
id_pelicula = peliculas[-1]['id']
response = requests.get(f'{BASE_URL}/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
# Utiliza el ultimo id de la lista de peliculas
id_pelicula = peliculas[-1]['id']
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'{BASE_URL}/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Eliminar una película
# Utiliza el ultimo id de la lista de peliculas
id_pelicula = peliculas[-1]['id']
response = requests.delete(f'{BASE_URL}/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.")
else:
    print("Error al eliminar la película.")
print()

# Buscar pelicula por titulo
termino_busqueda = 'in'
response = requests.get(f'{BASE_URL}/peliculas/buscar?titulo={termino_busqueda}')
if response.status_code == 200:
    peliculas_encontradas = response.json()
    print("Peliculas encontradas:")
    for pelicula in peliculas_encontradas:
        print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al buscar la pelicula")    
print()

# Sugerir pelicula aleatoria por su genero
genero = 'Acción'
response = requests.get(f'{BASE_URL}/peliculas/sugerir/{genero}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Filtrar por género
response = requests.get(f'{BASE_URL}/peliculas/genero/Aventura')
print_response("Películas de Aventura", response)
print()

# Recomendación para feriado
response = requests.get(f'{BASE_URL}/recomendar/Acción?tipo=inmovable')
print_response("Recomendar para feriado", response)
print()

# Test para sugerir película aleatoria
response = requests.get(f'{BASE_URL}/peliculas/sugerir')
print_response("Sugerir película aleatoria", response)
print()