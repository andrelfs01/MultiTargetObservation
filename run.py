# run.py
import matplotlib.pyplot as plt
from model import *  
import numpy as np


model = CTOModel(24, 12, 5, 50, 50)
for i in range(30):
    model.step()
    if (i % 5 == 0):
        for agent in model.schedule.agents:
            #under_observation = []
            if ('o_' in agent.unique_id):
                print (agent.unique_id)
                print (agent.under_observation)

