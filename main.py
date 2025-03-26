from flask import Flask, jsonify, request

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]


def obtener_peliculas():
    return jsonify(peliculas)


def obtener_pelicula(id):
    for pelicula in peliculas:
        if pelicula ['id']==id:
            return jsonify(pelicula )
    return jsonify({"mensaje" : "Pelicula no encontrada"}), 404 #Not Found


def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    for pelicula in peliculas:
        if pelicula['id']==id:
            pelicula['titulo'] = request.json.get('titulo', pelicula['titulo'])
            pelicula['genero'] = request.json.get('genero', pelicula['genero'])
            return jsonify(pelicula)
    return jsonify({"mensaje" : "Pelicula no encontrada"}), 404


def eliminar_pelicula(id):
    # Lógica para buscar la película por su ID y eliminarla

    # Busco la película por su ID
    for pelicula in peliculas: # Recorremos la lista
        if pelicula['id'] == id:
            peliculas.remove(pelicula)  # Eliminar la película de la lista
            return jsonify({"mensaje": "Película eliminada"}), 200  # Exito
        
    # Si no encontro una pelicula por id, devolvemos error
    return jsonify({'Error': 'Película no encontrada'}), 404


@app.route('/peliculas/buscar', methods=['GET'])
def buscar_por_titulo():
    termino_busqueda = request.args.get('titulo', '').lower()
    resultado = [p for p in peliculas if termino_busqueda in p['titulo'].lower()]
    return jsonify(resultado)
    
    
def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])

@app.route('/peliculas/sugerir/<string:genero>', methods=['GET'])
def sugerir_pelicula_aleatoria_genero(genero):
    #Sugerimos pelicula aleatorio segun el genero

    # Filtrar películas por género (ignorando mayúsculas/minúsculas)
    peliculas_filtradas = [
        pelicula for pelicula in peliculas 
        if pelicula['genero'].lower() == genero.lower()
    ]
    if not peliculas_filtradas:
        return jsonify({"error": "No se encontraron películas para ese género"}), 404
    
    # Seleccionar una película aleatoria del listado filtrado
    pelicula_seleccionada = random.choice(peliculas_filtradas)

    return jsonify(pelicula_seleccionada), 200 # Exito

if __name__ == '__main__':
    app.run()
