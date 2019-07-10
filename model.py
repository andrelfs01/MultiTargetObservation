# model.py
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector
from random import uniform
import math
from pandas import DataFrame
from sklearn.cluster import KMeans
import numpy as np

class TargetAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.under_observation = []
        self.destination = None
        self.old_position = None

    def step(self):
        self.move()
    
    def move(self):
        if (self.destination is None or self.pos == self.destination):
            self.destination = self.new_destination()
        new_position = self.trace_next_move()
        self.old_position = self.pos
        self.model.grid.move_agent(self, new_position)

# Cada alvo calcula o próximo destino, a partir da posição atual (x,y) 
    def new_destination(self):
        x, y = self.pos
        new_x = x + uniform(-25, 25)#Ele gera dois números aleatórios no intervalo [-25,+25]
        new_y = y + uniform(-25, 25)#Ele gera dois números aleatórios no intervalo [-25,+25]
#       desde que não caia fora do "cercado"
        while (new_x > self.model.grid.width or new_x < 0):
            new_x = x + uniform(-25, 25)
 
        while (new_y > self.model.grid.height or new_y < 0):
            new_y = y + uniform(-25, 25)

        return (math.floor(new_x), math.floor(new_y))

    def trace_next_move(self):
        x_pos, y_pos = self.pos
        x_dest, y_dest = self.destination
        if (x_dest > x_pos):
            x = x_pos + 1
            if (y_dest > y_pos):
                y = y_pos + 1
            elif (y_dest < y_pos):
                y = y_pos - 1
            else:
                y = y_pos
        elif (x_dest < x_pos):
            x = x_pos - 1
            if (y_dest > y_pos):
                y = y_pos + 1
            elif (y_dest < y_pos):
                y = y_pos - 1
            else:
                y = y_pos
        else:
            x = x_pos
            if (y_dest > y_pos):
                y = y_pos + 1
            elif (y_dest < y_pos):
                y = y_pos - 1
            else:
                y = y_pos
        return (x ,y)


class ObserverAgent(Agent):
    def __init__(self, unique_id, sensor_range, multiplication_factor, model):
        super().__init__(unique_id, model)
        self.under_observation = []
        self.sensor_range = sensor_range
        self.multiplication_factor = multiplication_factor
        self.destination = []

    def step(self):
        if (self.model.observers_indications.size != 0):
            self.destination = self.closer()
            self.move()
        else:
            self.move()
    
    def move(self):
        for i in range(0, int(self.multiplication_factor)):
            new_position = self.trace_next_move()
            self.model.grid.move_agent(self, new_position)
        ## verify field of view
        self.under_observation = self.check_fov()
        


    def check_fov(self):
        in_fov = self.model.grid.get_neighborhood(
                    self.pos,
                    True,
                    True,
                    int(self.sensor_range))
        #print (in_fov)
        return self.model.grid.get_cell_list_contents(in_fov)
    
    #verify indication closer to observer  
    def closer(self):
        dist = self.model.grid.height + self.model.grid.width + 100
        key = 0
        closer = []
        i = 0
        for point_indication in self.model.observers_indications:
            x1, y1 = self.pos
            x2 = math.floor(point_indication[0])
            y2 = math.floor(point_indication[1])
            #d =  self.model.grid.get_distance(self.pos, point_indication)
            d = math.sqrt( ((x1-x2)**2)+((y1-y2)**2))
            if (d <= dist):
                dist = d
                key = i
                closer = point_indication
            i += 1
        
        #print (closer, self.pos, self.model.observers_indications)
        #remove
        self.model.observers_indications = np.delete(self.model.observers_indications, key, 0)
        #return         
        return (math.floor(closer[0]), math.floor(closer[1]))

    def trace_next_move(self):
        x_pos, y_pos = self.pos
        x_dest, y_dest = self.destination
        if (x_dest > x_pos):
            x = x_pos + 1
            if (y_dest > y_pos):
                y = y_pos + 1
            elif (y_dest < y_pos):
                y = y_pos - 1
            else:
                y = y_pos
        elif (x_dest < x_pos):
            x = x_pos - 1
            if (y_dest > y_pos):
                y = y_pos + 1
            elif (y_dest < y_pos):
                y = y_pos - 1
            else:
                y = y_pos
        else:
            x = x_pos
            if (y_dest > y_pos):
                y = y_pos + 1
            elif (y_dest < y_pos):
                y = y_pos - 1
            else:
                y = y_pos
        return (x ,y)

