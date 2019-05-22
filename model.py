# model.py
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class TargetAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.under_observation = []

    def step(self):
        self.move()
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

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
                    self.sensor_range,
                    include_center=True)
        #print (in_fov)
        return self.model.grid.get_cell_list_contents(in_fov)
        

class CTOModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, O, sensorRange, width, height):
        self.running = True
        self.num_agents = N
        self.num_observer_agents = O
        self.sensor_range  = sensorRange
        self.grid = MultiGrid(width, height, True)
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
            agent_reporters={"Wealth": "under_observation"})  # An agent attribute

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        
