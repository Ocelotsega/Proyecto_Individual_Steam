
# *Proyecto Individual ML-OPS Steam Games*


![SteamGames](https://gamersunite.mx/wp-content/uploads/2021/12/videojuegos-en-8-bit.jpg)



---

# Steam Games: Sistema de Recomendación Item-Item

En este proyecto, asumo el rol de data scientist para llevar a cabo un análisis exhaustivo de los sentimientos expresados por los usuarios de Steam en relación con los juegos, considerando aspectos clave como género, desarrollador y año de lanzamiento. Como parte fundamental de este trabajo, hemos desarrollado un MVP que incluye un robusto modelo de recomendación item-item y un modelo NLP. En este contexto, hemos empleado VADER para el análisis de sentimientos, proporcionando una interpretación numérica precisa de las emociones expresadas.


---
# ETL (Extracción, Transformación y Carga)

Implementamos funciones especializadas para facilitar el proceso de extracción, transformación y carga de datos. Durante esta fase, llevamos a cabo imputaciones para eliminar datos redundantes o irrelevantes, preparando así un conjunto de datos óptimo para nuestro análisis posterior en el EDA.

---
# EDA (Análisis Exploratorio de Datos)

En esta etapa crítica, procedimos al análisis de los datos previamente procesados. Utilizando herramientas como seaborn y matplotlib, exploramos visualmente los datos y, además, retomamos el análisis de sentimientos. Creamos una distribución detallada que proporciona una perspectiva profunda de las emociones expresadas por los usuarios.


---
# ML  (Machine Learning)

Durante esta etapa, generamos los archivos necesarios para la implementación del modelo en la recomendación item-item. Optamos por utilizar el modelo de similitud coseno debido a la naturaleza matricial de la interpretación de los datos, garantizando así una eficaz identificación de patrones y preferencias.

---
# Feature Engineering

En esta fase crítica, diseñamos funciones especializadas, desarrollamos una API intuitiva y creamos tablas optimizadas para su propio consumo. Realizamos una carga y procesamiento eficiente de los datos y llevamos a cabo un análisis de sentimientos en la columna de reseñas utilizando VADER. En este análisis, asignamos valores de 1 para representar sentimientos negativos, 0 para neutral y 2 para positivos. Además, realizamos un análisis de sentimientos a lo largo de los años de lanzamiento de los juegos, presentando una distribución detallada de los resultados.

[API](https://pi-steamgames-ocelotsega.onrender.com/docs)
[Video](https://youtu.be/i9gnxpeYu4s?si=m4pj1VCbuOZ52T1E)

---  
# Conclusiones 

En resumen, este proyecto ha amalgamado técnicas avanzadas de análisis de datos y aprendizaje automático con herramientas de análisis de sentimientos. Proporciona una solución integral que beneficia tanto a los usuarios como a los desarrolladores de juegos. Este enfoque se presenta como una base sólida, adaptable y expansible para abordar desafíos similares en el ámbito de las recomendaciones y el análisis de sentimientos en diversas plataformas y aplicaciones.

## Autor 

**Jordi Mikel Segarra Guerra**