#verify number of targets under all observer's fov
def verify_observation(model):
    global_observation = set ([])
    for agent in model.schedule.agents:
        if ('o_' in agent.unique_id):
            for target in agent.under_observation:
                if ('t_' in target.unique_id):
                    #print (target.unique_id)
                    global_observation.add(target.unique_id)
    
    return len(global_observation)

class CTOModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, O, sensorRange, target_speed, active_prediction, a, width, height):
        self.running = True
        self.num_agents = N
        self.num_observer_agents = O
        self.target_speed = target_speed 
        self.multiplication_factor = 1.0/target_speed 
        self.sensor_range  = sensorRange * self.multiplication_factor
                
        #modificação para diminuir demora na execução
        #self.grid = Grid(int(width * self.multiplication_factor), int(height * self.multiplication_factor), False)
        self.grid = Grid(int(width), int(height), False)
        self.schedule = RandomActivation(self)
        self.observers_indications = []
        self.a = a
        self.active_prediction = active_prediction
        
        # Create targets
        for i in range(self.num_agents):
            a = TargetAgent("t_"+str(i), self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # Create observers
        for i in range(self.num_observer_agents):
            b = ObserverAgent("o_"+str(i), self.sensor_range, self.multiplication_factor, self)
            self.schedule.add(b)

            #Add the agent to a kmens indication
            self.observers_indications = self.kmeans_indications()
            point = self.observers_indications[i] 
            x = math.floor(point[0])
            y = math.floor(point[1])
            self.grid.place_agent(b, (x, y))

        self.datacollector = DataCollector(
            agent_reporters={"Observation": "under_observation"})  

    def step(self):
        if ((self.schedule.steps % 10) == 0):
                #print ("running kmeans...")
                if(not self.active_prediction):
                    print("kmeans")
                    self.observers_indications = self.kmeans_indications()
                else:
                    self.observers_indications = self.kmeans_predicted_indications()
        self.schedule.step()
        #print("step")
        self.datacollector.collect(self)
        
    def kmeans_indications(self):
        x_list = []
        y_list = []
        for a in self.grid.coord_iter():
            agent, x, y = a
            #print (agent)
            if (agent != None and 't_' in agent.unique_id):
                y_list.append(y)
                x_list.append(x)
        Data = {'x': x_list,
                'y': y_list }        
  
        df = DataFrame(Data,columns=['x','y'])
        #print (df)
        kmeans = KMeans(n_clusters=self.num_observer_agents).fit(df)
        centroids = kmeans.cluster_centers_
        return (centroids)
            
    def kmeans_predicted_indications(self):
        x_list = []
        y_list = []
        for a in self.grid.coord_iter():
            agent, x, y = a
            

            #print (agent)
            #calcular a equacao
            if (agent != None and 't_' in agent.unique_id):
                old_x = x
                old_y = y
                if (agent.old_position != None):
                    old_x, old_y = agent.old_position
                x_predicted = x + self.a * (x - old_x)
                y_predicted = y + self.a * (y - old_y)
                y_list.append(y_predicted)
                x_list.append(x_predicted)
        Data = {'x': x_list,
                'y': y_list }        
  
        df = DataFrame(Data,columns=['x','y'])
        #print (df)
        kmeans = KMeans(n_clusters=self.num_observer_agents).fit(df)
        centroids = kmeans.cluster_centers_
        return (centroids)
        
