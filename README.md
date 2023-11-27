---
# Steam Games, sistema de recomendación item-item

En este proyecto, asumo el papel de data scientist para realizar un análisis profundo de los sentimientos expresados por los usuarios de Steam en relación con los juegos, considerando aspectos como género, desarrollador y año de lanzamiento. Además, se ha desarrollado un MVP que incluye un modelo de recomendación item-item y un modelo NLP. En este contexto, hemos utilizado VADER para el análisis de sentimientos, proporcionando una interpretación numérica de las emociones expresadas.
---
# ETL (Extracción, Transformación y Carga)

Implementamos funciones dedicadas a facilitar el proceso de extracción, transformación y carga de los datos. Durante esta etapa, se realizaron imputaciones de datos redundantes o irrelevantes para nuestro estudio posterior en el EDA.
---
# EDA (Análisis Exploratorio de Datos)

En esta fase, procedimos a analizar los datos previamente procesados. Utilizamos funciones de seaborn y matplotlib para explorar visualmente los datos. Además, se retomó el análisis de sentimientos, creando una distribución que ofrece una perspectiva detallada de las emociones expresadas.
---
# ML  (Machine Learning)

Durante esta etapa, generamos los archivos necesarios para la implementación del modelo en la recomendación item-item. Optamos por utilizar el modelo de similitud coseno debido a la naturaleza matricial de la interpretación de los datos.

---

# Feature Engineering

En esta etapa, diseñamos funciones, la API y las tablas para su propio consumo. Se cargaron y procesaron los datos, y se llevó a cabo un análisis de sentimientos en la columna de reseñas utilizando VADER. En este análisis, asignamos valores de 1 para representar sentimientos negativos, 0 para neutral y 2 para positivos. Además, realizamos un análisis de sentimientos a lo largo de los años de lanzamiento de los juegos, presentando una distribución detallada de los resultados.
-Enlace de la API:
https://pi-steamgames-ocelotsega.onrender.com/docs#/

# Conclusiones 
Este proyecto de Steam Games, centrado en el desarrollo de un sistema de recomendación item-item y el análisis de sentimientos de usuarios, ha brindado valiosas percepciones sobre la interacción de la comunidad de Steam con los juegos. A continuación, se destacan algunas conclusiones clave:

1. Recomendación Personalizada: La implementación del modelo de recomendación item-item ha demostrado ser efectiva para proporcionar sugerencias personalizadas a los usuarios en función de sus preferencias históricas. Esto mejora significativamente la experiencia del usuario al ofrecer recomendaciones adaptadas a sus intereses.

2. Análisis de Sentimientos: La aplicación de VADER para el análisis de sentimientos ha enriquecido nuestra comprensión de la respuesta emocional de los usuarios a los juegos. La distribución de sentimientos a lo largo del tiempo proporciona una visión valiosa de las tendencias emocionales y permite a los desarrolladores y diseñadores ajustar estrategias en consecuencia.

3. Feature Engineering: La construcción de funciones específicas, el diseño de la API y la creación de tablas personalizadas han facilitado el consumo y la comprensión de los datos. La introducción de un análisis de sentimientos basado en VADER ha agregado una dimensión emocional a los datos, permitiendo una evaluación más completa.

4. Enlace de la API: La disponibilidad de la API proporciona una interfaz amigable para interactuar con los resultados del proyecto. Los desarrolladores y otros interesados pueden acceder fácilmente a las recomendaciones y análisis de sentimientos a través de la API.

En resumen, este proyecto ha combinado técnicas avanzadas de análisis de datos y aprendizaje automático con herramientas de análisis de sentimientos para ofrecer una solución integral que beneficia tanto a los usuarios como a los desarrolladores de juegos. Este enfoque puede adaptarse y ampliarse para abordar desafíos similares en el ámbito de las recomendaciones y el análisis de sentimientos en otras plataformas y aplicaciones.

