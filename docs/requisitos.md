# Requisitos del Analizador de Secuencias FASTA

## Descripción del problema

En bioinformática, el formato FASTA es uno de los más usados para almacenar
secuencias de ADN, ARN o proteínas. Cada secuencia tiene dos partes:

1. Una línea de **encabezado** que empieza con `>` y contiene el nombre o
   identificador de la secuencia.
2. Una o más líneas con la **secuencia** de bases (A, T, G, C).

Ejemplo de archivo FASTA:

    >seq1 Homo sapiens BRCA1
    ATGCGATCGATCGATCGCTATCGATCGTAGCTAGCTAGC
    ATCGATCGATCGATCGATCGATCGATCGATCGATCGAT
    >seq2 Mus musculus Actb
    GCGCGCGCGCATCGATCGATCGATCG

En proyectos de genómica es común recibir archivos FASTA con cientos o miles de
secuencias y necesitar filtrarlas por características básicas antes de un análisis
más profundo.

## Objetivo

Construir un programa en Python que procese un archivo FASTA y produzca un reporte
con estadísticas básicas, permitiendo filtrar las secuencias por criterios definidos
por el usuario.

## Requisitos funcionales

1. El programa debe recibir la ruta del archivo FASTA como argumento de línea de comandos.
2. El programa debe recibir la ruta del archivo de salida como argumento.
3. El programa debe calcular para cada secuencia:   
   - Longitud (número de bases)
   - Contenido GC (proporción de bases G y C entre 0 y 1)
4. El programa debe permitir filtrar secuencias por:   
   - Longitud mínima (`--min-len`)
   - Longitud máxima (`--max-len`)
   - Contenido GC mínimo (`--min-gc`)
   - Contenido GC máximo (`--max-gc`)
   Todos los filtros son opcionales.
5. El archivo de salida debe ser un TSV (valores separados por tabulador)
   con columnas: `nombre de secuencia (encabezado)`, `longitud`, `contenido_gc`.
6. El programa debe manejar errores cuando el archivo de entrada no existe.

## Entrada y salida esperadas

**Entrada:**

```
uv run python src/analizador.py -i data/ejemplo.fasta -o resultados.tsv --min-len 50
```

**Salida en consola:**

```
Leyendo archivo: data/ejemplo.fasta
  4 secuencias encontradas
  2 secuencias pasan los filtros
Resultados escritos en 'resultados.tsv'
```

**Archivo `resultados.tsv`:**

```
encabezado	longitud	contenido_gc
seq1 Homo sapiens BRCA1	78	0.4872
seq3 Homo sapiens TP53	130	0.5538
```

~~~

> **💡 ¿Por qué escribir los requisitos antes de programar?**  
> Los requisitos son un contrato: definen exactamente qué debe hacer tu programa.
> Si los tienes escritos, puedes verificar al final si cumpliste con todo.
> 


**Lee detenidamente esto que copiaste para entender el problema. No puedes continuar si no te queda claro de que trata el problema.**
