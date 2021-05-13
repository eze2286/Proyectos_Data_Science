# 1 Librerias

import pandas as pd
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats
from fbprophet import Prophet

pd.options.display.float_format = '{:.2f}'.format

#######################################################FUNCIONES################################################################################

## Funciones combinadas de salario e inflacion para obtener los outputs deseados

 #A --> esta funcion me sirve de entrada a la funcion inflacion_anual_filter() para que salga un grafico al llamar a dicha funcion

class funciones():
    def grafico(x):
        if x["Interanual IPC"].min() > x["Interanual Salarios"].min():
            ejey = x["Interanual Salarios"].min() - 4.5
        else:
            ejey = x["Interanual IPC"].min() - 4.5
        plt.figure(figsize=(15, 8), facecolor="#CEF6E3")
        plt.style.use('fivethirtyeight')
        plt.plot(x["Fecha"], x["Interanual IPC"], label = "IPC_Interanual", marker= "o", markersize=5, linewidth=5)
        plt.plot(x["Fecha"], x["Interanual Salarios"], label = "Salarios_interanual",ls='--', marker= "*", c="red")        
        plt.fill_between(x["Fecha"], x["Interanual IPC"],x["Interanual Salarios"], alpha=0.1, color="blue")
        plt.text(x.Fecha.max(), ejey , "Fuente: www.indec.gob.ar", fontfamily="fantasy", fontsize=8)        
        plt.xlabel("Fecha",visible=False)
        plt.ylabel("Inflacion(%) vs Salarios(%)", fontsize = 12 )
        plt.title("Comparacion Interanual - IPC vs SALARIOS",color = "white", backgroundcolor="black", x=0.5, y=1.05)
        plt.xticks(rotation=25)
        plt.legend()
        plt.show()

 #B_1 -->esta funcion al llamarla realiza un grafico comparativo de la inflacion y los salarios en las fechas que estan cargadas en el archivo  
   
    def grafico_historico():        
        fig = plt.figure(figsize=(15, 8), facecolor="#E6E6E6")
        ax1, ax2, ax3 = fig.subplots(3, 1)        
        fig.subplots_adjust(hspace=0.5)    
        ax1.plot(inflacion_vs_salarios["Fecha"], inflacion_vs_salarios["Nivel general"], label = "IPC_Nivel_general", \
            marker= "o", markersize=5, linewidth=5) 
        ax1.plot(inflacion_vs_salarios["Fecha"], inflacion_vs_salarios["Var. Salarios"], label = "Var. Salarios",\
             marker= "*", c="red", linewidth=3)
        ax2.plot(inflacion_vs_salarios["Fecha"], inflacion_vs_salarios["Var. Salarios"], c="red")
        ax2.fill_between(inflacion_vs_salarios["Fecha"], inflacion_vs_salarios["Var. Salarios"],\
            inflacion_vs_salarios["Var. Salarios"].mean(), alpha=0.2, color="red")
        ax3.plot(inflacion_vs_salarios["Fecha"], inflacion_vs_salarios["Nivel general"], c="blue")
        ax3.fill_between(inflacion_vs_salarios["Fecha"], inflacion_vs_salarios["Nivel general"],\
            inflacion_vs_salarios["Nivel general"].mean(), alpha=0.2, color="blue")
        ax3.text(inflacion_vs_salarios.Fecha.max(),-1.3, "Fuente: www.indec.gob.ar", fontfamily="fantasy")        
        ax1.set_ylabel("Inflacion(%) vs Salarios(%)")
        ax2.set_ylabel(" Salarios(%) vs Promedio(%)")
        ax3.set_ylabel(" IPC(%) vs Promedio(%)")       
        ax1.set_title("Historico IPC vs SALARIOS", color = "white", backgroundcolor="gray", x=0.3, y=1.1)
        ax2.set_title("Variacion Salarios vs Promedio Salarios", color = "white", backgroundcolor="red",  y=1.05)
        ax3.set_title("Variacion IPC vs Promedio IPC", color = "white", backgroundcolor="blue",  y=1.05)       
        ax1.legend()    
        plt.show()

 #B_2 esta funcion al llamarla realiza un grafico de barras de la inflacion y los salarios de los ultimos 36 meses
     
    def grafbarras_ult_36_meses():
        fig = plt.figure(figsize=(20, 10), facecolor="#CEF6E3")
        fig.suptitle("Analisis Inflacionario-Salarial",y=0.95, x=0.5, fontsize=18, color="#0B0B61", fontfamily="serif")
        ax = fig.subplots()
        ax.set_facecolor("lightgray")
        barI = ax.bar(inflacion_vs_salarios["Fecha"].tail(36)-timedelta(days=5), inflacion_vs_salarios["Nivel general"].tail(36),\
             width=7, color="black", label="IPC", ec="k")
        barII = ax.bar(inflacion_vs_salarios["Fecha"].tail(36)+timedelta(days=5), inflacion_vs_salarios["Var. Salarios"].tail(36),\
             width=7,color="white", label="Salarios", ec="k")
        linea_ipc = ax.plot(inflacion_vs_salarios["Fecha"].tail(36), inflacion_vs_salarios["Nivel general"].tail(36), color = "black",\
             linewidth=3)
        linea_sal = ax.plot(inflacion_vs_salarios["Fecha"].tail(36), inflacion_vs_salarios["Var. Salarios"].tail(36), color = "white",\
             linewidth=3)
        ax.text(inflacion_vs_salarios.Fecha.tail(36)[inflacion_vs_salarios["Nivel general"].tail(36)== inflacion_vs_salarios["Nivel general"].tail(36).max()],\
        inflacion_vs_salarios["Nivel general"].tail(36).max() + 0.1, "Pico Inflacionario", fontsize=11, alpha=0.9) 
        ax.text(inflacion_vs_salarios.Fecha.tail(36)[inflacion_vs_salarios["Var. Salarios"].tail(36)== inflacion_vs_salarios["Var. Salarios"].tail(36).max()],\
        inflacion_vs_salarios["Var. Salarios"].tail(36).max() + 0.1, "Pico Salarial", fontsize=11, alpha=0.9)
        ax.text(inflacion_vs_salarios.Fecha.tail(36).max(),-1.3, "Fuente: www.indec.gob.ar", fontfamily="fantasy")       
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_title("IPC vs Salarios - últimos 36 meses", color = "white", backgroundcolor="black", y=0.95)
        ax.set_xlabel("Fecha", color = "white", backgroundcolor="black", labelpad = 12.0)
        ax.set_ylabel("Porcentaje mensual", color = "white", backgroundcolor="black", labelpad = 12.0)
        ax.set_ylim(-0.5,8)
        plt.xticks(rotation=25)
        plt.legend()
        plt.show()

