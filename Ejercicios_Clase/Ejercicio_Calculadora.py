#Written and Directed by Jaime Orbea
#Edited by Alvorak
import tkinter
from enum import Enum
num=0 #el inical/por defecto de la calculadora


operacion= None #operacion que vamos a realizar
class Operaciones(Enum): # Definimos las operaciones
    SUMA = 1
    RESTA = 2
    MULTIPLICACION = 3

ventana=tkinter.Tk() #inicializar ventana 
ventana.geometry("400x300") #Tamaño de la ventana


cajaTexto=tkinter.Entry(ventana) #Metemos en ventana un label (textbox)
cajaTexto.grid(row=0, column=0, columnspan=4, pady=10)  #tamaño del label

#region Funciones calculadora
def mostrarEnCaja(valor): # funcion para mostrar en la caja de texto un valor (botones de la calculadora)
    actual=cajaTexto.get() #obtenemos el valor actual de la caja de texto
    cajaTexto.delete(0, tkinter.END) #borramos el contenido de la caja de texto
    cajaTexto.insert(0, actual+str(valor)) #insertamos el nuevo valor en la caja de texto

def suma(): # funcion para realizar la suma
    global num1, operacion #declaramos las variables globales
    num1=float(cajaTexto.get()) #obtenemos el valor de la caja de texto y lo convertimos a float
    operacion=Operaciones.SUMA #asignamos la operacion a realizar
    cajaTexto.delete(0, tkinter.END) #borramos el contenido de la caja de texto

def resta(): # funcion para realizar la resta
    global num1, operacion #declaramos las variables globales
    num1=float(cajaTexto.get()) #obtenemos el valor de la caja de texto y lo convertimos a float
    operacion=Operaciones.RESTA #asignamos la operacion a realizar
    cajaTexto.delete(0, tkinter.END) #borramos el contenido de la caja de texto

def multiplicación(): # funcion para realizar la multiplicacion
    global num1, operacion #declaramos las variables globales
    num1=float(cajaTexto.get()) #obtenemos el valor de la caja de texto y lo convertimos a float
    operacion=Operaciones.MULTIPLICACION #asignamos la operacion a realizar
    cajaTexto.delete(0, tkinter.END) #borramos el contenido de la caja de texto

def resultado(): # funcion para mostrar el resultado de la operacion
    num2=float(cajaTexto.get()) #obtenemos el valor de la caja de texto y lo convertimos a float
    cajaTexto.delete(0, tkinter.END) #borramos el contenido de la caja de texto
    match operacion: # evaluamos la operacion a realizar
        case Operaciones.SUMA:  
            cajaTexto.insert(0, int(num1+num2))
        case Operaciones.RESTA:
            cajaTexto.insert(0, int(num1-num2))
        case Operaciones.MULTIPLICACION:
            cajaTexto.insert(0, int(num1*num2))
#endregion

#region Botones calculadora

# Botones numéricos creados con bucle - distribución de calculadora estándar
# Estructura: [[7,8,9], [4,5,6], [1,2,3]]
botones_numeros = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3]
]

# Crear botones numéricos del 1-9 usando bucle
for fila_idx, fila in enumerate(botones_numeros): # Recorremos los numeros de la matriz de botones (fila)
    for col_idx, numero in enumerate(fila): # por cada columna
        boton = tkinter.Button( # Creamos el botón
            ventana, # entry => ventana
            text=str(numero), # texto del botón
            command=lambda num=numero: mostrarEnCaja(num), # comando al pulsar el botón (lo que se ejecuta)
            width=5, # ancho del botón
            height=2 # alto del botón
        )
        boton.grid(row=fila_idx + 1, column=col_idx, padx=5, pady=5) # posicionamos el botón en la ventana 
        #fila_idx + 1 porque la fila 0 es la caja de texto

# Botón 0 (posición especial)
boton0 = tkinter.Button(ventana, text="0", command=lambda: mostrarEnCaja(0), width=5, height=2)
boton0.grid(row=4, column=0, padx=5, pady=5)

# Botones de operaciones - columna derecha
operaciones_botones = [ 
    ("x", multiplicación, 1),  # (texto, función, fila)
    ("-", resta, 2),
    ("+", suma, 3),
    ("=", resultado, 4)
]
# Crear botones de operaciones usando bucle
for texto, funcion, fila in operaciones_botones: # Recorremos la lista de operaciones
    boton = tkinter.Button( 
        ventana, 
        text=texto, 
        command=funcion,
        width=5,
        height=2
    )
    boton.grid(row=fila, column=3, padx=5, pady=5) # posicionamos el botón en la ventana
    #columna 3 porque es la columna derecha

# endregion

ventana.mainloop() #muestra la ventana hasta que se cierre
