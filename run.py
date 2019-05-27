# run.py
import matplotlib.pyplot as plt
from model import *  
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


model = CTOModel(24, 12, 5, 30, 30)
history_observation = []
for i in range(300):
    model.step()
    for agent in model.schedule.agents:
        global_observation = set ([])
        if ('o_' in agent.unique_id):
            #print (agent.unique_id)
            #print ("observando")
            for target in  agent.under_observation:
                if ('t_' in target.unique_id):
                    #print (target.unique_id)
                    global_observation.add(target.unique_id)
    
    history_observation.append(len(global_observation))

plt.hist(history_observation)
plt.savefig('histograma.png')
plt.clf()

observers_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    i = 0
    for agent in cell_content:
        if ('o_' in agent.unique_id):
            i += 1
    observers_counts[x][y] = i
plt.imshow(observers_counts, interpolation='nearest')
plt.colorbar()
plt.savefig('observers_positions.png')
plt.clf()

targets_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    i = 0
    for agent in cell_content:
        if ('t_' in agent.unique_id):
            i += 1
    targets_counts[x][y] = i
plt.imshow(targets_counts, interpolation='nearest')
plt.colorbar()
plt.savefig('targets_positions.png')
