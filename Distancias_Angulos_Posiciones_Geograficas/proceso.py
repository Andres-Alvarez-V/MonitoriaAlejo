from math import sin, cos, sqrt, atan2, radians
import numpy as np

def distance_haversine(lat1, lon1, lat2, lon2):#Esta es la formula de haversine, esto recibe latitud y longitud
    # approximate radius of earth in meters
    R = 6373000.0
    
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1 : list, v2 : list): #V1 es el vector antes del giro - V2 es el vector luego del giro
    """ Returns the angle in degrees between vectors 'v1' and 'v2'::
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    
    degreesValue = np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))
    #print(v1_u, v2_u)
    #if(v1_u[1] > v2_u[1]): return -(degreesValue)
    return degreesValue

def get_distances(l: list): #Recibe una lista de tuplas(latitude, longitude), retorna n-1 distancias entre los puntos consecutivamente
    distances = []
    len_list = len(l)
    for i in range(len_list-1):
        distance = distance_haversine(l[i][0],l[i][1],l[i+1][0], l[i+1][1])
        distances.append(distance)
    
    return distances


    

def get_angles(l: list) : #Recibe una lista de tuplas(latitude, longitude), retorna n-2 angulos entre los puntos consecutivamente
    angles = []
    len_list = len(l)
    for i in range(len_list-2):
        v1 = list(map(lambda i, j: (j - i), l[i], l[i+1]))
        v2 = list(map(lambda i, j: (j - i), l[i+1], l[i+2]))
        angle = angle_between(v1, v2)
        angles.append(angle)
    return angles


    
def get_cartesian_points(l:list): #Recibe una lista de tuplas(latitude, longitude), retorna n puntos cartesianos desde el punto 0,0 que es el inicial
    cartesianPoints = []
    len_list = len(l)
    firstElement = l[0]
    for i in range(len_list):
        point = list(map(lambda i, j: i - j, l[i], firstElement))
        #print(list(map(lambda i: i*10000, point)))
        cartesianPoints.append(point)
    return cartesianPoints
    
    

def nose(list_of_nodes : list): #Recibe una lista de tuplas(latitude, longitude) ej: [(6.345817,-75.538971),(6.340448,-75.545554)] 

    distances = get_distances(list_of_nodes)
    cartesian_points = get_cartesian_points(list_of_nodes)
    turning_angles = get_angles(list_of_nodes)
    print(cartesian_points)
    
    return turning_angles, distances


    
    
    
    
def main():
        
    nodes = [(6.224331, -75.197122), (6.228073, -75.193758), (6.234815, -75.195872), (6.246944, -75.192731), (6.249814, -75.184046), (6.260827, -75.195057), (6.238565, -75.188579)]
    #nodes = [(6.342520, -75.546081),(6.342690, -75.545476),(6.343166, -75.545544),(6.342755, -75.544833),(6.342891, -75.544322), (6.343656, -75.545585),(6.344065, -75.545663)]
    turning_angles, distances = nose(nodes)
    print("Turning angles: ")
    print(turning_angles)
    print("Distances")
    print(distances)
        
    
main()