#B_3 esta funcion al llamarla realiza un grafico de scatter plot de la inflacion historica ponderada por color y tmañano de la burbuja
    def scatter_plot_inflacion():
        fig = plt.figure(figsize=(18,8),facecolor="#CEF6E3")
        fig.suptitle("Inflacion histórica",y=0.95, x=0.5, fontsize=20, color="#0B0B61", fontfamily="serif")
        ax = fig.subplots()
        ax.scatter(Inflacion_historica.Fecha, Inflacion_historica["Nivel general"], s=Inflacion_historica["Nivel general"]*500,\
             c=Inflacion_historica["Nivel general"], cmap="Blues", alpha=0.7, linewidths=2.5)
        ax.set_ylim(1,7)
        ax.set_title("Ponderada por tamaño y color", color = "black", x=0.48, y=1, fontfamily="fantasy")
        ax.set_xlabel("Fecha", color = "white", backgroundcolor="black", labelpad = 12.0)
        ax.set_ylabel("Porcentaje mensual", color = "white", backgroundcolor="black", labelpad = 12.0)
        ax.text(inflacion_vs_salarios.Fecha.max(),0.4, "Fuente: www.indec.gob.ar", fontfamily="fantasy")
        for i in range(0,len(Inflacion_historica)):
            plt.annotate(Inflacion_historica["Nivel general"][i],(Inflacion_historica.Fecha[i], Inflacion_historica["Nivel general"][i]))
        plt.show()

