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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import listiterator as it

assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

"""


# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------
def newCatalog():
    """ Inicializa el catálogo de libros

    Crea una lista vacia para guardar todos los libros

    Se crean indices (Maps) por los siguientes criterios:
    Autores
    ID libros
    Tags
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    catalog = dict()

    catalog['movies'] = lt.newList('SINGLE_LINKED', compareMoviesIds) 
    catalog['moviesIds'] = mp.newMap(300,
                                     maptype='PROBING',
                                     loadfactor=0.4,
                                     comparefunction=compareMapMoviesIds)
    catalog['productoras'] = mp.newMap(500,
                                 maptype='CHAINING',
                                 loadfactor=0.7,
                                 comparefunction=compareMapProductora)
    return catalog


# Funciones para agregar informacion al catalogo
def addMovie(catalog, movie):
    """
    Esta funcion adiciona un libro a la lista de libros,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Finalmente crea una entrada en el Map de años, para indicar que este
    libro fue publicaco en ese año.
    """
    
    lt.addLast(catalog['movies'], movie)
    mp.put(catalog['moviesIds'], int(movie['id']), movie)
    addMovieproductora(catalog, movie)

def compareMapProductora(name, product):
    proentry = me.getKey(product)
    if (name == proentry):
        return 0
    elif (name > proentry):
        return 1
    else:
        return -1


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
    lt.addLast(pro['movies'], movie)
def newproductora(pubyear):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'productora': "", "movies": None}
    entry['productora'] = pubyear
    entry['movies'] = lt.newList('SINGLE_LINKED', compareMapProductora)
    return entry

"""def rq1(cont,estudio,key):
    s = cont["movies"]
    w=lt.newList('ARRAY_LIST')
    contador_depel= 0                    #solucion mediante listas
    promediode_pel=0
    final=lt.newList('ARRAY_LIST')
    iterator = it.newIterator(s)
    while it.hasNext(iterator):
        element = it.next(iterator)
        if element[key].lower()==estudio: 
            promediode_pel+=float(element["vote_average"])
            lt.addLast(w, element)
            contador_depel+=1
    promediode_pel = round(promediode_pel/contador_depel,2)
    lt.addLast(final, w)
    lt.addLast(final, contador_depel)
    lt.addLast(final, promediode_pel)
    return final"""

# ==============================
# Funciones de consulta
# ==============================


# ==============================
# Funciones de Comparacion
# ==============================

def compareMoviesIds(id1, id2):
    """
    Compara dos ids de libros
    """
    id1 = int(id1)
    id2 = int(id2)
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


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
    







