# run.py
import matplotlib.pyplot as plt
from model import *  
import numpy as np


model = CTOModel(24, 12, 5, 10, 10)
for i in range(30):
    model.step()
    if (i % 5 == 0):
        for agent in model.schedule.agents:
            #under_observation = []
            if ('o_' in agent.unique_id):
                print (agent.unique_id)
                print ("observando")
                for target in  agent.under_observation:
                    print (target.unique_id)
                print ("--------------")

