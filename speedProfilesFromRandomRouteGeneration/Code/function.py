import requests
import math

def getSlopeAngle(altitude1 : int, altitude2 : int, distance : int): #Esta funcion retorna el angulo de la pendiente, recibe las dos altitudes y la distancia entre estos dos puntos
    height = altitude2 - altitude1
    angle = math.degrees( math.asin(height/distance) )
    return angle #Cuando el angulo es negativo va en bajada, cuando el angulo es positivo va en subida
    
    
def make_stringURL(i : int, n : int, list_of_nodes : list): #indice donde inicia los nodos - cantidad puntos - nodos
    
    strTemp = ""
    
    for x in range(i, n):
        strTemp += "point={latitude},{longitude}&".format(latitude=list_of_nodes[x][0], longitude=list_of_nodes[x][1])
    
    return("https://graphhopper.com/api/1/route?{}elevation=true&points_encoded=false&details=time&details=distance&calc_points=true&key=api_key".format(strTemp))#en esta parte debe poner localmente la api_key, esto se obtiene al logguearse


def getVelocities_slopes(list_of_nodes : list): #Recibe una lista de tuplas(latitude, longitude) ej: [(6.345817,-75.538971),(6.340448,-75.545554)] 

    len_nodes = len(list_of_nodes)
    speeds = [] #Lista donde se guardaran las velocidades
    slopeAngles = [] #Lista donde se guardaran los angulos de las pendientes, los angulos negativos son cuando va en bajada, los positivos es en subida

    if(len_nodes < 2): print('There arent enough nodes')
        
    if(len_nodes <= 5):
        
        response = requests.get(make_stringURL(0, len_nodes, list_of_nodes))#Se hace una peticion en base a la URL que devuelva el metodo
        
        if(response.status_code == 200):
                
            responseJSON = response.json()
            distances = responseJSON["paths"][0]["details"]["distance"]#arreglo de distancias en metros
            times = responseJSON["paths"][0]["details"]["time"] #Arreglo de tiempos en milisegundos
            coordinates = responseJSON["paths"][0]["points"]["coordinates"] #Arreglo de las coordenadas
            
            for i in range(len(times)): #El tamaño de distances y times es el mismo
                
                kilometers = distances[i][2]/1000 #Calculo los kilometros
                hours = times[i][2]/3600000 #Calculo las horas
                speed = kilometers/hours #Calculo la velocidad km/h
                seconds = round((times[i][2]/1000)) #Obtengo los segundos
                firstInterval = times[i][0] #Obtengo los intervalos del tiempo para calcular las coordenadas en el mismo tramo
                secondInterval = times[i][1] # '     '   '    '    '     '    '    '   ' '     '      '     '    '
                slopeAngle = getSlopeAngle( coordinates[firstInterval][2], coordinates[secondInterval][2], distances[i][2] ) #Llamo la funcion para obtener el angulo de la pendiente, le paso las altitudes respectivas al intervalo y la distancia q las separa
                
                for i in range (seconds):
                    speeds.append(round(speed, 2))
                    slopeAngles.append(round(slopeAngle, 2))

    return (speeds, slopeAngles)


def main():
    list_of_nodes = [(6.345817,-75.538971),(6.340448,-75.545554)] 
    speeds, slopeAngles = getVelocities_slopes(list_of_nodes)

    print(speeds)
    print("ANGULOS:")
    print(slopeAngles)


main()    

