# TUDI

## QUE SE NECESITA INSTALAR
Tenemos que tener python3 ya instalado en nuestra máquina. Luego de esto solo necesitamos instalar el paquete de PyGame que viene en el documento de requerimientos.

`$ pip install -r requirements.txt`

## COMO CORRER UN PROGRAMA
`$ python virtual_machine.py [NOMBRE DE ARCHIVO]`

Ejemplo:
`$ python virtual_machine.py test_cases/multiplicacion_matriz.tudi`


## Avance 7
Creación de cuádruplos de arreglos y de funciones I/O.

Refactorización de la clase de memoria virtual así como actualización del manejo de memoria virtual para creación de cuádruplos y ejecución. Creación de clase de memoria de funciones para matar memoria al final de ejecución. 

Creación completa de máquina virtual así como cambio en manera de ejecutar programas.

## Avance 6
Creación de memoria virtual en todos los niveles y sustitución con memorias virtuales en los cuádruplos. Código de funciones y sus cuádruplos esta terminado.

Queda pendiente primeras iteraciones de máquina virtual y cuádruplos de arreglos.


## Avance 5
Se implementan borradores de los cuadruplos de los condicionales (if - else - else if) y de ciclo while. Se generaron funciones adicionales para generar cuadruplos desde el parser.

Se planea implementar el ciclo for y encontrar casos de prueba adicionales.

## Avance 4
Se implementa la generación de cuadruplos para expresiones aritméticas, relacionales y lógicas. 
Se implementa una más estructurada suite de testing. En la que se checa que la sintaxis funcione y los cuadruplos sean los esperados.

Se trabaja en terminar la generación de cuadruplos para estatutos secuenciales, condicionales y ciclos

## Avance 3
Se corrige un error en la gramática de las expresiones relacionales (<, <=, ==, !=, >=, >). Se agrega la primera iteración del cubo semántico.

Se están corrigiendo comentarios del directorio de funciones y tablas de variables. Y se está trabajando en la generación de los cuádruplos.

## Avance 2
Se completó lo pendiente del avance 1, solucionando los errores de la gramática y los conflictos shift/reduce. Se cambió la escritura de los tokens en el parser para anotar los caracteres por su cuenta. Se agregaron tokens para llamadas a funciones y de métodos propios del lenguaje. Actualmente todos los tokens son utilizados a excepción del operador lógico NOT que queda pendiente para el siguiente avance. 

Se creó el cuadro semántico de tipos, queda pendiente completar el cubo semántico para añadir las operandos.

Queda pendiente también añadir los recursos semánticos básicos al código del lenguaje.

## Avance 1

Estado incompleto, con errores por encontrar y arreglar en reglas de la gramática. Al parecer son conflictos shift/reduce. Y también tenemos tokens que aún no están siendo utilizados. Y hace falta agregar algunos statements como el return, letreros, entre otros. 

1. Funciones Start y Update marca error en el token donde se menciona el nombre de la funcion.
2. Declaracion de variables múltiples causa problemas.

## Objetivo

***TUDI*** es un lenguaje de programación para desarrollar videojuegos, o prototipos de videojuegos, con una vista 2D. 

La idea de ***TUDI*** es ser un lenguaje con el cuál el usuario pueda introducirse en el mundo de la programación a través del desarrollo de un pequeño proyecto que tenga en mente, ya que además de ser fácil de leer y entender, también contará con las principales características básicas que podrá encontrar en otros lenguajes en su futuro como desarrollador.

Características tales como lo son: *tipos de datos, entradas y salidas, variables, funciones y estructuras de datos básicas*.

## Características del lenguaje

La estructura general de un programa escrito en TUDI es:

```
/* Nombre del programa y tamaño de canvas */
game <name>;
canvas = 10, 10;

/* Declarar variables globales */
declare {
    float a, b, c;
    int[5] vector;
    int[5, 5] matriz;
}

/* Definir módulos */
func DoSomethingA : int () {
    declare {
        int x;
    }
    x = 1;
    return x;
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
