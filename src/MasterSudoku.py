#!/usr/bin/python3

# Universidad de Costa Rica
# Facultad de Ingenieria
# Escuela de Ingenieria Electrica
# Programacion bajo plataformas abiertas
# Prof: Julian Gairaud
# David Rodriguez Gutierrez / B59281
# Proyecto de Python

# Introduccion:

# El codigo de este documento implementa un juego de
# Sudoku, el cual da a escoger al usuario 3 niveles de
# dificultad. Asimismo, al principio se dan las reglas del
# juego y en tanto se elija el nivel deseado, se abrira
# la interfaz que contiene el tablero. Cabe destacar que,
# en tanto el usuario coloque un numero donde no vaya,
# automaticamente la casilla se pondr'a en rojo. AL final
# de la partida se mostrara un mensaje de felicitaciones
# al haber completado correctamente el tablero.

# Resolucion:

import numpy as np
import random
import copy
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa

# Llamamos el Builder de Gtk
builder = Gtk.Builder()

# Llamamos el proyecto
builder.add_from_file("MasterSudoku.glade")

# Llamamos las ventanas
ventana_instrucciones_botones = builder.get_object(
    "ventana_instrucciones_botones")
ventana_interfaz = builder.get_object("ventana_interfaz")

# Llamamos los contenedores
contenedor_instrucciones_botones = builder.get_object(
    "contenedor_instrucciones_botones")
contenedor_botones_dificultad = builder.get_object(
    "contenedor_botones_dificultad")
contenedor_interfaz = builder.get_object("contenedor_interfaz")
contenedor_cuadricula = builder.get_object("contenedor_cuadricula")

# Llamamos los objetos
boton_dificil = builder.get_object("boton_dificil")
boton_intermedio = builder.get_object("boton_intermedio")
boton_facil = builder.get_object("boton_facil")
label_dificultad = builder.get_object("label_dificultad")


