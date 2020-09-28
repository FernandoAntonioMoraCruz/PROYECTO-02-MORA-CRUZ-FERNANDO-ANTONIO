#Se importa la librería CSV para trabajar con los datos de un excel
import csv
#Se importa matplotlib para realizar las gráficas
import matplotlib.pyplot as plt

#Se define un diccionario que contendrá los resultados condensados sobre las exportaciones y otro para las importaciones
rutas_exportaciones, rutas_importaciones = {}, {}
#Se define un diccionario que contendrá información sobre el tranporte utilizado en las exportaciones y otro para las importaciones
transportes_exportaciones, transportes_importaciones = {}, {}

#Se define una función que calcula la frecuencia de uso de la ruta y el total de ingresos generados por la misma
def Analisis_Frecuencia_IngresosTotales (diccionario):
    #Se agrega la llave con el nombre de la ruta al diccionario si no se encuentra ya dentro de él
    if ruta not in diccionario.keys():
        #Se agregan como valores la primer frecuencia y el primer ingreso asociado
        diccionario[ruta] = {'frecuencia':1,
                             'ingresos':int(linea['total_value'])
                             }

    #Posteriormente, para las rutas repetidas, se realiza la suma acumulada de los nuevos ingresos y se aumenta la frecuencia en 1
    else:
        diccionario[ruta]['frecuencia'] = diccionario[ruta].get('frecuencia') + 1
        diccionario[ruta]['ingresos'] = diccionario[ruta].get('ingresos') + int(linea['total_value'])

#Se define una función que calcula la frecuencia de uso y los ingresos asosciados a cada método de transporte        
def Analisis_Transportes (diccionario):
    transporte = linea['transport_mode']
    #Se agrega la llave con el nombre del transporte al diccionario si no se encuentra ya dentro de él
    if transporte not in diccionario.keys():
        #Se agregan como valores la primer frecuencia y el primer ingreso asociado
        diccionario[transporte] = {'frecuencia':1,
                                   'ingresos':int(linea['total_value'])
                                   }
    #Posteriormente, para los transportes repetidos, se realiza la suma acumulada de los nuevos ingresos y se aumenta la frecuencia en 1
    else:
        diccionario[transporte]['frecuencia'] = diccionario[transporte].get('frecuencia') + 1
        diccionario[transporte]['ingresos'] = diccionario[transporte].get('ingresos') + int(linea['total_value'])
    
        
#Se define una función que determina las rutas con mayores ingresos y que representan el 80% de los ingresos totales
def Analisis_MayoresIngresos (lista):
    total_ingresos, suma = 0, 0
    #Primero se cuantifica el ingreso total
    for elemento in lista:
        total_ingresos += elemento[1]['ingresos']
    
    #Después se recorre e imprime la lista de rutas (ordenada de mayor ingreso a menor ingreso) hasta llegar al 80% de los ingresos totales
    for elemento in lista:
        suma += elemento[1]['ingresos']
        if suma <= (total_ingresos*0.8):
            print(elemento[0] + ':', formato_cifra (elemento[1]['ingresos']) )
        else:
            suma -= elemento[1]['ingresos']
            print('* Las rutas anteriores aportan el',str(round(suma*100/total_ingresos, 2)) + '% de los ingresos totales')
            print('El total de ingresos fue de', formato_cifra(total_ingresos) )
            break

#Se define una función que da formato a las cifras monetarias, separando los dígitos con comas y agregando el signo monetario al principio, para favorecer su legibilidad
def formato_cifra (numero):
    numero = str(numero) #Convertimos el número a string
    numero_formato = '$' #Colocamos el signo monetario al inicio del formato del número
    #Se recorren los dígitos de la cifra de derecha a izquierda
    for i in range (len(numero)-1, -1, -1):
        #Cada tercer digito se agrega una coma
        if ((i+1)%3) == 0: #Si estamos en un índice múltiplo de 3 (pj. 3,6,9...) entonces agregamos una coma antes del dígito
            #Si el número tiene una cantidad total de cifras múltiplo de 3, omitimos anteponer una coma al primer dígito
            if i+1 == len(numero): 
                numero_formato = numero_formato + numero[-(i+1)]
            #Para los siguientes dígitos ubicados en un índice múltiplo de 3 se antepone una coma
            else:
                numero_formato = numero_formato +','
                numero_formato = numero_formato + numero[-(i+1)]
        #Para los dígitos en índices que no sean múltiplos del 3 únicamente se anexan sin anteponer una coma
        else:
            numero_formato = numero_formato + numero[-(i+1)]
    return numero_formato
                    