#B_4 esta funcion al llamarla realiza un grafico de whiskers_plot de la inflacion y salarios historicos analizando la variabilidad de los datos
    def whiskers_plot():
        fig = plt.figure(figsize = (14, 9),facecolor="#2E2E2E")
        fig.suptitle("Whiskers_plot-Salarios vs Inflacion", fontsize=18, color="white")        
        ax1, ax2 = fig.subplots(1,2)
        ax1.set_facecolor("#ECE0F8")
        ax2.set_facecolor("#ECE0F8")
        ax1.boxplot(inflacion_vs_salarios["Nivel general"], manage_ticks = True)
        ax2.boxplot(inflacion_vs_salarios["Var. Salarios"])        
        ax2.text(1.3,-1.9, "Fuente: www.indec.gob.ar", fontfamily="fantasy", color="white")
        ax1.set_title("Variabilidad de datos", color = "white", x=0.5, y=1, fontfamily="serif")
        ax2.set_title("Variabilidad de datos", color = "white", x=0.5, y=1, fontfamily="serif")
        ax1.set_ylim(-1,7)
        ax2.set_ylim(-1,7)
        ax1.tick_params(axis='y', colors='white')
        ax1.tick_params(axis='x', colors='#2E2E2E')
        ax2.tick_params(axis='x', colors='#2E2E2E')
        ax2.tick_params(axis='y', colors='white')
        ax1.set_xlabel("IPC", color="white")
        ax2.set_xlabel("SALARIOS", color="white")
        ax1.set_ylabel("Porcentajes mensuales (%)", color="white")
        ax1.text(1,inflacion_vs_salarios["Nivel general"].max()+0.1, "Outlaier", fontfamily="fantasy", color = "darkblue", fontsize=13)
        ax2.text(1,inflacion_vs_salarios["Var. Salarios"].max()+0.1, "Outlaier", fontfamily="fantasy",color = "darkblue", fontsize=13)
        plt.show()

