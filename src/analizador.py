"""Analizador simple de secuencias FASTA.

Proporciona utilidades para leer archivos FASTA, calcular
estadísticas básicas (longitud y contenido GC) y escribir
resultados en formato TSV.

Este módulo valida la existencia de archivos al abrirlos,
acepta secuencias con bases en minúsculas y documenta las
funciones principales.
"""

import argparse
import os


def calcular_gc(secuencia: str) -> float:
    """Calcula el contenido GC de una secuencia.

    Convierte la secuencia a mayúsculas para contar tanto
    letras mayúsculas como minúsculas ('g' y 'c').

    Args:
        secuencia: Secuencia de ADN/ARN.

    Returns:
        Fracción de bases que son G o C (entre 0 y 1). Retorna 0
        si la secuencia está vacía.
    """

    if len(secuencia) == 0:
        return 0.0

    seq_up = secuencia.upper()
    gc = seq_up.count("G") + seq_up.count("C")

    return gc / len(secuencia)


def leer_fasta(ruta):
    """
    Lee un archivo FASTA y devuelve una lista
    de tuplas (encabezado, secuencia).
    """

    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

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

        print(f"{len(secuencias)} secuencias encontradas")

        resultados = []

        for encabezado, secuencia in secuencias:
            stats = calcular_estadisticas(encabezado, secuencia)
            if pasa_filtros(stats, args):
                resultados.append(stats)

        print(f"{len(resultados)} secuencias pasan los filtros")

        try:
            escribir_resultados(resultados, args.output)
        except OSError as e:
            print(f"Error al escribir '{args.output}': {e}")
            return

        print(f"Resultados escritos en '{args.output}'")

    except FileNotFoundError:
        print(f"Error: no existe el archivo '{args.input}'")
        return
    except Exception as e:
        print(f"Error inesperado: {e}")
        return


if __name__ == "__main__":
    main()
