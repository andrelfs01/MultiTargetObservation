# model.py
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector
from random import uniform
import math

class TargetAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.under_observation = []
        self.destination = None

    def step(self):
        self.move()
    
    def move(self):
        if (self.destination is None or self.pos == self.destination):
            self.destination = self.new_destination()
        new_position = self.trace_next_move()
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
    def __init__(self, unique_id, sensor_range, model):
        super().__init__(unique_id, model)
        self.under_observation = []
        self.sensor_range = sensor_range

    def step(self):
        self.move()
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        ## verify field of view
        self.under_observation = self.check_fov()

    def check_fov(self):
        in_fov = self.model.grid.get_neighborhood(
                    self.pos,
                    True,
                    True,
                    self.sensor_range)
        #print (in_fov)
        return self.model.grid.get_cell_list_contents(in_fov)

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
    def __init__(self, N, O, sensorRange, width, height):
        self.running = True
        self.num_agents = N
        self.num_observer_agents = O
        self.sensor_range  = sensorRange
        self.grid = Grid(width, height, False)
        self.schedule = RandomActivation(self)

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
            b = ObserverAgent("o_"+str(i), self.sensor_range, self)
            self.schedule.add(b)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(b, (x, y))

        self.datacollector = DataCollector(
            agent_reporters={"Observation": "under_observation"})  

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        
