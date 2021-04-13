# Proyectos_Data_Science :zap::four_leaf_clover:

## Proyecto evolución de Inflacion y Salarios (base INDEC):money_with_wings:

El proyecto busca poder obtener mediante el lenguaje de Python la evolucion historica de la inflacion y tambien la evolucion historica de los salarios, para de esta forma poder combinar estas 2 informaciones y hacer una comparativa. Estos datos se muestran tanto de forma numerica como gráfica, para los años y meses que se encuentran disponible en la pagina web del INDEC (desde año 2016 hasta la fecha) .

En total consta de 10 outputs(funciones) posibles. Algunas de ellas son gráficos, otros información y otras combina graficos e información. 

Dentro del codigo se realazan comentarios explicando lo que se hace en cada paso.

*Los outputs posibles son:*:punch:

*- funciones.grafico_historico(): muestra graficamente la evolución de los salarios y la inflacion, y tambien la compraracion historica de salarios e inflacion respecto a su media aritmetica.*

*- funciones.grafbarras_ult_3*6_meses(): muestra graficamente la evolución de los salarios y la inflacion de los ultimos 36 meses, mediante un grafico de barras, mostrando el pico del indice salarial y el pico del indice inflacionario. Asi mismo, sobre el mismo grafico se presenta un grafico de linea de cada una de las variables.*

*- funciones.scatter_plot_inflacion(): se muestra un scatter plot de la inflacion historica, donde el tamaño y el color de cada burbuja representa el valor del indice inflacionario. A mayor tamaño y color mas oscuro el indice inflacionario será mayor.
*
*- funciones.whiskers_plot(): grafico de whiskers_plot donde se observa la dispersion de cada una de las variables de estudio.*

*- funciones.regresion_lineal(): se muestra graficamente una recta de correlacion entre salarios e inflacion medido en %*

*- funciones.inflacion_salarios_anual_filter(): se solicita al usuario que se intruzca un mes y en base al mismo se realiza una grafica interanual comparativa de inflacion y salarios. Asi mismo se muestra la informacion en un DataFrame tanto a nivel del mes seleccionado como de forma interanual.*

*- funciones.calculo_IPC_Salarios(): se pide al usuario que introduzca AÑO-MES en formato formato: YYYY-MM, tanto fecha desde como fecha hasta. Y en base a las fechas introducidas se informa la inflacion y la variacion salarial durante el periodo seleccionado.*

*- funciones.inflacion_puntual(): se pide al usuario que introduzca AÑO-MES en formato formato: YYYY-MM y se informa como salida la inflacion de ese periodo seleccionado.
*
*- funciones.calculo_inflacion_periodica(): se pide al usuario que introduzca AÑO-MES en formato formato: YYYY-MM, tanto fecha desde como fecha hasta. Y en base a las fechas introducidas se informa la inflacion del periodo seleccionado.*

*- funciones.forescast(): se le solicita al usuario la cantidad de meses que desea y se realiza una proyeccion de la inflacion para el periodo seleccionado mediante la tecnica de Forescast.*
