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
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

"""

# -----------------------------------------------------
# API del TAD Catalogo de Peliculas
# -----------------------------------------------------

def newCatalog():
    """ Inicializa el catálogo de Peliculas

    Crea una lista vacia para guardar todos los Peliculas

    Se crean indices (Maps) por los siguientes criterios:
    Autores
    ID Peliculas
    Tags
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    catalog = {'Movies': None,
               'MoviesIds': None,
               'authors': None,
               'tags': None,
               'tagIds': None,
               'years': None}

    catalog['Movies'] = lt.newList('SINGLE_LINKED', compareMovieIds)
    catalog['MoviesIds'] = mp.newMap(200,
                                   maptype='PROBING',
                                   loadfactor=0.4,
                                   comparefunction=compareMapMovieIds)
    catalog['authors'] = mp.newMap(200,
                                   maptype='PROBING',
                                   loadfactor=0.4,
                                   comparefunction=compareAuthorsByName)
    catalog['tags'] = mp.newMap(1000,
                                maptype='CHAINING',
                                loadfactor=0.7,
                                comparefunction=compareTagNames)
    catalog['tagIds'] = mp.newMap(1000,
                                  maptype='CHAINING',
                                  loadfactor=0.7,
                                  comparefunction=compareTagIds)
    catalog['years'] = mp.newMap(500,
                                 maptype='CHAINING',
                                 loadfactor=0.7,
                                 comparefunction=compareMapYear)

    return catalog
def newAuthor(name):
    """
    Crea una nueva estructura para modelar los Peliculas de un autor
    y su promedio de ratings
    """
    author = {'name': "", "Movies": None,  "average_rating": 0}
    author['name'] = name
    author['Movies'] = lt.newList('SINGLE_LINKED', compareAuthorsByName)
    return author


def newTagMovie(name, id):
    """
    Esta estructura crea una relación entre un tag y los Peliculas que han sido
    marcados con dicho tag.  Se guarga el total de Peliculas y una lista con
    dichos Peliculas.
    """
    tag = {'name': '',
           'tag_id': '',
           'total_Movies': 0,
           'Movies': None,
           'count': 0.0}
    tag['name'] = name
    tag['tag_id'] = id
    tag['Movies'] = lt.newList()
    return tag

# Funciones para agregar informacion al catalogo

def addMovie(catalog, Movie):
    """
    Esta funcion adiciona un Pelicula a la lista de Peliculas,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Finalmente crea una entrada en el Map de años, para indicar que este
    Pelicula fue publicaco en ese año.
    """
    lt.addLast(catalog['Movies'], Movie)
    mp.put(catalog['MoviesIds'], Movie['id'], Movie)
    addMovieYear(catalog, Movie)


def addMovieYear(catalog, Movie):
    """
    Esta funcion adiciona un Pelicula a la lista de Peliculas que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de Peliculas de ese año.
    """
    years = catalog['years']
    pubyear = Movie['original_publication_year']
    pubyear = int(float(pubyear))
    existyear = mp.contains(years, pubyear)
    if existyear:
        entry = mp.get(years, pubyear)
        year = me.getValue(entry)
    else:
        year = newYear(pubyear)
        mp.put(years, pubyear, year)
    lt.addLast(year['Movies'], Movie)


def newYear(pubyear):
    """
    Esta funcion crea la estructura de Peliculas asociados
    a un año.
    """
    entry = {'year': "", "Movies": None}
    entry['year'] = pubyear
    entry['Movies'] = lt.newList('SINGLE_LINKED', compareYears)
    return entry