#B_5 esta funcion al llamarla realiza una recta de correlacion lineal entre la inflacion y salarios historicos

    def regresion_lineal():
        pendiente, intercepto, r_value, p_value, std_err = stats.linregress(inflacion_vs_salarios["Var. Salarios"], \
            inflacion_vs_salarios["Nivel general"])
        plt.figure(figsize=(18,8),facecolor="#CEF6E3")
        sns.regplot(data=inflacion_vs_salarios, x="Var. Salarios",  y = "Nivel general", scatter = True, label = "Relacion IPC-Salarios", \
            line_kws={"label": "y={0:.1f}x+{1:.1f}".format(pendiente, intercepto)})
        plt.text(inflacion_vs_salarios["Var. Salarios"].max(),inflacion_vs_salarios["Nivel general"].min()-0.9, "Fuente: www.indec.gob.ar", \
            fontfamily="fantasy", color="black")
        plt.xlim(inflacion_vs_salarios["Var. Salarios"].min()-0.2,inflacion_vs_salarios["Var. Salarios"].max()+0.2)
        plt.title("Recta de correlacion entre IPC y Salarios medido en %", color = "black", x=0.5, y=1, fontfamily="serif", fontsize=15)
        plt.legend(loc="upper right")
        plt.show()




 #C --> esta funcion le solicita un mes cualquiera al usuario y devuleve ipc y variacion salarial para el mes puntual en el año actual
     #  y los 3 anteriores como así tambien los interanuales del mes seleccionado respecto a los años previos. Tambien grafica este ultimo
     # resultado

    def inflacion_salarios_anual_filter():
        mes = int(input("Introduzca el numero de mes que desea: "))
        ipc_salarios_filtro = inflacion_vs_salarios[inflacion_vs_salarios["Mes"] == mes]
        ipc_salarios_filtro["Interanual Salarios"] = ipc_salarios_filtro.Indice.pct_change()*100
        ipc_salarios_filtro["Interanual IPC"] = ipc_salarios_filtro.Indice_Nivel_Gral.pct_change()*100    

        return ipc_salarios_filtro.loc[:,["Fecha", "Nivel general", "Var. Salarios", "Interanual Salarios", "Interanual IPC"]\
        ].fillna("Mes base").set_index("Fecha"), funciones.grafico(ipc_salarios_filtro)
        #return ipc_salarios_filtro.iloc[:,0:5]

 #D -->  esta funcion solicita un periodo unicial y uno final al usuario y devuelve mediante 2 frases, la inflacion y la variacion salarial 
       # entre estos 2 periodo seleccionados

    def calculo_IPC_Salarios():    
        fecha_pasada = str(input("Introduzca fecha inicial (formato: YYYY-MM): ")) + "-01"
        fecha_actual = str(input("Introduzca fecha final (formato: YYYY-MM): ")) + "-01"
        a = Inflacion_historica[Inflacion_historica["Fecha"]==pd.to_datetime(fecha_pasada)]["Indice_Nivel_Gral"].sum()
        b = Inflacion_historica[Inflacion_historica["Fecha"]==pd.to_datetime(fecha_actual)]["Indice_Nivel_Gral"].sum()
        c = inflacion_vs_salarios[inflacion_vs_salarios["Fecha"]==pd.to_datetime(fecha_pasada)]["Indice"].sum()
        d = inflacion_vs_salarios[inflacion_vs_salarios["Fecha"]==pd.to_datetime(fecha_actual)]["Indice"].sum()
        inflacion = round((b/a-1)*100,2)
        salarios =  round((d/c-1)*100,2)
        poder_adquisitvo =  abs(round((1-((1+salarios/100)/(1+inflacion/100)))*100,2))
        frase = "La inflacion durante el periodo" + "(" + fecha_actual + " - " + fecha_pasada +")" \
        + " fue: " + "% " + str(inflacion) + "\nLa variacion salarial durante el periodo" + "(" + \
        fecha_actual + " - " + fecha_pasada +")" + " fue: " + "% " + str(salarios)
        frase2 = ""
        if inflacion > salarios:
            frase2 = f"\nLa pérdida de poder adquisitvo del salario durante el periodo ({fecha_actual} - {fecha_pasada})"\
            f" fue de % {poder_adquisitvo}"
        else:
            frase2 = f"\nLa ganancia de poder adquisitvo del salario durante el periodo ({fecha_actual} - {fecha_pasada})"\
            f" fue de % {poder_adquisitvo}"
        
        return frase + frase2  

#E -->  esta funcion me calcula la inflacion de un año-mes puntual seleccionado

    def inflacion_puntual():
        año_mes = pd.to_datetime(str(input("Introduzca el periodo que desea consultar (formato: YYYY-MM): ")) + "-01")
        inflacion = Inflacion_historica[Inflacion_historica["Fecha"]== año_mes]["Nivel general"].sum()
        frase = "La inflacion del periodo seleccionado es: " + str(inflacion) + " %"
        return frase

#F -->  esta funcion me calcula la inflacion entre 2 periodos seleccionados por el usuario
##      La transformo a string para que se acople con la frase

    def calculo_inflacion_periodica():    
        fecha_pasada = str(input("Introduzca fecha inicial (formato: YYYY-MM): ")) + "-01"
        fecha_actual = str(input("Introduzca fecha final (formato: YYYY-MM): ")) + "-01"
        a = Inflacion_historica[Inflacion_historica["Fecha"]==pd.to_datetime(fecha_pasada)]["Indice_Nivel_Gral"].sum()
        b = Inflacion_historica[Inflacion_historica["Fecha"]==pd.to_datetime(fecha_actual)]["Indice_Nivel_Gral"].sum()
        inflacion = round((b/a-1)*100,2)
        frase = "La inflacion durante el periodo" + "(" + fecha_pasada[0:-3] + " - " + fecha_actual[0:-3] +")"\
        + " fue: " + "% " + str(inflacion)
        return frase

