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
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapstructure as mp
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me

assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

"""


# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------

def newCatalog(map_type="CHAINING", loadfactor=None):
    """ Inicializa el catálogo de libros

    Crea una lista vacia para guardar todos los libros

    Se crean indices (Maps) por los siguientes criterios:
    Autores
    ID libros
    Tags
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    if loadfactor is None:
        if map_type == "PROBING":
            loadfactor = 0.4
        elif map_type == "CHAINING":
            loadfactor = 0.9
        else:
            return None

    catalog = dict()

    catalog['producers'] = mp.newMap(100,
                                     maptype=map_type,
                                     loadfactor=loadfactor,
                                     comparefunction=compareMapProductora)

    catalog['actors'] = mp.newMap(400,
                                  maptype=map_type,
                                  loadfactor=loadfactor,
                                  comparefunction=compareMapProductora)

    catalog['genres'] = mp.newMap(400,
                                  maptype=map_type,
                                  loadfactor=loadfactor,
                                  comparefunction=compareMapProductora)

    return catalog


# Funciones para agregar informacion al catalogo


def addMovieproductora(catalog, movie):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """

    productora = catalog['producers']
    producmo = movie["production_companies"]
    existpro = mp.contains(productora, producmo)

    if existpro:
        entry = mp.get(productora, producmo)
        pro = me.getValue(entry)
    else:
        pro = lt.newList('SINGLE_LINKED', compareMovieName)
        mp.put(productora, producmo, pro)
        if productora['size'] / productora['capacity'] > productora['loadfactor']:
            catalog['producers'] = mp.rehash(productora)

    lt.addLast(pro, movie)


def addActor(catalog, movie):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """

    c_actors = catalog['actors']
    keys = ["actor1_name", "actor2_name", "actor3_name", "actor4_name", "actor5_name"]
    actors = [movie[key] for key in keys]

    for actor in actors:
        existpro = mp.contains(c_actors, actor)
        if existpro:
            entry = mp.get(c_actors, actor)
            act = me.getValue(entry)
        else:
            act = lt.newList('SINGLE_LINKED', compareMovieName)
            mp.put(c_actors, actor, act)
            if c_actors['size'] / c_actors['capacity'] > c_actors['loadfactor']:
                catalog['actors'] = mp.rehash(c_actors)

        lt.addLast(act, movie)


def addGeneres(catalog, movie):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """

    c_generes = catalog['genres']
    str_generes = movie["genres"]
    genres = str_generes.split("|")

    for genre in genres:
        existpro = mp.contains(c_generes, genre)
        if existpro:
            entry = mp.get(c_generes, genre)
            gen = me.getValue(entry)
        else:
            gen = lt.newList('SINGLE_LINKED', compareMovieName)
            mp.put(c_generes, genre, gen)
            if c_generes['size'] / c_generes['capacity'] > c_generes['loadfactor']:
                catalog['genres'] = mp.rehash(c_generes)

        lt.addLast(gen, movie)


# ==============================
# Funciones de consulta
# ==============================


def getMoviesinTagbyName(catalog, tag, name):
    """
    Retorna los peliculas publicadas por una productora
    """

    pro = mp.get(catalog[tag], name)
    if pro:
        movies = me.getValue(pro)
        return {"name": me.getKey(pro), "movies": me.getValue(pro), "size": lt.size(movies)}
    return None


def prom_movies(entry, key):
    """
    entry: dict con llave con el name, y con la llave movies con las movies asociadas
    key: llave a la que sacaremos promedio de las movies
    Return: promedio
    """
    movies = entry["movies"]
    iterator = it.newIterator(movies)
    summation = 0
    n = lt.size(movies)
    for i in range(n):
        movie = it.next(iterator)
        try:
            summation += int(movie[key])
        except ValueError:
            pass

    if n > 0:
        return summation / n
    else:
        print("not movies")
        return 0


# ==============================
# Funciones de Comparacion
# ==============================


# ==============================
# LIST
# ==============================
def compareMoviesIds(id1, id2):
    """
    Compara dos ids de libros
    """
    if id1 == id2:
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareMovieName(name1, name2):
    if name1 == name2:
        return 0
    elif name1 > name2:
        return 1
    else:
        return -1

    # ==============================
    # MAP
    # ==============================


def compareMapMoviesIds(id, entry):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if int(id) == int(identry):
        return 0
    elif int(id) > int(identry):
        return 1
    else:
        return -1


def compareMapProductora(name, product):
    proentry = me.getKey(product)
    if name == proentry:
        return 0
    elif name > proentry:
        return 1
    else:
        return -1