def addMovieAuthor(catalog, authorname, Movie):
    """
    Esta función adiciona un Pelicula a la lista de Peliculas publicados
    por un autor.
    Cuando se adiciona el Pelicula se actualiza el promedio de dicho autor
    """
    authors = catalog['director_name']
    existauthor = mp.contains(authors, authorname)
    if existauthor:
        entry = mp.get(authors, authorname)
        author = me.getValue(entry)
    else:
        author = newAuthor(authorname)
        mp.put(authors, authorname, author)
    lt.addLast(author['Movies'], Movie)

    authavg = author['average_rating']
    Movieavg = Movie['average_rating']
    if (authavg == 0.0):
        author['average_rating'] = float(Movieavg)
    else:
        author['average_rating'] = (authavg + float(Movieavg)) / 2


def addTag(catalog, tag):
    """
    Adiciona un tag a la tabla de tags dentro del catalogo
    """
    newtag = newTagMovie(tag['tag_name'], tag['tag_id'])
    mp.put(catalog['tags'], tag['tag_name'], newtag)
    mp.put(catalog['tagIds'], tag['tag_id'], newtag)


def addMovieTag(catalog, tag):
    """
    Agrega una relación entre un Pelicula y un tag.
    Para ello se adiciona el Pelicula a la lista de Peliculas
    del tag.
    """
    Movieid = tag['goodreads_Movie_id']
    tagid = tag['tag_id']
    entry = mp.get(catalog['tagIds'], tagid)

    if entry:
        tagMovie = mp.get(catalog['tags'], me.getValue(entry)['name'])
        tagMovie['value']['total_Movies'] += 1
        tagMovie['value']['count'] += int(tag['count'])
        Movie = mp.get(catalog['MovieIds'], Movieid)
        if Movie:
            lt.addLast(tagMovie['value']['Movies'], Movie['value'])

# ==============================
# Funciones de consulta
# ==============================

def getMoviesByAuthor(catalog, authorname):
    """
    Retorna un autor con sus Peliculas a partir del nombre del autor
    """
    author = mp.get(catalog['authors'], authorname)
    if author:
        return me.getValue(author)
    return None


def getMoviesByTag(catalog, tagname):
    """
    Retornar la lista de Peliculas asociados a un tag
    """
    tag = mp.get(catalog['tags'], tagname)
    Movies = None
    if tag:
        Movies = me.getValue(tag)['Movies']
    return Movies


def MoviesSize(catalog):
    """
    Número de Peliculas en el catago
    """
    return lt.size(catalog['Movies'])


def authorsSize(catalog):
    """
    Numero de autores en el catalogo
    """
    return mp.size(catalog['authors'])


def tagsSize(catalog):
    """
    Numero de tags en el catalogo
    """
    return mp.size(catalog['tags'])


def getMoviesByYear(catalog, year):
    """
    Retorna los Peliculas publicados en un año
    """
    year = mp.get(catalog['years'], year)
    if year:
        return me.getValue(year)['Movies']
    return None

# ==============================
# Funciones de Comparacion
# ==============================
def compareMovieIds(id1, id2):
    """
    Compara dos ids de Peliculas
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareMapMovieIds(id, entry):
    """
    Compara dos ids de Peliculas, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1


def compareAuthorsByName(keyname, author):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(author)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1


def compareTagNames(name, tag):
    tagentry = me.getKey(tag)
    if (name == tagentry):
        return 0
    elif (name > tagentry):
        return 1
    else:
        return -1


def compareTagIds(id, tag):
    tagentry = me.getKey(tag)
    if (int(id) == int(tagentry)):
        return 0
    elif (int(id) > int(tagentry)):
        return 1
    else:
        return 0


def compareMapYear(id, tag):
    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
        return 1
    else:
        return 0


def compareYears(year1, year2):
    if (int(year1) == int(year2)):
        return 0
    elif (int(year1) > int(year2)):
        return 1
    else:
        return 0
def funcionmelaparaimprimir(catalog,n):
    d = catalog['Movies'][n]["original_title"]
    w = catalog['Movies'][n]["release_date"]
    o = catalog['Movies'][n]["vote_average"]
    s = catalog['Movies'][n]["vote_count"]
    h = catalog['Movies'][n]["spoken_languages"]
    print(d,w,o,s,h)
        