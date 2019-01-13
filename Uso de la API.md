PLa API del postprocesado de votos permite obtener los resultados de una votación, una vez mandada una petición indicando el tipo de recuento a seguir y las diferentes opciones de una votación junto a su número de votos.

Esta API cuenta con un sólo método, al cual se accederá mediante una petición POST a la url [https://decideiopostproc.herokuapp.com/postproc/](https://decideiopostproc.herokuapp.com/postproc/)
En el cuerpo de la petición POST, se enviará un JSON indicando el tipo de postprocesado que se quiere hacer y una lista con las opciones de la votación junto a sus números de votos, un atributo llamado "number" que es la posición en la que se encuentran dentro de la lista cuando se envían y algunos parámetros específicos según el tipo de procesado que se quiera. A continuación, se indica cómo debe construirse el JSON para cada tipo de procesado.

**A fecha de 05/01/2019 existen 3 tipos de procesado implementados. Esta sección se actualizará conforme se implementen más tipos**

## Procesado simple

Las opciones se ordenan teniendo en cuenta sólo los votos que han obtenido. En el campo "type" de la petición se enviará "IDENTITY, y las opciones irán acompañadas de su nombre, su número, y sus votos. A continuación se muestra un ejemplo de cómo debe ser el JSON que se envíe:

```js
{
    "type": "IDENTITY",
    "options": [{ "option": "Option 1", "number": 1, "votes": 5 },
         { "option": "Option 2", "number": 2, "votes": 0 },
         { "option": "Option 3", "number": 3, "votes": 3 },
         { "option": "Option 4", "number": 4, "votes": 2 },
         { "option": "Option 5", "number": 5, "votes": 5 },
         { "option": "Option 6", "number": 6, "votes": 1 }
    ]
}
```

La respuesta a esta petición será la lista de las opciones junto a sus atributos, ya ordenadas. Se le añadirá además a cada opción un nuevo atributo, "postproc", que indica el valor que se ha usado para ordenar las opciones, y que en este caso será igual a "votes".

## Procesado con pesos en las opciones
Las opciones contarán con un peso, y se ordenarán multiplicando su número de votos por su peso. En el campo "type" se enviará "WEIGHTED" y a los atributos por defecto de las opciones se le añadirá "weight", que será el valor por el que se multipliquen los votos de la opción. Un ejemplo de como debe ser el JSON es el siguiente:

```js
{
    "type": "WEIGHTED",
    "options": [
        { "option": "Option 1", "number": 1, "votes": 5,"weight":1},
        { "option": "Option 2", "number": 2, "votes": 0,"weight":1},
        { "option": "Option 3", "number": 3, "votes": 3,"weight":1},
        { "option": "Option 4", "number": 4, "votes": 2,"weight":2},
        { "option": "Option 5", "number": 5, "votes": 5,"weight":1.5},
        { "option": "Option 6", "number": 6, "votes": 1,"weight":1}
    ]
}
```


La respuesta seguirá el mismo formato que en el caso anterior, añadiendo esta vez el parámetro "weight" de cada opción y siendo el valor de "postproc" el producto de los votos por su peso.

## Procesado aleatorio

A partir de las opciones de la votación y sus votos, se escogerá una opción al azar, teniendo en cuenta que aquellas opciones que hayan tenido más votos tendrán más probabilidades de salir elegidas. El cuerpo de la petición será idéntico al del procesado simple, con la diferencia que en "type" el valor a enviar será "RANDOM"

La respuesta consistirá de una lista de opciones que en este caso sólo contendrá la opción que haya sido elegida. Tendrá los mismos atributos que la respuesta del procesado simple, siendo "postproc" también el número de votos obtenidos, y dos atributos nuevos: "randomNumber" que indica el número aleatorio usado en la elección del resultado y "percentageAccumulated", que indica el porcentaje de votos acumulados entre la opción elegida y todas aquellas que habían tenido igual o más votos que la elegida. Para comprobar que el proceso se ha realizado correctamente, basta con asegurarse que "randomNumber" sea menor que "percentageAccumulated"

## Recuento Borda

Se realiza el recuento borda a las opciones disponibles en la votacion. Se deben enviar las opciones ordenadas directamente por el usuario, sin ninguna modificación. Se debe adjuntar además una lista con las opciones disponibles en la votacion, en el campo "choices". El campo type se enviará "BORDA". Un ejemplo de JSON es el siguiente.

```js
{
    'type':'BORDA',
    'options':{
        'choices':['a','b','c','d','e'],
        'votes':[['d', 'b', 'c', 'a', 'e'],
                 ['e', 'd', 'c', 'b', 'a'],
                 ['b', 'c', 'd', 'a', 'e'],
                 ['a', 'e', 'd', 'c', 'b'],
                 ['b', 'e', 'd', 'c', 'a']]
    }
}
```

La respuesta será un diccionario con las opciones indicadas en choices y sus correspondientes resultados.  
Ejemplo:

```js
{'a': 11, 'b': 17, 'c': 14, 'd': 18, 'e': 15}
```