#G -->  esta funcion le ingreso un mes que el usuario quiera y me muestra la inflacion de ese mes para el año actual y los 3 anteriores
## Ademas me muestra la infalcion interanual de ese mes selecionado respecto a los 3 años anteriores
## tambien lo muestra graficamente que es lo que se muestra primero al ejecutar el codigo.
## Primero creo grafico para que meterlo en la siguiente funcion y que me retorne un data frame y un grafico
## con parametros ingresados por el usuario

    def grafico_inflacion(x):                
        fig = plt.figure(figsize=(20, 8), facecolor="#2E2E2E")
        fig.suptitle("Inflacion_Argentina_base 2017", color = "white", x=0.5, y=0.97, fontfamily="serif", fontsize=18)
        ax = fig.subplots()                      
        ax.plot(x["Fecha"], x["IPC_Interanual"], label = "IPC_Interanual", marker= "s", markersize=5, linewidth=3, c="red")                                   
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Inflacion(%)")        
        ax.tick_params(axis='y', colors='white')
        ax.tick_params(axis='x', colors='white')        
        ax.set_xlabel("IPC", color="white")        
        ax.set_ylabel("Porcentajes mensuales (%)", color="white")        
        ax.set_title("Fuente: www.indec.gob.ar", color = "white", x=0.5, y=1.00, fontfamily="serif", fontsize=10)
        ax.grid(b=True,  c="gray", linestyle='-', linewidth=1, alpha=0.8)              
        plt.legend()
        plt.show()

    def inflacion_anual_filter():
        mes = int(input("Introduzca el numero de mes que desea: "))
        inflacion_mes_filtrada = Inflacion_historica[Inflacion_historica["Mes"] == mes]
        inflacion_mes_filtrada["IPC_Interanual"] = inflacion_mes_filtrada["Indice_Nivel_Gral"].pct_change()*100    
        inflacion_mes_filtrada.rename(columns={"Nivel general": "IPC_Mensual"}, inplace=True)
        return inflacion_mes_filtrada.loc[:,["Fecha","IPC_Mensual", "IPC_Interanual"]].fillna("base").set_index("Fecha"),\
        funciones.grafico_inflacion(inflacion_mes_filtrada)

#H -->  esta funcion permite obtener una prevision para la inflacion para un periodo a eleccion del usuario

    def forescast():
        periodo = input("Ingrese la cantidad de meses que desea para proyectar la inflacion: ")
        Inflacion_historica_subdataset = Inflacion_historica.filter(["Fecha", "Nivel general"], axis=1)
        jh = Inflacion_historica_subdataset.rename(columns={'Fecha': 'ds', 'Nivel general': 'y'})
        jh_model = Prophet(interval_width=0.95)
        jh_model.fit(jh)
        jh_forecast = jh_model.make_future_dataframe(periods=int(periodo), freq='MS') #freq = "D" (Día) / "MS" (Mes) 
        jh_forecast = jh_model.predict(jh_forecast)
        #plt.figure(figsize=(18, 6))
        jh_model.plot(jh_forecast, xlabel = 'Fecha', ylabel = 'Inflacion', figsize=(18, 8))
        plt.title('Prevision de Inflacion para '+ str(periodo)+" meses",x=0.5, y=0.99)
        plt.show()

####################################################### INFLACION ##############################################################################

# 2 Pagina Web

 ## Automatizo el nombre del archivo para que si no está el mes en curso, me baje la última version del archivo vigente

 ##nombre_archivo = "sh_ipc_"+"0"+str(datetime.now().month)+"_"+ str(datetime.now().year)[2:4] + ".xls"

def nombre_archivo():
    if datetime.now().month < 10:
        nombre_archivo = "sh_ipc_"+"0"+str(datetime.now().month)+"_"+ str(datetime.now().year)[2:4] + ".xls"
    else:
        nombre_archivo = "sh_ipc_"+str(datetime.now().month)+"_"+ str(datetime.now().year)[2:4] + ".xls"
    return nombre_archivo
    
