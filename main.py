from flask import Flask, jsonify, request
import random
from proximo_feriado import NextHoliday


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
    """
    Obtiene todas las peliculas

    Parameters:
    None

    Returns:
    Response: Un objeto JSON con todas las peliculas encontradas.
    """

    return jsonify(peliculas)


def obtener_pelicula(id):
    """
    Obtiene una pelicula segun su numero de id.

    Parameters:
    id (int): El ID de la película a obtener.

    Returns:
    Response: Un objeto JSON con la informacion detallada de la 
    pelicula obtenida.
    En caso de no encontrarla, devuelve un error con código 400.
    """

    for pelicula in peliculas:
        if pelicula ['id']==id:
            return jsonify(pelicula)
    return jsonify({"mensaje" : "Pelicula no encontrada"}), 404 #Not Found


def agregar_pelicula():
    """
    Agrega una nueva película a la lista.

    Parameters:
    JSON Body:
        - titulo (str): El título de la película.
        - genero (str): El género de la película.

    Returns:
    Response: Un objeto JSON con los detalles de la nueva película y un 
    código de estado 201 si se agregó correctamente.
    """

    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    """
    Actualiza los detalles de una película existente según su ID.

    Parameters:
    id (int): El ID de la película a actualizar.
    JSON Body (Opcional):
        - titulo (str): Nuevo título de la película. 
        Si no se proporciona, mantenemos el actual.
        - genero (str): Nuevo género de la película. 
        Si no se proporciona, mantenemos el actual.

    Returns:
    Response: Un objeto JSON con los detalles actualizados de la película.
              Si la película no se encuentra, devuelve un error con código 404.
    """

    for pelicula in peliculas:
        if pelicula['id']==id:
            pelicula['titulo'] = request.json.get('titulo', pelicula['titulo'])
            pelicula['genero'] = request.json.get('genero', pelicula['genero'])
            return jsonify(pelicula)
    return jsonify({"mensaje" : "Pelicula no encontrada"}), 404


def eliminar_pelicula(id):
    """
    Elimina una película de la lista según su ID.

    Parameters:
    id (int): El ID de la película a eliminar.

    Returns:
    Response: Un objeto JSON con un mensaje de éxito si la película fue eliminada,
              o un mensaje de error si no se encontró el ID.
    """

    # Busco la película por su ID
    for pelicula in peliculas: # Recorremos la lista
        if pelicula['id'] == id:
            peliculas.remove(pelicula)  # Eliminar la película de la lista
            return jsonify({"mensaje": "Película eliminada"}), 200  # Exito
        
    # Si no encontro una pelicula por id, devolvemos error
    return jsonify({'Error': 'Película no encontrada'}), 404    
    
def obtener_nuevo_id():
    """
    Genera un nuevo ID para una película.

    Parameters:
    None

    Returns:
    int: Un nuevo ID basado en el último ID de la lista de películas. 
         Si la lista está vacía, devuelve 1.
    """

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

@app.route('/peliculas/buscar', methods=['GET'])
def buscar_por_titulo():
    """
    Busca películas que en su titulo contengan el string pasado por URL.

    Query Parameters:
    titulo (str): Término de búsqueda a comparar con los títulos de las películas.

    Returns:
    Response: Un objeto JSON con una lista de películas que coinciden con la búsqueda.
              Si no hay coincidencias, devuelve una lista vacía.
    """
    
    termino_busqueda = request.args.get('titulo', '').lower()
    resultado = [p for p in peliculas if termino_busqueda in p['titulo'].lower()]
    return jsonify(resultado)

@app.route('/peliculas/sugerir/<string:genero>', methods=['GET'])
def sugerir_pelicula_aleatoria_genero(genero):
    """
    Sugiere una película aleatoria de un género específico.

    Parameters:
    genero (str): El género de la película a filtrar.

    Returns:
    Response: Un objeto JSON con los detalles de una película aleatoria del género solicitado.
              Si no hay películas del género, devuelve un mensaje de error con código 404.
    """

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

@app.route('/peliculas/genero/<string:genero>', methods=['GET'])
def filtrar_por_genero(genero):
    """
    Filtra y devuelve todas las películas de un género específico.

    Parameters:
    genero (str): El género de las películas a buscar.

    Returns:
    Response: Un objeto JSON con una lista de películas que pertenecen al género solicitado.
              Si no hay coincidencias, devuelve un mensaje de error con código 404.
    """

    resultado = [p for p in peliculas if p['genero'].lower() == genero.lower()]
    if not resultado:
        return make_response(jsonify({'error': f"Género '{genero}' no encontrado"}), 404)
    return jsonify(resultado)

@app.route('/peliculas/sugerir', methods=['GET'])
def sugerir_aleatoria():
    """
    Sugiere una película aleatoria de la lista de películas disponibles.

    Returns:
    Response: Un objeto JSON con los detalles de una película aleatoria.
              Si no hay películas disponibles, devuelve un mensaje de error con código 404.
              En caso de error interno, devuelve un mensaje con código 500.
    """

    if not peliculas:
        return jsonify({'error': 'No hay películas disponibles'}), 404
    try:
        pelicula_sugerida = random.choice(peliculas)
        return jsonify(pelicula_sugerida), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Error interno al sugerir película', 
            'detalle': str(e)
        }), 500

@app.route('/recomendar/<string:genero>', methods=['GET'])
def recomendar_feriado(genero):
    """
    Recomienda una película basada en un género específico y el próximo feriado.

    Parameters:
    genero (str): El género de la película a recomendar.

    Query Parameters:
    tipo (str, opcional): Tipo de feriado a considerar en la recomendación.

    Returns:
    Response: Un objeto JSON con información sobre el feriado próximo y 
              la película recomendada.
              Si no se encuentran feriados o películas del género solicitado, 
              devuelve un mensaje de error con código 404.
              En caso de error interno, devuelve un mensaje con código 500.
    """

    try:
        tipo_feriado = request.args.get('tipo', None)  # Obtener tipo desde query params
        next_holiday = NextHoliday()
        next_holiday.fetch_holidays(tipo=tipo_feriado)  # Pasar el tipo
        
        if not next_holiday.holiday:
            return jsonify({'error': 'No se encontraron feriados'}), 404
        
        opciones = [p for p in peliculas if p['genero'].lower() == genero.lower()]
        if not opciones:
            return jsonify({'error': 'No hay películas de este género'}), 404
        
        pelicula = random.choice(opciones)
        return jsonify({
            'feriado': next_holiday.holiday['motivo'],
            'fecha': f"{next_holiday.holiday['dia']}/{next_holiday.holiday['mes']}",
            'tipo': next_holiday.holiday['tipo'],  # Incluir tipo en respuesta
            'pelicula': pelicula
        }), 200
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500
    

if __name__ == '__main__':
    app.run()
