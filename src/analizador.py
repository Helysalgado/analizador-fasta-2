import argparse


def calcular_gc(secuencia):
    """
    Calcula el contenido GC de una secuencia.
    """

    if len(secuencia) == 0:
        return 0

    gc = secuencia.count("G") + secuencia.count("C")

    return gc / len(secuencia)


def leer_fasta(ruta):
    """
    Lee un archivo FASTA y devuelve una lista
    de tuplas (encabezado, secuencia).
    """

    secuencias = []

    encabezado = None
    secuencia_actual = ""

    with open(ruta, "r") as archivo:

        for linea in archivo:

            linea = linea.strip()

            if linea.startswith(">"):

                if encabezado is not None:

                    secuencias.append((encabezado, secuencia_actual))

                encabezado = linea[1:]

                secuencia_actual = ""

            else:

                secuencia_actual += linea

        if encabezado is not None:

            secuencias.append((encabezado, secuencia_actual))

    return secuencias


def calcular_estadisticas(encabezado, secuencia):
    """
    Calcula estadísticas de una secuencia.
    """

    longitud = len(secuencia)

    contenido_gc = calcular_gc(secuencia)

    return {
        "encabezado": encabezado,
        "longitud": longitud,
        "contenido_gc": contenido_gc,
    }


def pasa_filtros(stats, args):
    """
    Revisa si una secuencia pasa los filtros.
    """

    if args.min_len is not None:

        if stats["longitud"] < args.min_len:
            return False

    if args.max_len is not None:

        if stats["longitud"] > args.max_len:
            return False

    if args.min_gc is not None:

        if stats["contenido_gc"] < args.min_gc:
            return False

    if args.max_gc is not None:

        if stats["contenido_gc"] > args.max_gc:
            return False

    return True


def escribir_resultados(stats, ruta):
    """
    Escribe los resultados en un archivo TSV.
    """

    with open(ruta, "w") as archivo:

        archivo.write("encabezado\tlongitud\tcontenido_gc\n")

        for stat in stats:

            archivo.write(
                f"{stat['encabezado']}\t"
                f"{stat['longitud']}\t"
                f"{stat['contenido_gc']:.4f}\n"
            )


def parsear_argumentos():
    """
    Lee argumentos de línea de comandos.
    """

    parser = argparse.ArgumentParser(description="Analizador de secuencias FASTA")

    parser.add_argument("-i", "--input", required=True, help="Archivo FASTA de entrada")

    parser.add_argument("-o", "--output", required=True, help="Archivo TSV de salida")

    parser.add_argument("--min-len", type=int, default=None, help="Longitud mínima")

    parser.add_argument("--max-len", type=int, default=None, help="Longitud máxima")

    parser.add_argument(
        "--min-gc", type=float, default=None, help="Contenido GC mínimo"
    )

    parser.add_argument(
        "--max-gc", type=float, default=None, help="Contenido GC máximo"
    )

    return parser.parse_args()


def main():
    """
    Coordina todo el programa.
    """

    args = parsear_argumentos()

    print(f"Leyendo archivo: {args.input}")

    try:

        secuencias = leer_fasta(args.input)

    except FileNotFoundError:

        print(f"Error: no existe el archivo '{args.input}'")

        return

    print(f"{len(secuencias)} secuencias encontradas")

    resultados = []

    for encabezado, secuencia in secuencias:

        stats = calcular_estadisticas(encabezado, secuencia)

        if pasa_filtros(stats, args):

            resultados.append(stats)

    print(f"{len(resultados)} secuencias pasan los filtros")

    escribir_resultados(resultados, args.output)

    print(f"Resultados escritos en '{args.output}'")


if __name__ == "__main__":
    main()
