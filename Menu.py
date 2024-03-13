from Control_errores import control_errores #importamos el módulo de control de errores
def opciones_menu (): #Definimos la función menú, que se mostrará a través de pantalla al usuario
    print("Opciones para interactuar con el contrato: ")
    print("1._ Alta del Prestamista")
    print("2._ Alta del Cliente")
    print("3._ Depositar Garantia")
    print("4._ Solicitar Prestamo")
    print("5._ Aprobar Prestamo")
    print("6._ Reembolsar Prestamo")
    print("7._ Liquidar Garantia")
    print("8._ Obtener Prestamos por Cliente")
    print("9._ Obtener Detalle del Prestamo")
    print("0._ Salir")
        
def main(): # Definimos función que contiene el bucle que asigna la elección del usuario a la función a realizar
    while True:
        opciones_menu() #Llamada a la función para comparar la elección con la opciones del menú.
        eleccion = input("Por favor elija una opcion de (0-9): ")
        if eleccion.isdigit():
            eleccion = int(eleccion) 
            if 0 <= eleccion <= 9:
                if eleccion == 0:
                    print("Saliendo del Menu")
                    break
                control_errores(eleccion) #llamada al módulo de control de errores 
            else:
                print("Opcion fuera de rangp. Intentelo de nuevo")
        else:  
            print("Opcion no valida. Intentelo de nuevo")
if __name__ == "__main__": #llamada a la función main
    main()
                    