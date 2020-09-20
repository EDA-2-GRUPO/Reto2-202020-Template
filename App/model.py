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

    catalog['ids'] = mp.newMap(300, maptype='PROBING',
                               loadfactor= 0.4,
                               comparefunction=compareMapMoviesIds)

    catalog['productoras'] = mp.newMap(100,
                                       maptype=map_type,
                                       loadfactor=0.7,
                                       comparefunction=compareMapProductora)

    catalog['Actors'] = mp.newMap(400,
                                  maptype=map_type,
                                  loadfactor=0.7,
                                  comparefunction=compareMapProductora)

    return catalog


# Funciones para agregar informacion al catalogo
def add_ids(catalog, movie, pase = True):
    """
    Esta funcion adiciona un libro a la lista de libros,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Finalmente crea una entrada en el Map de años, para indicar que este
    libro fue publicaco en ese año.
    """

    ids = catalog['ids']
    id = int(movie["id"])
    if pase:
        mp.put(ids, id, movie)
        if ids['size'] / ids['capacity'] > ids['loadfactor']:
            print(ids['size'])
            catalog['ids'] = mp.rehash(ids)
    else:
        existpro = mp.contains(ids, id)
        if existpro:
            entry = mp.get(ids, id)
            (me.getValue(entry)).update(movie)
        else:
            mp.put(ids, id, movie)
            if ids['size'] / ids['capacity'] > ids['loadfactor']:
                print(ids['size'])
                catalog['ids'] = mp.rehash(ids)


def addMovieproductora(catalog, movie):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """

    productora = catalog['productoras']
    producmo = movie["production_companies"]
    existpro = mp.contains(productora, producmo)

    if existpro:
        entry = mp.get(productora, producmo)
        pro = me.getValue(entry)
    else:
        pro = newproductora(producmo)
        mp.put(productora, producmo, pro)
        if productora['size'] / productora['capacity'] > productora['loadfactor']:
            catalog['productoras'] = mp.rehash(productora)

    lt.addLast(pro['movies'], movie)


def addActor(catalog, movie):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """

    C_Actors = catalog['Actors']
    keys = ["actor1_name", "actor2_name", "actor3_name", "actor4_name", "actor5_name"]
    actors = [movie[key] for key in keys]

    for actor in actors:

        existpro = mp.contains(C_Actors, actor)

        if existpro:
            entry = mp.get(C_Actors, actor)
            act = me.getValue(entry)
        else:
            act = newActor(actor)
            mp.put(C_Actors, actor, act)
            if C_Actors['size'] / C_Actors['capacity'] > C_Actors['loadfactor']:
                catalog['Actors'] = mp.rehash(C_Actors)

        lt.addLast(act["movies"], movie)


def newActor(actor):
    entry = {'actor': "", "movies": None}
    entry['actor'] = actor
    entry['movies'] = lt.newList('SINGLE_LINKED', compareMapProductora)
    return entry


def newproductora(pr_name):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'actor': "", "movies": None}
    entry['productora'] = pr_name
    entry['movies'] = lt.newList('SINGLE_LINKED', compareMovieName)
    return entry


# ==============================
# Funciones de consulta
# ==============================

def MoviesSize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog['movies'])


def getMoviebyproductoras(catalog, productora):
    """
    Retorna los peliculas publicadas por una productora
    """
    pro = mp.get(catalog["productoras"], productora)
    if pro:
        return me.getValue(pro)
    return None


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
    if (id1 == id2):
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
    if (name == proentry):
        return 0
    elif (name > proentry):
        return 1
    else:
        return -1
