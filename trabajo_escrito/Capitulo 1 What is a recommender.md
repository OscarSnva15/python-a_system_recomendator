# Capitulo 1: What is a recommender?

It is a jungle out there as far as understanding what what a recommender systems is // Es una jungla en cuanto a entender qué es un sistema recomendador.

Here's what we'll cover:

​	Understanding the task a recommender system is trying to emulate

​	Developing

​	Developing a taxonomy of how to describe recommenders

​	Introduccing the example website Movie GEEKs

# Real-life recommendations

this is an example of recommendations, Marino recommended the same things repeatedly, which is okay with food , but that isń the case for mot other types of products, such as books or movies or music,// este es un ejemplo de recomendaciones, Marino recomendó las mismas cosas repetidamente, lo cual está bien con la comida, pero ese no es el caso para la mayoría de los otros tipos de productos, como libros, películas o música.

# Recommender systems are at home on the internet

becausethis is where you can not only address individual users but can also collect behavioral data // porque aquí es donde no solo puede dirigirse a usuarios individuales, sino que también puede recopilar datos de comportamiento

Examples

A web site showing top 10 lists of the most sold bread-making machines provides non-personalized recommendations//Un sitio web que muestra las 10 listas principales de las máquinas para hacer pan más vendidas brinda recomendaciones no personalizadas

if a website for home sales or concert tickets shows you recommendations based on your demographics or your current location, the recomendations are semi-personalized //  si un sitio web de venta de entradas a domicilio o de conciertos le muestra recomendaciones basadas en sus datos demográficos o su ubicación actual, las recomendaciones son semipersonalizadas.

Personalized recommendations can be found on Amazon, where identifified customers see "Recomendation for you" // Se pueden encontrar recomendaciones personalizadas en Amazon, donde los clientes identificados ven "Recomendación para usted"

La idea de la recomendación personalizada también surge de la idea de que a la gente no solo le interesan los artículos populares, sino también los artículos que no se venden más o los artículos que están en la cola larga.

# The long tail//la cola larga

the long tail was coinded by chris anderson, in an article in wired magazine in 2004,whic was expanded into a book published in 2006.

in the articler Anderson's insight was that if you 've a brick-and-mortar shop , you' ve a limited ammount of storage and more importantly, a finite sapce to show products to your customers// en el artículo, la idea de Anderson fue que si tiene una tienda física, tiene una cantidad limitada de almacenamiento y, lo que es más importante, un espacio finito para mostrar productos a sus clientes

Without these limitations,you don have to sell only popular prodcu as with the usual commerce business model. 

# The netflix recommender system

as you likely know, netflix is a streamming site, it i domain is that of films and TV series and it has a continuosus flow of available content.

the porpuse of netflix's recomendations is to keep you interest in its content for as long as possibles and to keep you paying the subcription fee month after month.//el propósito de las recomendaciones de netflix es mantener su interés en su contenido el mayor tiempo posible y que siga pagando la tarifa de suscripción mes tras mes.

Definition: recommender system

A recommender system calaculates and provides relevant content to the user based on knowledge of the user, content, and interactions between the user and the item. // Un sistema de recomendación calcula y proporciona contenido relevante para el usuario en función del conocimiento del usuario, el contenido y las interacciones entre el usuario y el elemento.

# Algorithms

A number of algoritms are presented in this book. The algorithms fallinto two groups , and they depend on the type of data you use to make your recommendations. 

Algorithms that employ usage data are called collaborative filtering,.

Algorithms that use content metadata and user profiles to calculate recomendations are called content based filtering.

A mix of the two types is called hybrid recommenders.

colaborative filtering

//

En este libro se presentan varios algoritmos. Los algoritmos se dividen en dos grupos y dependen del tipo de datos que utilice para hacer sus recomendaciones.

Los algoritmos que emplean datos de uso se denominan filtrado colaborativo.

Los algoritmos que usan metadatos de contenido y perfiles de usuario para calcular recomendaciones se denominan filtrado basado en contenido.

Una combinación de los dos tipos se denomina recomendadores híbridos.

filtrado colaborativo



A prediction is different than a recomendation : A prediction is about project ing what rating a user would give content, while a recommendation is a list of items thaś relevant to the user : while a recommendations is a list of items thaś relevant to the user

// Una predicción es diferente a una recomendación: una predicción se trata de proyectar qué calificación le daría un usuario al contenido, mientras que una recomendación es una lista de elementos que son relevantes para el usuario: mientras que una recomendación es una lista de elementos que son relevantes para el usuario

un contexto de recomendación es lo que sucede alrededor del usuario

buildinng a recommender systems

1.- idea

2.- data

3 algorimos

4.- offline results

5.-offline testing

6.- Online testing



when a recommendation arrives,Items that might not be predicted to have the highest ratings can be recommended if they suit context.