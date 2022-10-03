# TUDI

## Objetivo

***TUDI*** es un lenguaje de programación para desarrollar videojuegos, o prototipos de videojuegos, con una vista 2D. 

La idea de ***TUDI*** es ser un lenguaje con el cuál el usuario pueda introducirse en el mundo de la programación a través del desarrollo de un pequeño proyecto que tenga en mente, ya que además de ser fácil de leer y entender, también contará con las principales características básicas que podrá encontrar en otros lenguajes en su futuro como desarrollador.

Características tales como lo son: *tipos de datos, entradas y salidas, variables, funciones y estructuras de datos básicas*.

## Características del lenguaje

La estructura general de un programa escrito en TUDI es:

```
/* Nombre del programa */
game <name>;

/* Declarar variables globales */
declare {
    int x;
    float [a, b, c];
}

/* Definir módulos */
func DoSomethingA : int () {
}

/* Función Start */
func Start : void () {
    /* Código que se llama únicamente una vez antes de todo */
}

/* Función Update */
func Update : void () {
    /* Código que se llama en cada frame */
}
```

