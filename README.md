# Proyectos_Data_Science :zap::four_leaf_clover:
En este repositorio muestro los proyectos de Data_Science relacionados con diferentes variables economicas y sus vinculos. Ejemplo inflacion y salarios, plazos fijos. Y tambien incluye proyecto relacionado con el mercado financiero y la comparacion emtre los diferentes activos.

# **PROYECTO 1**:mag_right:
## Proyecto evolución de Inflacion y Salarios (base INDEC):money_with_wings:

El proyecto busca poder obtener mediante el lenguaje de Python la evolucion historica de la inflacion y tambien la evolucion historica de los salarios, para de esta forma poder combinar estas 2 informaciones y hacer una comparativa. Estos datos se muestran tanto de forma numerica como gráfica, para los años y meses que se encuentran disponible en la pagina web del INDEC (desde año 2016 hasta la fecha) .

En total consta de 10 outputs(funciones) posibles. Algunas de ellas son gráficos, otros información y otras combina graficos e información. 

Dentro del codigo se realazan comentarios explicando lo que se hace en cada paso.

*Los outputs posibles son:*:punch:

*- **funciones.grafico_historico()**: muestra graficamente la evolución de los salarios y la inflacion, y tambien la compraracion historica de salarios e inflacion respecto a su media aritmetica.*

*- **funciones.grafbarras_ult_36_meses()**: muestra graficamente la evolución de los salarios y la inflacion de los ultimos 36 meses, mediante un grafico de barras, mostrando el pico del indice salarial y el pico del indice inflacionario. Asi mismo, sobre el mismo grafico se presenta un grafico de linea de cada una de las variables.*

*- **funciones.scatter_plot_inflacion()**: se muestra un scatter plot de la inflacion historica, donde el tamaño y el color de cada burbuja representa el valor del indice inflacionario. A mayor tamaño y color mas oscuro el indice inflacionario será mayor.
*
*- **funciones.whiskers_plot()**: grafico de whiskers_plot donde se observa la dispersion de cada una de las variables de estudio.*

*- **funciones.regresion_lineal()**: se muestra graficamente una recta de correlacion entre salarios e inflacion medido en %*

*- **funciones.inflacion_salarios_anual_filter()**: se solicita al usuario que se intruzca un mes y en base al mismo se realiza una grafica interanual comparativa de inflacion y salarios. Asi mismo se muestra la informacion en un DataFrame tanto a nivel del mes seleccionado como de forma interanual.*

*- **funciones.calculo_IPC_Salarios()**: se pide al usuario que introduzca AÑO-MES en formato formato: YYYY-MM, tanto fecha desde como fecha hasta. Y en base a las fechas introducidas se informa la inflacion y la variacion salarial durante el periodo seleccionado. Además se muestra la ganancia o pérdida de poder adquisitivo del salario en dicho período.*

*- **funciones.inflacion_puntual()**: se pide al usuario que introduzca AÑO-MES en formato formato: YYYY-MM y se informa como salida la inflacion de ese periodo seleccionado.
*
*- **funciones.calculo_inflacion_periodica()**: se pide al usuario que introduzca AÑO-MES en formato formato: YYYY-MM, tanto fecha desde como fecha hasta. Y en base a las fechas introducidas se informa la inflacion del periodo seleccionado.*

*- **funciones.forescast()**: se le solicita al usuario la cantidad de meses que desea y se realiza una proyeccion de la inflacion para el periodo seleccionado mediante la tecnica de Forescast.*

# **PROYECTO 2**:chart_with_upwards_trend:
## Proyecto Precios y Rendimientos de acciones, indices o criptomonedas:bar_chart:

El proyecto utiliza los datos de la plataforma yahoo finance para poder consultar datos históricos y actuales relacionados al mercado financiero, tanto local como internacional, además del mercado de las criptomonedas. 
En la linea 13 del código se debe seleccionar la abreviatura de la accion (critomoneda o indice) que se quiera consultar en base los datos de la plataforma Yahoo Finance. Puede seleccionarse una o varias acciones. El output del código, en primer lugar pide que se eleccione una fecha a partir de la cual se quiere consultar(puede ser 1D, 7D, 1M, 1A, YTD, 5A o editable a eleccion del usuario). Luego pide que seleccione hasta que fecha se quiere realizar la consulta. En caso de seleccionar en fecha desde alguna opcion que no sea editable, en la fecha hasta debe seleccionarse la opcion de "hoy". De lo contrario en caso de seleccionarse en fecha desde la opcion "editable", luego en fecha hasta tambien debe seleccionarse esta opcion para elegir hasta que dia se quiere hacer la consulta. Por último, el programa tiene 2 funciones principales que el usuario debe elegir:

*1.  **precios:** en este caso, la salida es un DataFrame con los precios de la accion o criptomoneda seleccionada junto con la media movil de 20 periodos y un gráfico donde se muestran ambas variables. En caso de seleccionarse mas de una accion o criptomoneda, la salida es un DataFrame con con los precios de las acciones o criptomonedas seleccionadas junto con la media movil de 20 periodos y una tercera columna con los rendimientos acumulados para la fecha seleccionada. En este último caso no se emite gráfico alguno.*

*2.  **rendimientos (rend):** en este caso, la salida consta de un DataFrame con el rendimiento de la/s accion/es o criptomoneda/s seleccionadas dentro del periodo elegido anteriormente y un gráfico mostrando la comparativa de rendimientos entre los activos elegidos.  *

# **PROYECTO 3**:bank:
## Proyecto evolución de Inflacion y Plazos fijos 30 días (base INDEC-data.triviasp.com.ar):rotating_light:

El proyecto busca poder obtener mediante el lenguaje de Python la evolucion historica de la inflacion y tambien la evolucion historica del rendimiento de los depósitos a plazo fijo en pesos 30 días del Banco Nación Argentina, para de esta forma poder combinar estas 2 informaciones y hacer una comparativa. Estos datos se muestran tanto de forma numerica como gráfica, para los años y meses que se encuentran disponible en la pagina web del INDEC (en este caso desde enero de 2017) .

En total consta de 3 outputs(funciones) posibles. Una de ellas es un gráfico, y las otras 2,  combinan graficos e información. 

Dentro del codigo se realazan comentarios explicando lo que se hace en cada paso.

*Los outputs posibles son:*:punch:

*- **funciones.inflacion_plazofijo_anual_filter()**: se solicita al usuario que elija un mes y se realiza un grafico interanual del mes elegido para los todos los años, mostrando la variación interanual de forma comparativa tanto del IPC como de la tasa de plazo fijo a 30 días. Además se muestra la información mediante un DataFrame en formato tabla, donde las 2 primeras columnas muestran los valores individuales del mes seleccionado para cada uno de los años y en las 2 columnas restantes se muestran los valores interanuales. *

*- **funciones.grafico_historico()**: muestra graficamente de forma comparativa la evolución histótica del IPC y la tasa de plazo fijo a 30 días.*

*- **funciones.calculo_IPC_PF()**: se pide al usuario que introduzca AÑO-MES en formato formato: YYYY-MM, tanto la fecha desde como la fecha hasta. Y en base a las fechas introducidas se informa la ivariación del IPC y la variacion de la tasa de plazo fijo a 30 días durante el periodo seleccionado, permitiendo de esta forma hacer la comparación entre las 2 variables.*