# Creamos una funcion que genere un tablero completo de Sudoku
def tablero():

    # Primero se genera una matriz de ceros de 9x9
    matriz = np.zeros((9, 9), dtype=int)

    for i in range(9):
        for k in range(9):

            # Guardamos en un vector los valores posibles a
            # asignar en un sudoku.

            valores_posibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            # Verificamos si en la misma fila del elemento [i, j]
            # se encuentra ya el valor, si ya se encuentra, se elimina
            # del vector de valores posibles.

            valores_fila = set(matriz[i, :])
            valores_posibles = [
                n for n in valores_posibles if n not in valores_fila]

            # Verificamos si en la misma columna del elemento [i, j] se
            # encuentra ya el valor, si ya se encuentra, se elimina del
            # vector de valores posibles.

            valores_columna = set(matriz[:, k])
            valores_posibles = [
                n for n in valores_posibles if n not in valores_columna]

            # Verificamos si en el mismo subcuadrante del elemento [i, j]
            # se encuentra ya el valor, si ya se encuentra, se elimina
            # del vector de valores posibles.

            fila_inicio, columna_inicio = 3 * (i // 3), 3 * (k // 3)
            subcuadrante = matriz[
                fila_inicio:fila_inicio + 3, columna_inicio:columna_inicio + 3]

            valores_subcuadrante = set(subcuadrante.flatten())
            valores_posibles = [
                n for n in valores_posibles if n not in valores_subcuadrante]

            # Ya teniendo un vector con los valores posibles a asignar,
            # le asignamos un valor random a esa posicion.
            if valores_posibles:
                matriz[i, k] = random.choice(valores_posibles)
            else:
                # Si no hay valores posibles se reinicia la fila
                return tablero()

    return matriz

# Creamos tres funciones, una para cada dificultad. Lo que se hace es
# colocar ceros aleatoriamente en la matriz completada dependiendo
# de la dificultad.


def facil(button):

    # Se llama la funcion rablero() para generar el tablero completado.

    tablero_dificultad = tablero()

    # Le hacemos una deepcopy para tener una matriz fija con la solucion.

    solucion = copy.deepcopy(tablero_dificultad)

    # Iteramos 30 veces para eliminar valores de la matriz
    # tablero_dificultad().

    for _ in range(0, 31):
        i = random.randint(0, 8)
        j = random.randint(0, 8)

        tablero_dificultad[i, j] = 0

    # Al llegar a este punto se destruye la ventana de instrucciones.

    ventana_instrucciones_botones.destroy()

    # Se cambia el texto en el label

    label_dificultad.set_text("Nivel de Dificultad: Facil")

    # Llamamos la funcion jugar, a la cual le pasamos tablero_dificultad
    # y la solucion.

    jugar(tablero_dificultad, solucion)


def intermedio(button):
    tablero_dificultad = tablero()
    solucion = copy.deepcopy(tablero_dificultad)

    for _ in range(0, 51):
        i = random.randint(0, 8)
        j = random.randint(0, 8)

        tablero_dificultad[i, j] = 0

    ventana_instrucciones_botones.destroy()

    label_dificultad.set_text("Nivel de Dificultad: Intermedio")

    jugar(tablero_dificultad, solucion)


def dificil(button):
    tablero_dificultad = tablero()
    solucion = copy.deepcopy(tablero_dificultad)

    for _ in range(0, 71):
        i = random.randint(0, 8)
        j = random.randint(0, 8)

        tablero_dificultad[i, j] = 0

    ventana_instrucciones_botones.destroy()

    label_dificultad.set_text("Nivel de Dificultad: Dificil")

    jugar(tablero_dificultad, solucion)

# Definimos la funcion jugar que toma tablero_dificultad y la solucion y
# dependiendo de donde exsitan valores distintos de cero, asigna un label
# con ese valor. Si existe un cero en la matriz, coloca un entry para que
# el usuario ingrese su solucion a la casilla.


def jugar(tablero_dificultad, solucion):

    for i in range(0, 9):
        for j in range(0, 9):

            if tablero_dificultad[i, j] != 0:
                label = Gtk.Label(label=str(tablero_dificultad[i][j]))
                label.set_size_request(1, 70)
                contenedor_cuadricula.attach(label, j, i, 1, 1)

            else:
                entry = Gtk.Entry()
                entry.set_size_request(1, 70)
                entry.set_alignment(0.5)
                contenedor_cuadricula.attach(entry, j, i, 1, 1)

                # Aqui, conectamos los entrys a la funcion comparativa

                entry.connect("changed", comparativa, i, j, solucion)

    # Ya llena la interfaz, la mostramos

    ventana_interfaz.show_all()

# Creamos una funcion que detecta si el valor ingresado en los entrys
# difieren de la matriz solucion.


def comparativa(entry, i, j, solucion):
    valor_ingresado = entry.get_text()

    # Con un if, cambiamos el color de la casilla entry a rojo si el valor
    # ingresado difiere de su correspondiente en la matriz solucion
    # Para esto utilizamos la herramienta CssProvider para cambiar de
    # estilo las casillas

    if valor_ingresado and valor_ingresado != str(solucion[i, j]):
        css = Gtk.CssProvider()
        css.load_from_data(b'entry { background-color: red; }')

        color = entry.get_style_context()
        color.add_provider(css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    # Si la casilla esta vacia o el valor esta bien, se mantiene en su
    # color original

    else:
        css = Gtk.CssProvider()
        css.load_from_data(b'entry { background-color: unset; }')

        color = entry.get_style_context()
        color.add_provider(css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Llamamos la funcion salida y le pasamos los parametros
        # contenedor_cuadricula y la solucion del sudoku

        if salida(contenedor_cuadricula, solucion):
            label_dificultad.set_text(
                "¡Enhorabuena! Has completado el Sudoku correctamente.")

# Definimos una funcion que revisa si la matriz contenedor_cuadricula es
# igual ya completada a la matriz solucion


def salida(contenedor_cuadricula, solucion):
    # Iterate through all entries and check if they match the solution
    for i in range(9):
        for j in range(9):
            if isinstance(contenedor_cuadricula.get_child_at(j, i), Gtk.Entry):
                entrada = contenedor_cuadricula.get_child_at(j, i).get_text()
                if entrada != str(solucion[i, j]):
                    return False

    return True


# Ya con esas funciones creadas, conectamos cada boton a cada funcion
# y dejamos que el codigo avance

ventana_instrucciones_botones.show_all()

boton_facil.connect("clicked", facil)
boton_intermedio.connect("clicked", intermedio)
boton_dificil.connect("clicked", dificil)

ventana_interfaz.connect("destroy", Gtk.main_quit)
Gtk.main()
