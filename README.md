# Analizador de Secuencias FASTA

Programa de línea de comandos que calcula estadísticas básicas
(longitud y contenido GC) para secuencias de ADN en formato FASTA,
con opción de filtrar por criterios definidos por el usuario.

## Instalación

Clona el repositorio e instala el entorno con `uv`:

    git clone https://github.com/TU_USUARIO/analizador-fasta.git
    cd analizador-fasta
    uv sync

## Uso

Sintaxis general:

    uv run python src/analizador.py -i ARCHIVO_FASTA -o ARCHIVO_SALIDA [opciones]

### Ejemplos

Analizar todas las secuencias sin filtros:

    uv run python src/analizador.py -i data/ejemplo.fasta -o resultados.tsv

Filtrar secuencias de al menos 100 bases:

    uv run python src/analizador.py -i data/ejemplo.fasta -o resultados.tsv --min-len 100

Filtrar por longitud y contenido GC:

    uv run python src/analizador.py -i data/ejemplo.fasta -o resultados.tsv \
        --min-len 50 --min-gc 0.4 --max-gc 0.6

Ver todas las opciones disponibles:

    uv run python src/analizador.py --help

## Argumentos

| Argumento    | Tipo  | Requerido | Descripción                              |
|--------------|-------|-----------|------------------------------------------|
| `-i, --input`  | str | Sí        | Ruta al archivo FASTA de entrada         |
| `-o, --output` | str | Sí        | Ruta al archivo TSV de salida            |
| `--min-len`  | int   | No        | Longitud mínima de secuencia (en bases)  |
| `--max-len`  | int   | No        | Longitud máxima de secuencia (en bases)  |
| `--min-gc`   | float | No        | Contenido GC mínimo (entre 0.0 y 1.0)   |
| `--max-gc`   | float | No        | Contenido GC máximo (entre 0.0 y 1.0)   |

## Formato de salida

El archivo de salida es un TSV (tab-separated values) con tres columnas:

    encabezado          longitud    contenido_gc
    seq1 Homo sapiens   130         0.4872
    seq3 Homo sapiens   200         0.5538

## Documentación técnica

- [Requisitos del programa](docs/requisitos.md)
- [Diseño y diagrama de flujo](docs/diseño.md)
```
