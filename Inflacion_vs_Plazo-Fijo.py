import pandas as pd
import requests
from datetime import datetime
from matplotlib import pyplot as plt

pd.options.display.float_format = '{:.1f}'.format

class funciones():
    def grafico_historico():
        eje_x = IPC_vs_PF_final.reset_index()[["Año", "Mes"]]
        eje_x["Año-Mes"] = eje_x["Año"].map(str) + "-" + eje_x["Mes"].map(str)        
        plt.figure(figsize=(18,7) , facecolor="#CEF6E3")
        plt.style.use('seaborn-darkgrid')
        plt.plot(eje_x["Año-Mes"], IPC_vs_PF_final["IPC_mensual"], label = "IPC_mensual", marker= "o", markersize=5, linewidth=2)
        plt.plot(eje_x["Año-Mes"], IPC_vs_PF_final["Tasa_Plazo_Fijo"], label = "Plazo_Fijo_mensual",ls='--', marker= "*", c="red")        
        plt.xlabel("Fecha",visible=True)
        plt.ylabel("Inflacion(%) vs Plazo_Fijo(%)", fontsize = 12)
        plt.title("Comparacion IPC vs Plazo_fijo a 30 días\n\nFuente: INDEC y Banco Nacion Argentina",\
        color = "black", backgroundcolor="grey", x=0.5, y=1.05)
        plt.xticks(rotation=90)
        plt.legend()
        plt.show()

    def grafico(x):
            x.reset_index()
            x["Fecha"] = x["Año"].map(str) + "-" + x["Mes"].map(str)
            
            if x["Interanual IPC"].min() > x["Interanual P.Fijo"].min():
                ejey = x["Interanual P.Fijo"].min() - 5.8
            else:
                ejey = x["Interanual IPC"].min() - 5.8
            plt.figure(figsize=(15, 8), facecolor="#CEF6E3")
            plt.style.use('fivethirtyeight')
            plt.plot(x["Fecha"], x["Interanual IPC"], label = "Interanual IPC", marker= "o", markersize=5, linewidth=5)
            plt.plot(x["Fecha"], x["Interanual P.Fijo"], label = "Interanual P.Fijo",ls='--', marker= "*", c="red")        
            plt.fill_between(x["Fecha"], x["Interanual IPC"],x["Interanual P.Fijo"], alpha=0.1, color="blue")
            plt.text(x.Fecha.max(), ejey , "Fuente: www.indec.gob.ar y \nBanco Nacion Argentina", fontfamily="fantasy", fontsize=8)        
            plt.xlabel("Fecha",visible=False)
            plt.ylabel("Inflacion(%) vs Plazo Fijo(%)", fontsize = 12 )
            plt.title("Comparacion Interanual - IPC vs PLAZO FIJO", color = "white", backgroundcolor="black", x=0.5, y=1.05)
            plt.xticks(rotation=25)
            plt.legend()
            plt.show()

    def inflacion_plazofijo_anual_filter():
            df1 = IPC_vs_PF_final.reset_index()
            mes = int(input("Introduzca el numero de mes que desea: "))
            ipc_PF_filtro = df1[df1["Mes"] == mes]
            ipc_PF_filtro["Interanual IPC"] = ipc_PF_filtro.Indice_IPC.pct_change()*100
            ipc_PF_filtro["Interanual P.Fijo"] = ipc_PF_filtro.Indice_Plazo_Fijo.pct_change()*100    

            return ipc_PF_filtro.loc[:,["Año", "Mes", "IPC_mensual", "Tasa_Plazo_Fijo", "Interanual IPC", "Interanual P.Fijo"]].\
            set_index(["Año", "Mes"]).fillna("Mes base"), funciones.grafico(ipc_PF_filtro)

    def calculo_IPC_PF():
            df_IPC_PF= IPC_vs_PF_final.reset_index()
            df_IPC_PF["Fecha"] = df_IPC_PF["Año"].astype(str) + "-" + df_IPC_PF["Mes"].astype(str)
            df_IPC_PF["Fecha"] = pd.to_datetime(df_IPC_PF["Fecha"])
            fecha_pasada = str(input("Introduzca fecha inicial (formato: YYYY-MM): "))+ "-01"
            fecha_actual = str(input("Introduzca fecha final (formato: YYYY-MM): "))+ "-01"
            a = df_IPC_PF[df_IPC_PF["Fecha"]==pd.to_datetime(fecha_pasada)]["Indice_IPC"].sum()
            b = df_IPC_PF[df_IPC_PF["Fecha"]==pd.to_datetime(fecha_actual)]["Indice_IPC"].sum()
            c = df_IPC_PF[df_IPC_PF["Fecha"]==pd.to_datetime(fecha_pasada)]["Indice_Plazo_Fijo"].sum()
            d = df_IPC_PF[df_IPC_PF["Fecha"]==pd.to_datetime(fecha_actual)]["Indice_Plazo_Fijo"].sum()
            inflacion = round((b/a-1)*100,2)
            plazo_fijo =  round((d/c-1)*100,2)
            poder_adquisitvo =  round((1-((1+plazo_fijo/100)/(1+inflacion/100)))*100,2)
            frase = "La inflacion durante el periodo" + "(" + fecha_actual + " - " + fecha_pasada +")" \
            + " fue: " + "% " + str(inflacion) + "\nLa variacion de la tasa de plazo fijo a 30 dias durante el periodo" + "(" + \
            fecha_actual + " - " + fecha_pasada +")" + " fue: " + "% " + str(plazo_fijo)
            frase2 = ""
            if inflacion > plazo_fijo:
                frase2 = f"\nLa pérdida del plazo fijo frente a la inflacion durante el periodo ({fecha_actual} - {fecha_pasada})"\
                f" fue de % {poder_adquisitvo}"
            else:
                frase2 = f"\nLa ganancias del plazo fijo frente a la inflacion durante el periodo ({fecha_actual} - {fecha_pasada})"\
                f" fue de % {poder_adquisitvo}"
            return frase + frase2


