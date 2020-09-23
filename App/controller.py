
import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta. Esta responsabilidad
recae sobre el controlador.
"""


# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    return catalog


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadData(catalog, booksfile,cast):
    """
    Carga los datos de los archivos en el modelo
    """
    loadMovies(catalog, booksfile,cast)


def loadMovies(catalog, movies_file,cast):
    """
    Carga cada una de las lineas del archivo de libros.
    - Se agrega cada libro al catalogo de libros
    - Por cada libro se encuentran sus autores y por cada
      autor, se crea una lista con sus libros
    """
    dialect = csv.excel()
    dialect.delimiter = ";"
    movies_file = cf.data_dir + movies_file
    input_file = csv.DictReader(open(movies_file, encoding="utf-8-sig"), dialect=dialect)
    movies_file_cast = cf.data_dir + cast
    input_file_cast = csv.DictReader(open(movies_file_cast, encoding="utf-8-sig"), dialect=dialect)
    for movie,movie_cast in zip(input_file,input_file_cast):
        model.addMovie(catalog, movie,movie_cast)
def MoviesSize(catalog):
    """Numero de libros leido
    """
    return model.MoviesSize(catalog)
def get_productoras(catalog, productora):
    productora = model.getMoviebyproductoras(catalog, productora)
    return productora
def get_director(catalog, director):
    return model.getMoviebydirectores(catalog, director)
def get_pais(catalog, pais):
    return model.getMoviebydirectores(catalog, pais)
