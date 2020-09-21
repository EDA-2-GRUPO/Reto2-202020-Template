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
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import liststructure as lt
from DISClib.DataStructures import listiterator as it
from App import controller
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
    print("w-Inicializar Catálogo")
    print("q-Cargar información en el catálogo")
    print("1- Descubrir productoras de cine")
    print("0- Salir")


def max_freq_directors(directores):
    freq_dato = {"director": None, "veces": 0}
    most = []
    freq_max = 0

    for dato, freq in directores.items():
        if freq > freq_max:
            freq_dato["director"] = [dato]
            freq_max = freq
        elif freq == freq_max:
            most.append(dato)

    freq_dato["veces"] = freq_max
    return freq_dato


def printMoviesbyIdk(movies,imprimir, prom, direct=False):
    """
    Imprime los libros de un autor determinado
    """

    if movies:
        print('productora encontrada: ' + movies["name"])
        movies = movies["movies"]
        iterator = it.newIterator(movies)
        s = 0
        directores = {}
        n = lt.size(movies)
        for i in range(n):
            movie = it.next(iterator)
            s += float(movie[prom])
            if direct:
                drt = movie['director']
                if directores.get(drt):
                    directores[drt] += 1
                else:
                    directores[drt] = 0

            print(movie["original_title"])

        print("Numero de peliculas: ", n)
        print("vote_average", round(s / n, 2))
        if direct:
            ml = max_freq_directors(directores)
            print("el director con mayor participacion: {} con {} participaciones".format(ml["director"], ml['veces']))

    else:
        print('No se encontro el autor')


# ___________________________________________________
#  Menu principal
# ___________________________________________________

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    count = dict()

    if inputs[0] == "w":
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
        print(t2 - t1)

    elif inputs[0] == "q":
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
        print("tiempo de carga:", t2 - t1)

    elif int(inputs[0]) == 1:
        estudio = input("estudio que desea ver\n")
        print("Cargando...")
        t1 = perf_counter()
        movies = controller.get_name(cont, "producers", estudio)
        printMoviesbyIdk(movies, "vote_average")
        t2 = perf_counter()
        print("tiempo req1:", t2 - t1)

    elif int(inputs[0]) == 2:
        t1 = perf_counter()
        print("Cargando...")
        pass
        t2 = perf_counter()
        print("tiempo req2:", t2 - t1)

    elif int(inputs[0]) == 3:
        print("Cargando...")
        t1 = perf_counter()
        actor = input("actor que quiere consultar\n")
        movies = controller.get_name(cont, "actors", actor)
        printMoviesbyIdk(movies, "vote_average")
        t2 = perf_counter()
        print("tiempo req3:", t2 - t1)

    elif int(inputs[0]) == 4:
        t1 = perf_counter()
        print("Cargando...")
        genero = input("genero que quiere consultar\n")
        movies = controller.get_name(cont, "genres", genero)
        printMoviesbyIdk(movies, "vote_average")
        t2 = perf_counter()
        print("tiempo req4:", t2 - t1)

    elif int(inputs[0]) == 5:
        t1 = perf_counter()
        print("Cargando...")
        pass
        t2 = perf_counter()
        print("tiempo req5:", t2 - t1)

    elif int(inputs[0]) == 0:
        break

    else:
        print("Opcion invalida")
        continue
