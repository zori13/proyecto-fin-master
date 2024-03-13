#Definimos las funciones para validar la eleccion del usuario
def eleccion1():
     print("1._ Alta del Prestamista")
def eleccion2():
    print("2._ Alta del Cliente")
def eleccion3():
    print("3._ Depositar Garantia")
def eleccion4():
    print("4._ Solicitar Prestamo")
def eleccion5():
    print("5._ Aprobar Prestamo")
def eleccion6():
    print("6._ Reembolsar Prestamo")
def eleccion7():
    print("7._ Liquidar Garantia")
def eleccion8():
    print("8._ Obtener Prestamos por Cliente")
def eleccion9():
    print("9._ Obtener Detalle del Prestamo")
def eleccion0():
    print("0._ Salir")

#Control de errores

def control_errores(eleccion):#esta función dará un error si la elección del usuario está fuera del rango que le damos a escoger
    try:
        eleciones={
            1: eleccion1,
            2: eleccion2,
            3: eleccion3,
            4: eleccion4,
            5: eleccion5,
            6: eleccion6,
            7: eleccion7,
            8: eleccion8,
            9: eleccion9,
            0: eleccion0,
        }
        eleciones[eleccion]()
    except KeyError:
        print("Opción no válida")
                
                
