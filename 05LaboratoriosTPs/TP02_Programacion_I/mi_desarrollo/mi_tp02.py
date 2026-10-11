# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  .....................................
#  Comision:           .....................................
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO, MISION_LARGA

# =====================================================================
#  CONSTANTES
# =====================================================================

# Los cuatro comandos que el robot entiende los separo en dos grupos
# porque "avanzar" y "girar" llevan velocidad y tiempo, y los otros dos
# no llevan ningun dato.

COMANDOS_CON_DATOS = ("avanzar", "girar")
COMANDOS_SIN_DATOS = ("detenerse", "saludar")

# Marcas con las que empieza el texto que devuelve ejecutar_comando().
OK = "OK"
RECHAZADO = "RECHAZADO"

# Cuando el comando esta bien, el motivo de rechazo es una cadena vacia.
SIN_MOTIVO = ""


# =====================================================================
#  FUNCIONES AUXILIARES
# =====================================================================

def es_numero(valor):
    """
    Objetivo: Validar que el parámetro corresponde a un número ya sea entero o flotante.
    Parámetros:
        - valor(int/float): Variable a chequear tipo de dato.
    Devuelve:
        True si el valor es un numero de verdad (int o float).
    """
    return type(valor) == int or type(valor) == float

def motivo_de_rechazo(comando):
    """
    Objetivo: Especificar el motivo por el cual el comando no pudo ser ejecutado.
    Parámetros:
        - comando(tuple): Tupla con los datos del comando.
    Devuelve:
        str: Cadena de texto con el motivo por cual el comando no pudo ser ejecutado.
    """
    # 1. Tiene que ser una tupla.
    if type(comando) != tuple:
        return "no es una tupla de comando, es un " + type(comando).__name__

    # 2. La tupla no puede estar vacia.
    if len(comando) == 0:
        return "la tupla esta vacia y no dice que hacer"

    accion = comando[0]
    datos = len(comando) - 1 #Cuantos datos vinieron ademas del nombre

    # 3. El nombre tiene que ser uno de los cuatro validos.
    if accion not in COMANDOS_CON_DATOS and accion not in COMANDOS_SIN_DATOS:
        return "el comando '" + str(accion) + "' no existe"

    # 4. "detenerse" y "saludar" no llevan datos.
    if accion in COMANDOS_SIN_DATOS:
        if datos != 0:
            return "'" + accion + "' no lleva datos y le pasaron " + str(datos)
        return SIN_MOTIVO

    # 5. "avanzar" y "girar" llevan exactamente velocidad y tiempo.
    if datos != 2:
        return ("'" + accion + "' necesita velocidad y tiempo, "
                "y llegaron " + str(datos) + " dato/s")

    velocidad = comando[1]
    tiempo = comando[2]

    # 6. Velocidad y tiempo tienen que ser numeros, no textos.
    if not es_numero(velocidad):
        return "la velocidad tiene que ser un numero y llego '" + str(velocidad) + "'"

    if not es_numero(tiempo):
        return "el tiempo tiene que ser un numero y llego '" + str(tiempo) + "'"

    # 7. El tiempo no puede ser negativo.
    if tiempo < 0:
        return "el tiempo no puede ser negativo (" + str(tiempo) + " s)"

    return SIN_MOTIVO

# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    return motivo_de_rechazo(comando) == SIN_MOTIVO


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    # TU CODIGO ACA
    accion = comando[0]

    try:
        if accion == "avanzar":
            robot.avanzar(velocidad=comando[1], tiempo=comando[2])
            return "Comando avanzar ejecutado correctamente"
 
        elif accion == "girar":
            robot.girar(velocidad=comando[1], tiempo=comando[2])
            return "Comando girar ejecutado correctamente"
 
        elif accion == "detenerse":
            robot.detenerse()
            return "Robot detenido correctamente"
 
        elif accion == "saludar":
            robot.saludar()
            return "Saludo ejecutado correctamente"
 
        else:
            return "Comando desconocido"
 
    except ErrorDeSeguridad as error:
        return f"Comando rechazado: {error}"


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    # TU CODIGO ACA
    print("\nArranca la mision: " + str(len(mision)) + " comandos")
    print("-" * 68)
    for numero, comando in enumerate(mision, start=1):
        if comando_es_valido(comando):
            detalle = ejecutar_comando(robot, comando)
    
            if detalle.startswith(OK):
                estado = "ejecutado"
                motivo = SIN_MOTIVO
                capa = "-"
            else:
                estado = "rechazado"
                motivo = detalle.replace(RECHAZADO + ": ", "", 1)
                capa = "el robot"
        else:
            motivo = motivo_de_rechazo(comando)
            detalle = RECHAZADO + ": " + motivo
            estado = "rechazado"
            capa = "mi validacion"
        print("  " + str(numero).rjust(2) + ". " + str(comando))
        print("      -> " + detalle)

        historial.append({
                "numero": numero,
                "comando": comando,
                "estado": estado,
                "motivo": motivo,
                "capa": capa,
                "detalle": detalle,
            })
        print("-" * 68)


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    # TU CODIGO ACA
    """Contamos cuántos comandos se procesaron en total"""
    total = len(historial)
    
    """Filtramos el historial usando comprensión de listas:"""
    # Separo los pasos en dos listas con una comprension de listas.
    ejecutados = [paso for paso in historial if paso["estado"] == "ejecutado"]
    rechazados = [paso for paso in historial if paso["estado"] == "rechazado"]

    """Imprimimos el encabezado y las métricas principales de la misión"""
    print("\n" + "=" * 68)
    print("                      REPORTE FINAL DE LA MISION                      ")
    print("=" * 68)
    print(f"  Comandos recibidos : {total}")
    print(f"  Ejecutados         : {len(ejecutados)}")
    print(f"  Rechazados         : {len(rechazados)}")

    """Calculamos y mostramos el porcentaje de efectividad (evitando división por cero)"""
    if total > 0:
        porcentaje = (len(ejecutados) * 100) / total
        # El modificador :.1f redondea el número automáticamente a un decimal
        print(f"  Porcentaje OK      : {porcentaje:.1f} %")

    """Verificamos si hubo rechazos para cambiar el mensaje final"""
    if len(rechazados) == 0:
        print("\n  No hubo rechazos: la mision se ejecuto completa.")
    else:
        print("\n  Motivo de cada rechazo:")
        # Recorremos la lista de rechazados despaquetando cada tupla
        for paso in rechazados:
            print("    - comando " + str(paso["numero"]) + " " + str(paso["comando"]))
            print("      motivo  : " + paso["motivo"])
            print("      lo freno: " + paso["capa"])

    print("=" * 68 + "\n")


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    print("=== ELECCIÓN DE MISIÓN ===")
    print("1. Misión Básica")
    print("2. Misión Cuadrado")
    print("3. Misión con Errores")
    print("4. Misión Larga")
    
    opcion = input("Elija la misión que desea ejecutar (1-4): ").strip()

    if opcion == "1":
        mision_elegida = MISION_BASICA
        print("\n--> Ejecutando MISION_BASICA...\n")
    elif opcion == "2":
        mision_elegida = MISION_CUADRADO
        print("\n--> Ejecutando MISION_CUADRADO...\n")
    elif opcion == "3":
        mision_elegida = MISION_CON_ERRORES
        print("\n--> Ejecutando MISION_CON_ERRORES...\n")
    elif opcion == "4":
        mision_elegida = MISION_LARGA
        print("\n--> Ejecutando MISION_LARGA...\n")
    else:
        print("\nOpción inválida. Se ejecutará MISION_BASICA por defecto.\n")
        mision_elegida = MISION_BASICA

    robot = Robot()
    robot.conectar()

    historial = []

    try:
        ejecutar_mision(robot, mision_elegida, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
