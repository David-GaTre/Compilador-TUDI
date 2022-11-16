# TUDI

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

### Tokens

|Token|RegEx|Descripción|
|:---:|:---:|---|
|START|Start|Es la función inicial, la primera que se va a correr al iniciar el programa.|
|UPDATE|Update|Es la función que se ejecuta durante cada frame del programa.|
|GAME|game|Va a servir para guardar el título del juego desde el programa.|
|PRINT|Print|Va a servir para mostrar output al usuario en la consola.|
|READ|Read|Va a servir para recibir input del usuario.|
|SETPOSITION|SetPosition|Va a servir para posicionar un sprite en el canvas, recibe dos float.|
|TRANSLATE|Translate|Va a servir para mover a un sprite en dos dimensiones, recibe dos float.|
|SETCONTROLLABLE|SetControllable|Va a servir para definir si un sprite es posible controlarlo con las teclas, recibe bool.|
|INT|int|Inicia la declaración del tipo de dato entero.|
|FLOAT|float|Inicia la declaración del tipo de dato float.|
|BOOLEAN|bool|Inicia la declaración del tipo de dato booleano.|
|CHAR|char|Inicia la declaración del tipo de dato char.|
|VOID|void|Tipo de dato de retorno de una función que no regresará nada.|
|CANVAS|canvas|Representa el espacio en el que se podrán dibujar sprites.|
|SPRITE|sprite|Representa un objeto en 2 dimensiones.|
|FUNC|func|Representa que lo siguiente será una función.|
|RETURN|return|Palabra reservada cuyo siguiente valor o variable tendrá que ser del mismo tipo de la función en la que está dentro.|
|DECLARE|declare|Palabra reservada cuya función es iniciar el bloque donde se declaran las variables.|
|IF|if|Palabra reservada para inicializar un condicional.|
|ELSE|else|Palabra reservada para indicar un caso alterno en una condicional.|
|FOR|for|Inicialización de un ciclo for.|
|WHILE|while|Inicialización de un ciclo while.|
|;|\\;|Al final de declarar estatutos se colocará este token para indicar su fin.|
|:|\\:|Para declarar el tipo de retorno de una función.|
|,|\\,|Servirá para listar valores dentro de un arreglo (hacer la división entre valores) así como ayudar a declarar distintas dimensiones en un arreglo.|
|=|\\=|Se utilizará para las asignaciones de variables.|
|{|\\{|Se utilizará para iniciar un bloque de código.|
|}|\\}|Se utilizará para finalizar un bloque de código.|
|(|\\(|Tendrá como propósito indicar las llamadas a funciones o inicializar los paréntesis en una expresión.|
|)|\\)|Tendrá como propósito indicar el final de una llamada a función, después de llamar a los parámetros o finalizar los paréntesis en una expresión.|
|[|\\[|Servirá para iniciar la declaración de un arreglo o intento de acceso a un arreglo.|
|]|\\]|Servirá para finalizar la declaración de un arreglo o intento de acceso a un arreglo.|
|+|\\+|Servirá para hacer sumas en las expresiones, o en el caso de los chars, anidar un char al final del arreglo de chars.|
|-|\\-|Servirá para hacer las restas en las expresiones.|
|/|\\/|Servirá para hacer las divisiones en las expresiones.|
|*|\\*|Servirá para hacer las multiplicaciones en las expresiones.|
|>|\\>|Operador de comparación mayor qué.|
|>=|\\>\\=|Operador de comparación mayor o igual qué.|
|<|\\<|Operador de comparación menor qué.|
|<=|\\<\\=|Operador de comparación menor o igual qué.|
|==|\\=\\=|Operador de comparación igual qué.|
|!=|\\!\\=|Operador de comparación de no igual qué.|
|AND|y|Operador lógico de and|
|OR|o|Operador lógico de or|
|NOT|no|Operador lógico de not|
|INT_LITERAL|[0-9]|Servirá para validar los datos de tipo entero.|
|FLOAT_LITERAL|[0-9]+(\.[0-9]+)|Servirá para validar los datos de tipo flotante.|
|BOOL_LITERAL|(true)\|(false)|Servirá para identificar un valor de verdadero o falso.|
|STRING_LITERAL|\\"(\\w+\|\\s)+\\"|Servirá para identificar todo aquello que sea una palabra entre comillas.|
|ID|[a-zA-Z_][a-zA-Z_0-9]*|Servirá para crear identificadores para las variables.|

### Características de la semántica
La función **Read** recibe un STRING_LITERAL o un id de un arreglo de caracteres, el STRING se utiliza para mostrar un prompt al solicitar input del usuario y el valor de retorno es un arreglo de chars del tamaño de lo leído del usuario.

Esto se combina con las funciones de casteo para convertir un arreglo de caracteres o un STRING_LITERAL en un INT, FLOAT o BOOLEAN. Es decir, estas tres funciones de casteo, **type(arr)**, reciben un arreglo de caracteres y regresan un valor del tipo acorde. 

Un valor de tipo de dato sprite se crea con un tamaño y color. Y cuenta con tres métodos principales, los cuáles son: 
- **SetPosition**(float, float): se utiliza para colocar el sprite en el canvas en las coordenadas provistas.
- **SetControllable**(boolean): un valor verdadero indica que el sprite será controlable con input del usuario, al usar las flechas del teclado.
- **Translate**(float, float): Mueve el sprite hacía utilizando los componentes provistos de un vector 2D.

También existe un objeto global canvas al que se le deben asignar sus dimensiones al principio del programa con un estatuto:
- canvas=width, height;

Se estará manejando una lógica numérica en la que 0 será el único valor para falso, mientras que cualquier otro valor numérico representará el valor para verdadero. Mientras tanto, el tipo de dato **bool** es una especie de subclase de int, en la que se manejan dos palabras claves para los valores de verdadero y falso (True y False). **True** tendrá básicamente un valor de 1, mientras que **False** tendrá un valor de 0.
