
import sys
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from App import controller
from DISClib.ADT import map as mp
from time import perf_counter
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones y por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

movies_file = "GoodMovies/AllMoviesCastingRaw.csv"
movies_file_cast="GoodMovies/AllMoviesDetailsCleaned.csv"


# ___________________________________________________
#  Funciones para imprimir la inforamación de
#  respuesta.  La vista solo interactua con
#  el controlador.
# ___________________________________________________

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Descubrir productoras de cine")
    print("4- Consultar los libros de un autor")
    print("5- Consultar los Libros por etiqueta")
    print("0- Salir")

def Printn_Movie(catalog, n): 
    s = lt.getElement(catalog["movies"], n)
    print("id de Pelicula:  "+str(s["id"]))
    print("original_title:  "+str(s["original_title"]))
    print("release_date: "+str(s["release_date"]))
    print("vote_average: "+str(s["vote_average"]))
    print("vote_count: "+ str(s["vote_count"]))
    print("spoken_languages: "+str(s["spoken_languages"]))
def printMoviesbyproductora(movies):
    """
    Imprime los libros de un autor determinado
    """
    if movies:
        print('productora encontrada: ' + movies['productora'])
        iterator = it.newIterator(movies['movies'])
        s = 0
        w=0
        while it.hasNext(iterator):
            movie = it.next(iterator)
            w+=1
            s+=float(movie["vote_average"])
            print(movie["original_title"])
        print(w)
        print(round(s/w,2))    
    else:
        print('No se encontro el autor')
def printMoviesbyalgo(movies,primer):
    """
    Imprime los libros de un autor determinado
    """
    if movies:
        print('productora encontrada: ' + movies[primer])
        iterator = it.newIterator(movies['movies'])
        s = 0
        w=0
        while it.hasNext(iterator):
            movie = it.next(iterator)
            w+=1
            s+=float(movie["vote_average"])
            print(movie["original_title"])
        print(w)
        print(round(s/w,2))    
    else:
        print('No se encontro el autor')
def printMoviesbydirector(movies):
    """
    Imprime los libros de un autor determinado
    """
    if movies:
        print('productora encontrada: ' + movies['director'])
        iterator = it.newIterator(movies['movies'])
        s = 0
        w=0
        while it.hasNext(iterator):
            movie = it.next(iterator)
            w+=1
            s+=float(movie["vote_average"])
            print(movie["original_title"])
        print(w)
        print(round(s/w,2))    
    else:
        print('No se encontro el autor')



# ___________________________________________________
#  Menu principal
# ___________________________________________________

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.initCatalog()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        t1_start = perf_counter()
        controller.loadData(cont, movies_file, movies_file_cast)
        t1_stop = perf_counter()
        print("Tiempo de ejecución ", t1_stop - t1_start, " segundos")
    elif int(inputs[0]) == 3: 
        print("Cargando...")
        estudio = input("estudio que desea ver\n")
        movies = controller.get_productoras(cont, estudio)
        printMoviesbyproductora(movies)
    elif int(inputs[0]) == 4:
        nombre = input("nombre del director")
        movies = controller.get_director(cont, nombre)
        printMoviesbydirector(movies)
    elif int(inputs[0]) == 8:
        pais = input("pais peliculas")
        movies = controller.get_pais(cont, pais)
        printMoviesbyalgo(movies,"pais")
        
    else:
        break
