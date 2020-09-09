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

import config as cf
from App import model
import csv
from DISClib.ADT import list as lt
from collections import OrderedDict
from DISClib.ADT import map 



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
def loadData(catalog, Moviesfile, tagsfile, Movietagsfile):
    """
    Carga los datos de los archivos en el modelo
    """
    loadMovies(catalog, Moviesfile)
    """loadTags(catalog, tagsfile)
    loadMoviesTags(catalog, Movietagsfile)"""

def transformar(input_file, catalog):
    lista = lt.newList('ARRAY_LIST')
    for Movie in input_file:
        for key, value in Movie.items():
             i = str(value)
             w = str(key)
             listak = w.split(";")
              
             listav = i.split(";")
             model.addMovie(catalog, listak)
             if len(listam) ==19:
              model.addMovieAuthor(catalog, author.strip(), listak)
             if len(listam) !=19:
                 print(listam, len(listam))
    return lista
def loadMovies(catalog, Moviesfile):
    """
    Carga cada una de las lineas del archivo de Peliculas.
    - Se agrega cada Pelicula al catalogo de Peliculas
    - Por cada Pelicula se encuentran sus autores y por cada
      autor, se crea una lista con sus Peliculas
    """
    Moviesfile = cf.data_dir + Moviesfile
    input_file = csv.DictReader(open(Moviesfile,encoding ="utf-8-sig"))
    w = transformar(input_file,catalog)
    for a in w:
        model.addMovie(catalog, a)


def loadTags(catalog, tagsfile):
    """
    Carga en el catalogo los tags a partir de la informacion
    del archivo de etiquetas
    """
    tagsfile = cf.data_dir + tagsfile
    input_file = csv.DictReader(open(tagsfile,encoding ="utf-8-sig"))
    for tag in input_file:
        model.addTag(catalog, tag)


def loadMoviesTags(catalog, Movietagsfile):
    """
    Carga la información que asocia tags con Peliculas.
    Primero se localiza el tag y se le agrega la información leida.
    Adicionalmente se le agrega una referencia al Pelicula procesado.
    """
    Movietagsfile = cf.data_dir + Movietagsfile
    input_file = csv.DictReader(open(Movietagsfile,encoding ="utf-8-sig"))
    for tag in input_file:
        model.addMovieTag(catalog, tag)
# Funciones para consultas 

def MoviesSize(catalog):
    """Numero de Peliculas leido
    """
    return model.MoviesSize(catalog)


def authorsSize(catalog):
    """Numero de autores leido
    """
    return model.authorsSize(catalog)


def tagsSize(catalog):
    """Numero de tags leido
    """
    return model.tagsSize(catalog)

def getMoviesByAuthor(catalog, authorname):
    """
    Retorna los Peliculas de un autor
    """
    authorinfo = model.getMoviesByAuthor(catalog, authorname)
    return authorinfo


def getMoviesByTag(catalog, tagname):
    """
    Retorna los Peliculas que han sido marcados con
    una etiqueta
    """
    Movies = model.getMoviesByTag(catalog, tagname)
    return Movies


def getMoviesYear(catalog, year):
    """
    Retorna los Peliculas que fueron publicados
    en un año
    """
    Movies = model.getMoviesByYear(catalog, year)
    return Movies