#Se abre el archivo.csv
with open("synergy_logistics_database.csv","r",encoding="utf-8-sig") as archivo:
    #Se genera el objeto lector en forma de diccionario
    lector = csv.DictReader(archivo)
    
    #Se itera sobre cada línea del objeto lector
    for linea in lector:
        #Se genera una cadena de texto con la ruta ("Origen - Destino")
        ruta = linea['origin'] + ' - ' + linea['destination']
        
        #Se analizan los datos de las rutas de exportación
        if linea['direction'] == 'Exports':
            #Se calcula la frecuencia y el total de ingresos de cada ruta de exportación
            Analisis_Frecuencia_IngresosTotales(rutas_exportaciones)
            #Se calcula la frecuencia y el total de ingresos por método de transporte de cada exportación
            Analisis_Transportes (transportes_exportaciones)
        
        #Se analizan los datos de las rutas de importación
        if linea['direction'] == 'Imports':
            #Se calcula la frecuencia y el total de ingresos de cada ruta de importación
            Analisis_Frecuencia_IngresosTotales(rutas_importaciones)
            #Se calcula la frecuencia y el total de ingresos por método de transporte de cada importación
            Analisis_Transportes (transportes_importaciones)
                 
            
#Se imprimen los resultados:

### RUTAS MÁS DEMANDADAS
print('EXPORTACIONES - 10 RUTAS MÁS DEMANDADAS:')
#print(list(rutas_exportaciones.items())[0][1]['frecuencia'])
exportaciones_ordenada = sorted(rutas_exportaciones.items(), key=lambda x: x[1]['frecuencia'], reverse=True)
print(exportaciones_ordenada[:10])
print()
print('IMPORTACIONES - 10 RUTAS MÁS DEMANDADAS:')
importaciones_ordenada = sorted(rutas_importaciones.items(), key=lambda x: x[1]['frecuencia'], reverse=True)
print(importaciones_ordenada[:10])
print()
#PROCESO DE GRAFICACIÓN
plt.figure(1)
#Se recuperan los resultados en listas, para graficar con mayor facilidad
lista_datos_graficar = [] #Generamos una variable que almacenará los datos a graficar
lista_nombres_graficar = []
for i in range(10):
    lista_datos_graficar.append(exportaciones_ordenada[i][1]['frecuencia'])
    lista_nombres_graficar.append(exportaciones_ordenada[i][0])
#Se grafica el resultado de exportaciones
plt.suptitle('10 RUTAS MÁS DEMANDADAS',fontsize = 16)
plt.subplot(1,2,1)
colors = ['red','crimson','orangered','tomato','orange','gold','yellow','lawngreen','springgreen','lightgreen']
plt.bar(range(10), lista_datos_graficar, color=colors)
plt.xlabel('Ruta', fontsize = 14, labelpad = 10)
plt.ylabel('Frecuencia de uso', fontsize = 14, labelpad = 1)
plt.title('EXPORTACIÓN', pad=5, fontsize = 14)
plt.xticks(range(10), lista_nombres_graficar, rotation=90)
plt.subplots_adjust(bottom=0.44, left =0.15, top=0.85)
#Se recuperan los resultados en listas, para graficar con mayor facilidad
lista_datos_graficar = [] #Generamos una variable que almacenará los datos a graficar
lista_nombres_graficar = []
for i in range(10):
    lista_datos_graficar.append(importaciones_ordenada[i][1]['frecuencia'])
    lista_nombres_graficar.append(importaciones_ordenada[i][0])
print(lista_nombres_graficar,lista_datos_graficar)
#Se grafica el resultado de importaciones
plt.subplot(1,2,2)
plt.bar(range(10), lista_datos_graficar, color=colors)
plt.xlabel('Ruta', fontsize = 14, labelpad = 10)
plt.ylabel('Frecuencia de uso', fontsize = 14, labelpad = 1)
plt.title('IMPORTACIÓN', pad=5, fontsize = 14)
plt.xticks(range(10), lista_nombres_graficar, rotation=90)


