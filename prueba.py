# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""
import numpy as np
from matplotlib import *
#Preliminary function definition
def distance(inic_point,final_point):
    dist=abs(inic_point[0]-final_point[0])+abs(inic_point[1]-final_point[1])
    return dist
"""
#Testing distance function
#print(distance((0,0),(0,3)))
"""


#Classes definition: one for cars one for rides
class car:
    def __init__(self,posx,posy):
        self.position=[posx,posy]
    
class ride:
    def __init__(self,pos_inic_1,pos_inic_2,pos_final_1,pos_final_2,start_t,latest,avaliable,distance):
        self.pos_inics = [pos_inic_1,pos_inic_2]
        self.pos_final = [pos_final_1,pos_final_2]
        self.avaliable = avaliable
        self.distance = distance
        self.start_t = start_t
        self.latest = latest



#Open text file
f = open('e_high_bonus.in')
file='e_high_bonus.in'
text=f.read()


#Segementation of the text file
vector=text.split()


#obtain information from text file segmentation
rows= int(vector[0])
columns=int(vector[1])
number_vehicles= int(vector[2])
number_rides=int(vector[3])
bonus=int(vector[4])
timestep=int(vector[5])

#Generate a vector with car information: all cars begin in (0,0)

car_vector=[]
for i in range(number_vehicles):
    car_vector.append(car(0,0))
   
#Generate a vector with all possible rides    

rides_vector=[]  

#Obtain the information of all rides from the file and a for loop to write it in the vector

#initial and final position
inital_points_x_1 = np.loadtxt(file,delimiter=' ',skiprows=1,usecols=[0])
inital_points_x_2 = np.loadtxt(file,delimiter=' ',skiprows=1,usecols=[1])
final_points_y_1 = np.loadtxt(file,delimiter=' ',skiprows=1,usecols=[2])
final_points_y_2 = np.loadtxt(file,delimiter=' ',skiprows=1,usecols=[3])
#starting time
start_time = np.loadtxt(file,delimiter=' ',skiprows=1,usecols=[4])
#latest finish
latest_finish = np.loadtxt(file,delimiter=' ',skiprows=1,usecols=[5]) 
#Availability of the ride ((all rides are available at the beginning))
available_ride=True
#write the information in the vector
for i in range(number_rides):
    initial_1=inital_points_x_1[i]
    initial_2=inital_points_x_2[i]
    final_1=final_points_y_1[i]
    final_2=final_points_y_2[i]
    start_t=start_time[i]
    latest=latest_finish[i]
    distance_t=distance([initial_1,initial_2],[final_1,final_2])
    avaliable=available_ride
    rides_vector.append(ride(initial_1,initial_2,final_1,final_2,start_t,latest,avaliable,distance_t))


#grid generator (in case we needed)
grid = np.zeros((rows,columns), dtype=int)


#extracting ride information in a vector
viaje=rides_vector[0]
print(viaje.distance)

N_viajes = number_rides
N_car = number_vehicles
n_viajes = 0
B =bonus
T=timestep

def score_fun(viajes, j, D2, t, B):
    viaje = viajes[j]
    if D2[j][0] + t > viaje.start_t:
        if D2[j][0] + viaje.distance + t < viaje.latest:
            score = viaje.distance
        else:
            score = 0
    if D2[j][0] + t < viaje.start_t:
        if viaje.start_t+viaje.distance< viaje.latest:
          score  = viaje.distance   
        else:
            score = 0
    if D2[j][0] + t == viaje.start_t:
         if D2[j][0] + viaje.distance + t < viaje.latest:
             score = viaje.distance + B
         else:
             score = 0
    return score


submission = []

for car_idx in range(len(car_vector)):
    car = car_vector[car_idx]
    t = 0
    listofviajes=[]
    while t<T:
        D2 = []
        score = [0]
        A = False
        for i in range(len(rides_vector)):
            viaje = rides_vector[i]
            if viaje.avaliable:
                D2.append([distance(car.position,viaje.pos_inics),i])
        for j in range(len(D2)):
            score.append(score_fun(rides_vector, j, D2, t, B))
        
        if  np.amax(score) == 0:
            A = True
        if A:
            break
        max_pos = np.argmax(score)
        max_pos = max_pos -1
        choice = D2[max_pos][1]
        listofviajes.append(choice) 
        viaje = rides_vector[choice]
        car.position = viaje.pos_final
        viaje.avaliable = False
        t = np.amax(np.array([t+viaje.distance+D2[max_pos][0],viaje.start_t+viaje.distance]))
    submission.append([len(listofviajes),listofviajes])
print(submission)

with open("submisionE.in", "w") as output:
    for i in range(len(submission)):
        
        output.write(str(submission[i][0]))
        for j in range(len(submission[i][1])):
            output.write(str(" "))
            output.write(str(submission[i][1][j]))
        output.write(str("\n"))







 