def nombre_archivo_except():
    if datetime.now().month-1 == 0:
        nombre_archivo_ex = "sh_ipc_"+"12"+"_"+ str(datetime.now().year-1)[2:4] + ".xls"
    elif 0 < datetime.now().month-1 < 10:
        nombre_archivo_ex = "sh_ipc_"+"0"+str(datetime.now().month-1)+"_" + str(datetime.now().year)[2:4] + ".xls"    
    else:
        nombre_archivo_ex = "sh_ipc_"+str(datetime.now().month-1)+"_"+ str(datetime.now().year)[2:4] + ".xls"
    return nombre_archivo_ex

    # 3  Lectura de archivos desde la web
 ## Intento leer el último archivo que está cargado en la web del INDEC
 ## Si me tira error porque no está el mes vigente le pido el último que esté disponible

url = "https://www.indec.gob.ar/ftp/cuadros/economia/"+nombre_archivo()
url2 = "https://www.indec.gob.ar/ftp/cuadros/economia/"+nombre_archivo_except()

try:
    df_indec = pd.read_excel(url, skiprows=5, parse_dates = True)
    df_indec_indices = pd.read_excel(url, skiprows=5, parse_dates = True, sheet_name = "Índices IPC Cobertura Nacional")
    
except:    
    df_indec = pd.read_excel(url2, skiprows=5, parse_dates = True)
    df_indec_indices = pd.read_excel(url2, skiprows=5, parse_dates = True, sheet_name = "Índices IPC Cobertura Nacional")

# 4  Elimino NaN

df_indec_indices = df_indec_indices.dropna()
df_indec = df_indec.dropna()

# 5  Estructuro el DataFrame

ipc_nacional = df_indec.iloc[:18]
ipc_nacional_indices = df_indec_indices.iloc[:18]
lista = {3:"Nivel general", 4:"Alimentos y bebidas no alcohólicas", 5: "Bebidas alcohólicas y tabaco", \
    6: "Prendas de vestir y calzado", 7: "Vivienda. agua. electricidad y otros combustibles", 8:"Equipamiento y mantenimiento del hogar", \
    9:"Salud", 10:"Transporte", 11:"Comunicación", 12:"Recreación y cultura", 13:"Educación", 14:"Restaurantes y hoteles",\
    15:"Bienes y servicios varios",18:"Estacional", 19:"Núcleo" , 20:"Regulados", 23:"Bienes", 24:"Servicios"}
ipc_T = ipc_nacional.T
ipc_T_indices = ipc_nacional_indices.T
ipc_T = ipc_T.rename(columns=lista)
ipc_T_indices = ipc_T_indices.rename(columns=lista)
ipc_T = ipc_T.drop('Total nacional')
ipc_T_indices = ipc_T_indices.drop('Total nacional')

# 6  Hago casting y acomodo indices

ipc_T = ipc_T.reset_index()
ipc_T_indices = ipc_T_indices.reset_index()
ipc_T = ipc_T.convert_dtypes()
ipc_T_indices = ipc_T_indices.convert_dtypes()
ipc_T = ipc_T.rename(columns={"index":"Fecha"})
ipc_T_indices = ipc_T_indices.rename(columns={"index":"Fecha"})

# 7  Consulto info de columnas

#ipc_T.info()
#ipc_T_indices.info()

# 8  Armo un Sub_dataset para luego hacer merge

nivel_general_indices = ipc_T_indices[["Fecha","Nivel general"]]

# 8.1  Cambio nombre del sub_dataset para que no se repita con el del otro dataframe

nivel_general_indices = nivel_general_indices.rename(columns={"Nivel general": "Indice_Nivel_Gral"})

# 9  Prueba Final
## con la función .T invierto el DataFrame
## Hago un merge para obtener los datos finales

Inflacion_historica = ipc_T.merge(nivel_general_indices, how="inner", on="Fecha")


# 10  Guardo excel en carpeta

#Inflacion_historica.to_excel(r'D:\Desktop\Todas mis cosas\Cursos\EXCEL\Data Science-Basico\Inflacion automatizada\IPC_Final.xlsx')

# 11  Modifico el dataset para filtrarlo por mes de forma interanual 

Inflacion_historica["Mes"] = Inflacion_historica["Fecha"].dt.month

