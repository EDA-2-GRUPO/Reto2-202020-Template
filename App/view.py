"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

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
    print("0- Salir")


# def Printn_Movie(catalog, n):
#     s = lt.getElement(catalog["movies"], n)
#     print("id de Pelicula:  " + str(s["id"]))
#     print("original_title:  " + str(s["original_title"]))
#     print("release_date: " + str(s["release_date"]))
#     print("vote_average: " + str(s["vote_average"]))
#     print("vote_count: " + str(s["vote_count"]))
#     print("spoken_languages: " + str(s["spoken_languages"]))


def printMoviesbyproductora(movies):
    """
    Imprime los libros de un autor determinado
    """
    if movies:
        print('productora encontrada: ' + movies['productora'])
        iterator = it.newIterator(movies['movies'])
        s = 0
        w = 0
        while it.hasNext(iterator):
            movie = it.next(iterator)
            """print(movie)
            print("----------------------------")
            print("\n\n\n\n\n\n")"""
            w += 1
            s += float(movie["vote_average"])
            print(movie["original_title"])
        print(w)
        print(round(s / w, 2))
        print("Numero de peliculas" + str(w))
        print("vote_average" + str(round(s / w, 2)))
    else:
        print('No se encontro el autor')


# ___________________________________________________
#  Menu principal
# ___________________________________________________

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    count = dict()

    if int(inputs[0]) == 1:
        C1 = input("desea usar el ADT map PROBE: 0, CHAINING: 1 :")
        map_type = "CHAINING" if int(C1) else "PROBE"
        C2 = input("Loadfactor por defecto: 1, Otro: 2")
        if C2 == "2":
            print("recuerde que para map PROBE el loadfactor no debe superar")
            C3 = input("Ingrese en valor de loadfactor")
            loadfactor = float(C3)

        else:
            loadfactor = None

        t1 = perf_counter()
        print("Inicializando Catálogo ....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.initCatalog(map_type, loadfactor)
        t2 = perf_counter()
        print(t2-t1)

    elif int(inputs[0]) == 2:

        C1 = input("Datos de prueba: 1, completos: 2")

        if C1 == "2":
            movies_file1 = "GoodMovies/AllMoviesDetailsCleaned.csv"
            movies_file2 = "GoodMovies/AllMoviesCastingRaw.csv"
        else:
            movies_file1 = "GoodMovies/SmallMoviesDetailsCleaned.csv"
            movies_file2 = "GoodMovies/MoviesCastingRaw-small.csv"
        t1 = perf_counter()

        print("Cargando información de los archivos ....")
        controller.loadData(cont, movies_file1, movies_file2)

        print("Numero de Peliculas cargadas")


        t2 = perf_counter()
        print("tiempo de carga:", t2-t1)
    elif int(inputs[0]) == 3:
        print("Cargando...")
        estudio = input("estudio que desea ver\n")
        movies = controller.get_productoras(cont, estudio)
        printMoviesbyproductora(movies)
    elif int(inputs[0]) == 4:
        s = cont["productoras"]
        print(mp.get(s, "Lucasfilm"))

        """keyskeys= keys.keys()
        print(keyskeys)"""

    else:
        break
