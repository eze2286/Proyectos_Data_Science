import pandas as pd
import datetime

pd.options.display.float_format = '{:.4f}'.format
pd.options.display.max_columns = 8


#fecha_desde = pd.to_datetime(str(input("Introduzca fecha inicial (formato: YYYY-MM-DD): ")))
#fecha_hasta = pd.to_datetime(str(input("Introduzca fecha final (formato: YYYY-MM-DD): ")))



consulta_acciones = ["BTC-USD", "ETH-USD", "ADA-USD"]

def acciones_urls():
    lista_urls = []
    for accion in consulta_acciones:
        accion = "https://query1.finance.yahoo.com/v7/finance/download/"+accion+"?period1=1451606400&period2=1796915743&interval=1d&events=history&includeAdjustedClose=true/"+accion+".csv"
        lista_urls.append(accion)
    
    return(lista_urls)

def parseo_tablas():
    acciones = []            
    for url in urls:               
        historicos = pd.read_csv(url)
        acciones.append(historicos)
        
    return acciones

## TRANSFORMO LOS DATAFRAMES
def transformacion_datos(x):
    acciones_df_final = []
    indice_accion = 0
    for accion in df_acciones:            
        accion.Date = pd.to_datetime(accion.Date)
        accion = accion.convert_dtypes()
        accion.columns = ["Fecha","Apertura", "Maximo", "Minimo", "Cierre", "Cierre_Aj_"+str(consulta_acciones[indice_accion]), "Volumen"]
        if x == "SMA_20":
            accion["SMA_20_"+str(consulta_acciones[indice_accion])] = accion["Cierre_Aj_"+str(consulta_acciones[indice_accion])].rolling(20).mean()
            accion = accion.set_index("Fecha")
            accion["Cierre_Aj_"+str(consulta_acciones[indice_accion])] = accion["Cierre_Aj_"+str(consulta_acciones[indice_accion])].astype(float)
            accion = accion[(accion.index>=fecha_desde)&(accion.index<=fecha_hasta)]
            accion = accion.iloc[:,[4,6]]
            accion = accion.dropna()
            acciones_df_final.append(accion)
            indice_accion+=1
        else:
            accion = accion.set_index("Fecha")
            accion["Cierre_Aj_"+str(consulta_acciones[indice_accion])] = accion["Cierre_Aj_"+str(consulta_acciones[indice_accion])].astype(float)
            accion = accion[(accion.index>=fecha_desde)&(accion.index<=fecha_hasta)]
            accion["Rendimiento_"+str(consulta_acciones[indice_accion])] = ((1 + (accion["Cierre_Aj_"+str(consulta_acciones[indice_accion])].pct_change())).cumprod()-1)*100
            accion = accion.iloc[:,[4,6]]
            accion = accion.fillna(0)
            acciones_df_final.append(accion)        
            indice_accion+=1
    return acciones_df_final

## CONCATENO LOS DATAFRAMES OBTENIDOS EN EL PUNTO ANTERIOR Y QUE ESTAN ALMACENADOS EN UNA LISTA

def concatenado_acciones():    
   resumen_acciones = pd.DataFrame()
   indice_accion = 0
   if len(consulta_acciones)==1:       
       for df in df_acciones_final:        
           resumen_acciones = pd.concat([resumen_acciones, df],join='outer', axis=1)
           data = resumen_acciones.plot(figsize=(18,8),\
           grid=True,title="Precios y Media movil de 20 ruedas "+ str(fecha_desde)[0:10]  + " y " +str(fecha_hasta)[0:10])
           return resumen_acciones.dropna(), data
   else:
       for df in df_acciones_final:
           resumen_acciones = pd.concat([resumen_acciones, df],join='outer', axis=1)
           resumen_acciones["Rendimiento_"+str(consulta_acciones[indice_accion])] = \
           ((1 + (resumen_acciones["Cierre_Aj_"+str(consulta_acciones[indice_accion])].pct_change())).cumprod()-1)*100
           resumen_acciones = resumen_acciones.fillna(0)
           indice_accion += 1
   return resumen_acciones
    #resumen_acciones = pd.DataFrame()
    #for df in df_acciones_final:
        #resumen_acciones = pd.concat([resumen_acciones, df],join='outer', axis=1)
    
    #if len(consulta_acciones)==1:
        #data = resumen_acciones.plot(figsize=(18,8),grid=True,title="Precios y Media movil de 20 ruedas entre "+ str(fecha_desde)[0:10]  + " y " +str(fecha_hasta)[0:10], linewidth=2)
        #return resumen_acciones.dropna(), data
    #else:
        #return resumen_acciones.dropna()

