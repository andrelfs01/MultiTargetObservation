from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
#from cto.random_walk import RandomWalker


class TargetAgent(Agent):
    '''
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    '''

    energy = None
    under_observation = []
    pos = (1,1)
    unique_id = 't_'

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, model)
        self.energy = energy
        self.under_observation = []
        self.unique_id = unique_id
        self.model = model
        self.moore = moore

    def step(self):
        '''
        A model step. Move, then eat grass and reproduce.
        '''
        self.random_move()
        living = True

    def random_move(self):
        '''
        Step one cell in any allowable direction.
        '''
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)


class ObserverAgent(Agent):
    '''
    A wolf that walks around, reproduces (asexually) and eats sheep.
    '''

    m = Model()
    m.schedule = RandomActivation(m)

    energy = None
    under_observation = []
    pos = (1,1)
    unique_id = 'o_'
    model = m

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, model)
        self.energy = energy
        self.pos = pos
        self.under_observation = []
        self.unique_id = unique_id
        self.model = model
        self.moore = moore
        
    def step(self):
        self.random_move()
        #self.energy -= 1

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, TargetAgent)]
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            
        if False:
            self.model.grid._remove_agent(self.pos, self)
           
        else:
            if self.random.random() < 0.5:
                # Create a new wolf cub
                #self.energy /= 2
                pass

    def random_move(self):
        '''
        Step one cell in any allowable direction.
        '''
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)