# 1) Armado del DataFrame del historico de Plazo Fijo desde 01-2017 hasta la fecha.

url_trivia='http://data.triviasp.com.ar/files/parte2/COE460.HTM'
r_trivia = requests.get(url_trivia)
df_trivia = pd.read_html(r_trivia.text)
tasas_historicas_pf = df_trivia[2]
tasas_historicas_pf.drop(tasas_historicas_pf.index[0], inplace=True)
tasas_historicas_pf.columns = ["Fecha", "TNA_%", "TEM_%"]
tasas_historicas_pf["TNA_%"]=tasas_historicas_pf["TNA_%"].astype(float)
tasas_historicas_pf["TNA_%"] = tasas_historicas_pf["TNA_%"]/100
tasas_historicas_pf["TEM_%"] = (tasas_historicas_pf["TNA_%"])/(365/30)
tasas_historicas_pf.Fecha = pd.to_datetime(tasas_historicas_pf.Fecha)
tasas_historicas_pf["Mes"] = tasas_historicas_pf["Fecha"].dt.month
tasas_historicas_pf["Año"] = tasas_historicas_pf["Fecha"].dt.year
tasas_historicas_pf_desde_2016 = tasas_historicas_pf[tasas_historicas_pf.Fecha > "2016-12-01"]
plazo_fijo_filtro = tasas_historicas_pf_desde_2016.groupby(["Año", "Mes"])[["TEM_%"]].agg("mean")

# 2) Armado del DataFrame IPC en base a informacion disponible de INDEC desde 01-2017

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

    #   Lectura de archivos desde la web
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

#   Elimino NaN

df_indec_indices = df_indec_indices.dropna()
df_indec = df_indec.dropna()

#   Estructuro el DataFrame

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

#   Hago casting y acomodo indices

ipc_T = ipc_T.reset_index()
ipc_T_indices = ipc_T_indices.reset_index()
ipc_T = ipc_T.convert_dtypes()
ipc_T_indices = ipc_T_indices.convert_dtypes()
ipc_T = ipc_T.rename(columns={"index":"Fecha"})
ipc_T_indices = ipc_T_indices.rename(columns={"index":"Fecha"})

#   Consulto info de columnas

#ipc_T.info()
#ipc_T_indices.info()

#   Armo un Sub_dataset para luego hacer merge

nivel_general_indices = ipc_T_indices[["Fecha","Nivel general"]]

###  Cambio nombre del sub_dataset para que no se repita con el del otro dataframe

nivel_general_indices = nivel_general_indices.rename(columns={"Nivel general": "Indice_Nivel_Gral"})

#   Prueba Final
## con la función .T invierto el DataFrame
## Hago un merge para obtener los datos finales

Inflacion_historica = ipc_T.merge(nivel_general_indices, how="inner", on="Fecha")

# 10  Modifico el dataset para filtrarlo por mes de forma interanual
Inflacion_historica["Mes"] = Inflacion_historica["Fecha"].dt.month
Inflacion_historica_depurado = Inflacion_historica[["Fecha", "Nivel general", "Mes"]]
Inflacion_historica_depurado["Año"] = Inflacion_historica_depurado.Fecha.dt.year
Inflacion_historica_final = Inflacion_historica_depurado.groupby(["Año", "Mes"]).mean()

# 3) Armado de DataFrame combinado

IPC_vs_PF = Inflacion_historica_final.merge(plazo_fijo_filtro, how="outer", left_index=True, right_index=True).fillna(method="ffill").fillna(method="bfill")
IPC_vs_PF_final = IPC_vs_PF[["Nivel general", "TEM_%"]]
IPC_vs_PF_final.fillna(0, inplace=True)
IPC_vs_PF_final = IPC_vs_PF_final.rename(columns={"TEM_%":"Tasa_Plazo_Fijo", "Nivel general":"IPC_mensual"})
IPC_vs_PF_final["Indice_IPC"] = (IPC_vs_PF_final["IPC_mensual"]/100 + 1).cumprod()
IPC_vs_PF_final["Indice_Plazo_Fijo"] = (IPC_vs_PF_final["Tasa_Plazo_Fijo"]/100 + 1).cumprod()

 


#print(funciones.inflacion_plazofijo_anual_filter())
print(funciones.grafico_historico())
#print(funciones.calculo_IPC_PF())