### RUTAS DE MAYORES INGRESOS
print('EXPORTACIONES - 10 RUTAS DE MAYORES INGRESOS:')
exportaciones_ordenada = sorted(rutas_exportaciones.items(), key=lambda x: x[1]['ingresos'], reverse=True)
print(exportaciones_ordenada[:10])
print()
print('IMPORTACIONES - 10 RUTAS DE MAYORES INGRESOS:')
importaciones_ordenada = sorted(rutas_importaciones.items(), key=lambda x: x[1]['ingresos'], reverse=True)
print(importaciones_ordenada[:10])
print()
#PROCESO DE GRAFICACIÓN
plt.figure(2)
#Se recuperan los resultados en listas, para graficar con mayor facilidad
lista_datos_graficar = [] #Generamos una variable que almacenará los datos a graficar
lista_nombres_graficar = []
for i in range(10):
    lista_datos_graficar.append(exportaciones_ordenada[i][1]['ingresos'])
    lista_nombres_graficar.append(exportaciones_ordenada[i][0])
#Se grafica el resultado de exportaciones
plt.suptitle('10 RUTAS DE MAYORES INGRESOS',fontsize = 16)
plt.subplot(1,2,1)
colors = ['red','crimson','orangered','tomato','orange','gold','yellow','lawngreen','springgreen','lightgreen']
plt.bar(range(10), lista_datos_graficar, color=colors)
plt.xlabel('Ruta', fontsize = 14, labelpad = 10)
plt.ylabel('Ingresos [$]', fontsize = 14, labelpad = 1)
plt.title('EXPORTACIÓN', pad=5, fontsize = 14)
plt.xticks(range(10), lista_nombres_graficar, rotation=90)
plt.subplots_adjust(bottom=0.44, left =0.15, top=0.85)
#Se recuperan los resultados en listas, para graficar con mayor facilidad
lista_datos_graficar = [] #Generamos una variable que almacenará los datos a graficar
lista_nombres_graficar = []
for i in range(10):
    lista_datos_graficar.append(importaciones_ordenada[i][1]['ingresos'])
    lista_nombres_graficar.append(importaciones_ordenada[i][0])
print(lista_nombres_graficar,lista_datos_graficar)
#Se grafica el resultado de importaciones
plt.subplot(1,2,2)
plt.bar(range(10), lista_datos_graficar, color=colors)
plt.xlabel('Ruta', fontsize = 14, labelpad = 10)
plt.ylabel('Ingresos [$]', fontsize = 14, labelpad = 1)
plt.title('IMPORTACIÓN', pad=5, fontsize = 14)
plt.xticks(range(10), lista_nombres_graficar, rotation=90)


### TRANSPORTES MÁS DEMANDADOS
print('EXPORTACIONES - TRANSPORTES MÁS DEMANDADOS:')
transportes_exp_ordenada = sorted(transportes_exportaciones.items(), key=lambda x: x[1]['frecuencia'], reverse=True)
print(transportes_exp_ordenada)
print()
print('IMPORTACIONES - TRANSPORTES MÁS DEMANDADOS:')
transportes_imp_ordenada = sorted(transportes_importaciones.items(), key=lambda x: x[1]['frecuencia'], reverse=True)
print(transportes_imp_ordenada)
print()
#PROCESO DE GRAFICACIÓN
plt.figure(3)
#Se recuperan los resultados en listas, para graficar con mayor facilidad
lista_datos_graficar = [] #Generamos una variable que almacenará los datos a graficar
lista_nombres_graficar = []
for i in range(len(transportes_exp_ordenada)):
    lista_datos_graficar.append(transportes_exp_ordenada[i][1]['frecuencia'])
    lista_nombres_graficar.append(transportes_exp_ordenada[i][0])
#Se grafica el resultado de exportaciones
plt.suptitle('TRANSPORTES MÁS DEMANDADOS',fontsize = 16)
plt.subplot(1,2,1)
colors = ['orangered','gold','springgreen','cyan']
plt.bar(range(len(transportes_exp_ordenada)), lista_datos_graficar, color=colors)
plt.xlabel('Vía de transporte', fontsize = 14, labelpad = 10)
plt.ylabel('Frecuencia de uso', fontsize = 14, labelpad = 1)
plt.title('EXPORTACIÓN', pad=5, fontsize = 14)
plt.xticks(range(len(transportes_exp_ordenada)), lista_nombres_graficar, rotation=90)
plt.subplots_adjust(bottom=0.33, wspace=0.35, top=0.85)
#Se recuperan los resultados en listas, para graficar con mayor facilidad
lista_datos_graficar = [] #Generamos una variable que almacenará los datos a graficar
lista_nombres_graficar = []
for i in range(len(transportes_imp_ordenada)):
    lista_datos_graficar.append(transportes_imp_ordenada[i][1]['frecuencia'])
    lista_nombres_graficar.append(transportes_imp_ordenada[i][0])