#---------------------------------------------------------------------------------------------

##############################################################SALARIOS###########################################################################
# 2 Pagina Web

 ## Automatizo el nombre del archivo para que si no está el mes en curso, me baje la última version del archivo vigente
 ## url = https://www.indec.gob.ar/ftp/cuadros/sociedad/variaciones_salarios_01_21.xls

def nombre_archivo_salarios():
    if datetime.now().month < 10:
        nombre_archivo = "variaciones_salarios_"+"0"+str(datetime.now().month)+"_"+ str(datetime.now().year)[2:4] + ".xls"
    else:
        nombre_archivo = "variaciones_salarios_"+str(datetime.now().month)+"_"+ str(datetime.now().year)[2:4] + ".xls"
    return nombre_archivo
    
def nombre_archivo_except_salarios():
    if str(datetime.now().month-1) == "0":
        nombre_archivo_ex = "variaciones_salarios_"+"12"+"_"+ str(datetime.now().year-1)[2:4] + ".xls"
    elif 0 < datetime.now().month-1 < 10:
        nombre_archivo_ex = "variaciones_salarios_"+"0"+str(datetime.now().month-1) + "_"+ str(datetime.now().year)[2:4] + ".xls"
    else:
        nombre_archivo_ex = "variaciones_salarios_" + str(datetime.now().month-1) + "_"+ str(datetime.now().year)[2:4] + ".xls"
    return nombre_archivo_ex

    # 3  Lectura de archivos desde la web
 ## Intento leer el último archivo que está cargado en la web del INDEC
 ## Si me tira error porque no está el mes vigente le pido el último que esté disponible

url = "https://www.indec.gob.ar/ftp/cuadros/sociedad/"+nombre_archivo_salarios()
url2 = "https://www.indec.gob.ar/ftp/cuadros/sociedad/"+nombre_archivo_except_salarios()

#print(url)
#print(url2)

columns = ["Año", "Mes", "Var. Salarios", "Indice"]

try:
    salarios = pd.read_excel(url, skiprows=7, usecols=[0,1,10,11], names=columns)    
    
except:    
    salarios = pd.read_excel(url2, skiprows=7, usecols=[0,1,10,11], names=columns)

## 4 Hago preprocesado de datos

salarios["Año"] = salarios.Año.fillna(method="ffill")

salarios = salarios.dropna()
salarios["Año"] = salarios.Año.str.replace("*","").fillna("2015")
salarios = salarios.iloc[12:]

Meses_nombre = ["Enero ", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
Meses_numero = ["1","2","3","4","5","6","7","8","9","10","11","12"]
meses = dict(zip(Meses_nombre, Meses_numero))

salarios["Mes"] = salarios.Mes.replace(meses)

salarios["Año_Mes"] = salarios["Año"] + "-" + salarios["Mes"] + "-" + "01"

salarios = salarios.filter(["Año_Mes", "Var. Salarios", "Indice"])

salarios.rename(columns={"Año_Mes":"Fecha"}, inplace=True)
salarios = salarios.convert_dtypes()
salarios["Fecha"] = pd.to_datetime(salarios["Fecha"])
salarios["Mes"] = salarios["Fecha"].dt.month

# 5  Hago casting 
salarios.loc[12, "Var. Salarios"]=0
salarios = salarios.convert_dtypes()

#print(salarios.tail())

inflacion_vs_salarios = Inflacion_historica[["Fecha", "Nivel general", "Indice_Nivel_Gral"]].merge(salarios, how="inner", on="Fecha")

#print(inflacion_vs_salarios.tail(5))

#######################################################OUTPUTS_POSIBLES#########################################################################

#print(funciones.grafico_historico()) 
#print(funciones.grafbarras_ult_36_meses())
#print(funciones.scatter_plot_inflacion())
#print(funciones.whiskers_plot())
#print(funciones.regresion_lineal())
#print(funciones.inflacion_salarios_anual_filter())
#print(funciones.calculo_IPC_Salarios())
#print(funciones.inflacion_puntual())
#print(funciones.calculo_inflacion_periodica())
#print(funciones.forescast())
