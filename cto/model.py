from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from cto.agents import TargetAgent, ObserverAgent

from random import uniform
import math
from pandas import DataFrame
from sklearn.cluster import KMeans
import numpy as np
import time


class Modelo(Model):
    """
    A model with some number of agents.
    """

    N=1
    O=1
    sensorRange=5
    target_speed=1.0
    active_prediction=False
    a=1
    width = 20
    height = 20

    def __init__(self, N=1, O=1, sensorRange=5, target_speed=1.0, active_prediction=False, a=1, width = 20, height = 20):
        super().__init__()
        #self.running = True
        self.num_agents = N
        self.num_observer_agents = O
        self.target_speed = target_speed 
        self.multiplication_factor = 1.0/target_speed 
        self.sensor_range  = sensorRange # * self.multiplication_factor
                
        self.grid = MultiGrid(int(width), int(height), False)
        self.schedule = RandomActivation(self)
        self.observers_indications = []
        self.a = a
        self.active_prediction = active_prediction
        
        self.verbose = False  # Print-monitoring



#        self.datacollector = DataCollector(
#            {"Wolves": lambda m: m.schedule.get_breed_count(Wolf),
#             "Sheep": lambda m: m.schedule.get_breed_count(Sheep)})

        # Create targets
        for i in range(self.num_agents):
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            a = TargetAgent("t_"+str(i), (x, y), self, False)
            self.schedule.add(a)

            
            self.grid.place_agent(a, (x, y))

        # Create observers
        for i in range(self.num_observer_agents):
            #b = ObserverAgent("o_"+str(i), self.sensor_range, self.multiplication_factor, self)

            # Add the agent to a kmens indication
            self.observers_indications = self.kmeans_indications()
            point = self.observers_indications[i] 
            x = math.floor(point[0])
            y = math.floor(point[1])
            b = ObserverAgent("o_"+str(i), (x, y), self, False)
            self.schedule.add(b)

            
            self.grid.place_agent(b, (x, y))

        self.datacollector = DataCollector(
            agent_reporters={"Observation": "under_observation"})


    def step(self):
        if ((self.schedule.steps % 10) == 0):
                # print ("running kmeans...")
                if(not self.active_prediction):
                    # print("kmeans")
                    self.observers_indications = self.kmeans_indications()
                else:
                    self.observers_indications = self.kmeans_predicted_indications()
        self.schedule.step()
        # print("step")
        self.datacollector.collect(self)

    def kmeans_indications(self):
        x_list = []
        y_list = []
        for a in self.grid.coord_iter():
            agent, x, y = a
            print (agent)
            if (len(agent) != 0):
                for ag in agent:
                    if ('t_' in ag.unique_id):
                        y_list.append(y)
                        x_list.append(x)
        Data = {'x': x_list,
                'y': y_list }        
  
        df = DataFrame(Data,columns=['x','y'])
        # print (df)
        kmeans = KMeans(n_clusters=self.num_observer_agents).fit(df)
        centroids = kmeans.cluster_centers_
        return (centroids)
            
    def kmeans_predicted_indications(self):
        x_list = []
        y_list = []
        for a in self.grid.coord_iter():
            agent, x, y = a
            

            # print (agent)
            # calcular a equacao
            if (agent != None and 't_' in agent.unique_id):
                old_x = x
                old_y = y
                if (agent.old_position != None):
                    old_x, old_y = agent.old_position
                x_predicted = x + self.a * (x - old_x)
                y_predicted = y + self.a * (y - old_y)
                if (x_predicted < 0):
                    x_predicted = 0
                if (x_predicted >= self.grid.width):
                    x_predicted = self.grid.width - 1
                if (y_predicted < 0):
                    y_predicted = 0
                if (y_predicted >= self.grid.height):
                    y_predicted = self.grid.height -1

                y_list.append(y_predicted)
                x_list.append(x_predicted)
        Data = {'x': x_list,
                'y': y_list }        
  
        df = DataFrame(Data,columns=['x','y'])
        # print (df)
        kmeans = KMeans(n_clusters=self.num_observer_agents).fit(df)
        centroids = kmeans.cluster_centers_
        return (centroids)

    def run_model(self, step_count=2000):

        if self.verbose:
            print('Initial number targets: ',
                  self.num_agents)
            print('Initial number observers: ',
                  self.num_observer_agents)

        for i in range(step_count):
            self.step()