## CONCATENO LOS DATAFRAMES OBTENIDOS EN EL PUNTO ANTERIOR Y QUE ESTAN ALMACENADOS EN UNA LISTA

def concatenado_acciones_rendimientos():
    resumen_rendimientos = pd.DataFrame()
    for df in df_rendimientos:
        resumen_rendimientos = pd.concat([resumen_rendimientos, df],join='outer', axis=1)
    
    return resumen_rendimientos.dropna()

## OBTENGO UN SUBDATASET DE RENDIMIENTOS UNICAMENTE

def rendimientos():
    #plt.figure(figsize=(18,8))
    subdataset_columns = []
    for x in range(len(resumen_rendimientos.columns)):
        if x%2!=0:
            subdataset_columns.append(x)
    data = resumen_rendimientos.iloc[:,subdataset_columns].dropna().plot(figsize=(18,8), ylabel="Rendimiento(%)",\
    grid=True, title="Rendimientos acumulados entre " + str(fecha_desde)[0:10]  + " y " +str(fecha_hasta)[0:10], linewidth=2)
    return resumen_rendimientos.iloc[:,subdataset_columns].dropna(), data

def fecha_inicial():
    fecha_inicial=0
    seleccion_periodo = str(input("Introduzca el perido que quiere consultar entre las siguientes opciones: \ 1D, 7D, 1M, 1A, YTD, 5A o editable: "))
    if seleccion_periodo=="1D":
        if datetime.datetime.today().weekday()==5:
            fecha_inicial = datetime.datetime.today()-datetime.timedelta(days=3)
        elif (datetime.datetime.today().weekday()==6)|(datetime.datetime.today().weekday()==0):
            fecha_inicial = datetime.datetime.today()-datetime.timedelta(days=5)
        else:
            fecha_inicial = datetime.datetime.today()-datetime.timedelta(days=2)
    elif seleccion_periodo=="7D":
        fecha_inicial = datetime.datetime.today()-datetime.timedelta(days=8)
    elif seleccion_periodo=="1M":
        fecha_inicial = datetime.datetime.today()-datetime.timedelta(days=30)
    elif seleccion_periodo=="1A":
        fecha_inicial = datetime.datetime.today()-datetime.timedelta(days=367)
    elif seleccion_periodo=="YTD":
        fecha_inicial = datetime.datetime.strptime(str(datetime.datetime.today().year-1) + "-"+ "12" + "-" + "31", '%Y-%m-%d')
    elif seleccion_periodo=="5A":
        fecha_inicial = datetime.datetime.today()-datetime.timedelta(days=1830)
    else:
        fecha_inicial = pd.to_datetime(str(input("Introduzca fecha inicial (formato: YYYY-MM-DD): ")))
    return fecha_inicial

def fecha_final():
    fecha_final=0
    seleccion_periodo = str(input("Introduzca el perido que quiere consultar entre las siguientes opciones: hoy o editable: "))
    if seleccion_periodo=="hoy":
        fecha_final = datetime.datetime.today()      
    else:
        fecha_final = pd.to_datetime(str(input("Introduzca fecha final (formato: YYYY-MM-DD): ")))
    return fecha_final

fecha_desde = fecha_inicial()
fecha_hasta = fecha_final()
urls = acciones_urls()
df_acciones = parseo_tablas()
df_acciones_final = transformacion_datos("SMA_20")
df_rendimientos = transformacion_datos("rendimientos")
resumen_rendimientos = concatenado_acciones_rendimientos()


## OUTPUTS POSIBLES
def eleccion ():
    resultado = input(str("Seleccione que operacion quiere visualizar: precios o rend: "))
    if resultado == "precios":
        print(concatenado_acciones())
    elif resultado == "rend":
        print(rendimientos())
    else:
        print("eleccion incorrecta")
        
#print(eleccion ())        
#print(rendimientos())
#print(concatenado_acciones())


