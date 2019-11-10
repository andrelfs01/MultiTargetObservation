from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from random import uniform
import math
import time
import numpy as np
#from cto.random_walk import RandomWalker


class TargetAgent(Agent):
    under_observation = {}
    pos = (1,1)
    unique_id = 't_'
    destination = None
    old_position = (0,0)
    speed = 1

    def __init__(self, unique_id, pos, model,target_speed, destination = None, old_position = None, ):
        super().__init__(unique_id, model)
        self.under_observation = {}
        self.unique_id = unique_id
        self.destination = destination
        self.old_position = old_position
        self.speed = target_speed

    def step(self):
        self.move()
    
    def move(self):
        #print("dest: {}".format(self.destination))
        if (self.destination is False or self.destination is None or self.pos == self.destination):
            self.destination = self.new_destination()
        self.trace_next_move()
        
        if ( self.old_position != self.pos):
            print("pos: {} ".format(self.pos))
            _x, _y = self.pos
            self.model.grid.move_agent(self, self.correction_pos(_x, _y))

    def  correction_pos(self, continuos_x, continuos_y):
        if continuos_x < 0:
            continuos_x = 0
        
        if continuos_y < 0:
            continuos_y = 0

        if continuos_x >= self.model.grid.x_max:
            continuos_x = self.model.grid.x_max - 0.1

        if continuos_y >= self.model.grid.y_max:
            continuos_y = self.model.grid.y_max - 0.1

        return (continuos_x, continuos_y)

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

        return (new_x, new_y)
    
    #funcao que define o movimento em um passo, de acordo com o destino do agente.
    def trace_next_move(self):
        #posicao atual
        x_pos, y_pos = self.pos
        #destino do agente
        #print("det: {}".format(self.destination))
        x_dest, y_dest = self.destination
        
        #se o X do destino é maior que o X atual, incrementa o X para o movimento desse passo
        if (x_dest > x_pos):
            x = x_pos + self.speed
            #mesmo procedimento, agora aplicado ao Y
            #se o Y do destino é maior que o Y atual, incrementa o Y para o movimetno nesse passo
            if (y_dest > y_pos):
                y = y_pos + self.speed
            #se o Y do destino é menor que o Y atual, decrementa o Y para o movimento desse passo
            elif (y_dest < y_pos):
                y = y_pos - self.speed
            #senão, o Y do destino é igual o Y atual, não altera o Y para o movimento desse passo
            else:
                y = y_pos
        #se o X do destino é menor que o X atual, decrementa o X para o movimento desse passo
        elif (x_dest < x_pos):
            x = x_pos - self.speed
            #mesmo procedimento, agora aplicado ao Y
            if (y_dest > y_pos):
                y = y_pos + self.speed
            elif (y_dest < y_pos):
                y = y_pos - self.speed
            else:
                y = y_pos
        #senão, o X do destino é igual o X atual, não altera o X para o movimento desse passo
        else:
            x = x_pos
            #mesmo procedimento, agora aplicado ao Y
            if (y_dest > y_pos):
                y = y_pos + self.speed
            elif (y_dest < y_pos):
                y = y_pos - self.speed
            else:
                y = y_pos

        self.old_position = self.pos
        self.pos = self.correction_pos( x, y)
        return self.pos    

class ObserverAgent(Agent):

    under_observation = {}
    pos = (1,1)
    unique_id = 'o_'
    multiplication_factor = 1
    sensor_range = 5

    def __init__(self, unique_id, pos, model, sensor_range, multiplication_factor):
        super().__init__(unique_id, model)
        self.pos = pos
        self.under_observation = {}
        self.unique_id = unique_id
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
        new_position = self.trace_next_move()
        self.model.grid.move_agent(self, new_position)
        ## verify field of view
        self.under_observation = self.check_fov()      


    def check_fov(self):
        in_fov = self.model.grid.get_neighbors(
                    self.pos,
                    int(self.sensor_range))
        return in_fov
    
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

    