print(lista_nombres_graficar,lista_datos_graficar)
#Se grafica el resultado de importaciones
plt.subplot(1,2,2)
plt.bar(range(len(transportes_imp_ordenada)), lista_datos_graficar, color=colors)
plt.xlabel('Vía de transporte', fontsize = 14, labelpad = 10)
plt.ylabel('Frecuencia de uso', fontsize = 14, labelpad = 1)
plt.title('IMPORTACIÓN', pad=5, fontsize = 14)
plt.xticks(range(len(transportes_imp_ordenada)), lista_nombres_graficar, rotation=90)

### TRANSPORTES MÁS REMUNERANTES
print('EXPORTACIONES - TRANSPORTES QUE GENERAN MAYORES INGRESOS:')
transportes_exp_ordenada = sorted(transportes_exportaciones.items(), key=lambda x: x[1]['ingresos'], reverse=True)
print(transportes_exp_ordenada)
print()
print('IMPORTACIONES - TRANSPORTES QUE GENERAN MAYORES INGRESOS:')
transportes_imp_ordenada = sorted(transportes_importaciones.items(), key=lambda x: x[1]['ingresos'], reverse=True)
print(transportes_imp_ordenada)
print()
#PROCESO DE GRAFICACIÓN
plt.figure(4)
#Se recuperan los resultados en listas, para graficar con mayor facilidad
lista_datos_graficar = [] #Generamos una variable que almacenará los datos a graficar
lista_nombres_graficar = []
for i in range(len(transportes_exp_ordenada)):
    lista_datos_graficar.append(transportes_exp_ordenada[i][1]['ingresos'])
    lista_nombres_graficar.append(transportes_exp_ordenada[i][0])
#Se grafica el resultado de exportaciones
plt.suptitle('TRANSPORTES QUE GENERAN MAYORES INGRESOS',fontsize = 16)
plt.subplot(1,2,1)
colors = ['orangered','gold','springgreen','cyan']
plt.bar(range(len(transportes_exp_ordenada)), lista_datos_graficar, color=colors)
plt.xlabel('Vía de transporte', fontsize = 14, labelpad = 10)
plt.ylabel('Ingresos [$]', fontsize = 14, labelpad = 1)
plt.title('EXPORTACIÓN', pad=5, fontsize = 14)
plt.xticks(range(len(transportes_exp_ordenada)), lista_nombres_graficar, rotation=90)
plt.subplots_adjust(bottom=0.33, wspace=0.35, top=0.85)
#Se recuperan los resultados en listas, para graficar con mayor facilidad
lista_datos_graficar = [] #Generamos una variable que almacenará los datos a graficar
lista_nombres_graficar = []
for i in range(len(transportes_imp_ordenada)):
    lista_datos_graficar.append(transportes_imp_ordenada[i][1]['ingresos'])
    lista_nombres_graficar.append(transportes_imp_ordenada[i][0])
print(lista_nombres_graficar,lista_datos_graficar)
#Se grafica el resultado de importaciones
plt.subplot(1,2,2)
plt.bar(range(len(transportes_imp_ordenada)), lista_datos_graficar, color=colors)
plt.xlabel('Vía de transporte', fontsize = 14, labelpad = 10)
plt.ylabel('Ingresos [$]', fontsize = 14, labelpad = 1)
plt.title('IMPORTACIÓN', pad=5, fontsize = 14)
plt.xticks(range(len(transportes_imp_ordenada)), lista_nombres_graficar, rotation=90)

### RUTAS QUE GENERAN EL 80% DE LOS INGRESOS
print('EXPORTACIONES - RUTAS QUE GENERAN EL 80% DE LOS INGRESOS:')
Analisis_MayoresIngresos(exportaciones_ordenada)
print()

print('IMPORTACIONES - RUTAS QUE GENERAN EL 80% DE LOS INGRESOS:')
Analisis_MayoresIngresos(importaciones_ordenada)


plt.show()
