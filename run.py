# run.py
import matplotlib.pyplot as plt
from model import *  
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from mesa.batchrunner import BatchRunner

run_iterations = 5
run_max_steps = 120

#variando o sensor range
fixed_params = {"width": 150,
                "height": 150,
                "N": 24,
                "O": 12,
                "target_speed": 0.5,
                "active_prediction": False,
                "a" : 1.0
                }

variable_params = {"sensorRange": range(5, 30, 5)}

batch_run = BatchRunner(CTOModel,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=run_iterations,
                        max_steps=run_max_steps,
                        model_reporters={"Observation": verify_observation})
print ("kmeans variando o sensor range")
# batch_run.run_all()

# run_data = batch_run.get_model_vars_dataframe()
# run_data.head()
# plt.scatter(run_data.sensorRange, run_data.Observation)
# plt.savefig('media_kmeans_variando_sensor.png')

plt.clf()
#variando o speed 
fixed_params = {"width": 150,
                "height": 150,
                "N": 24,
                "O": 12,
                "sensorRange": 20,
                "active_prediction": False,
                "a" : 1.0
                }

variable_params = {"target_speed": np.arange(0.1, 1.0, 0.2)}

batch_run = BatchRunner(CTOModel,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=run_iterations,
                        max_steps=run_max_steps,
                        model_reporters={"Observation": verify_observation})
print ("kmeans variando o target speed")
# batch_run.run_all()

# run_data = batch_run.get_model_vars_dataframe()
# run_data.head()
# plt.scatter(run_data.target_speed, run_data.Observation)
# plt.savefig('media_kmeans_variando_speed.png')
# plt.clf()


#com predicao
#variando o sensor range
fixed_params = {"width": 150,
                "height": 150,
                "N": 24,
                "O": 12,
                "target_speed": 0.5,
                "active_prediction": True,
                "a" : 1.0
                }

variable_params = {"sensorRange": range(5, 30, 5)}

batch_run = BatchRunner(CTOModel,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=run_iterations,
                        max_steps=run_max_steps,
                        model_reporters={"Observation": verify_observation})
print ("kmeans com predicao variando o sensor range")
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.sensorRange, run_data.Observation)
plt.savefig('media_kmeans_predicao_variando_sensor.png')

plt.clf()
#variando o speed 
fixed_params = {"width": 150,
                "height": 150,
                "N": 24,
                "O": 12,
                "sensorRange": 20,
                "active_prediction": True,
                "a" : 1.0
                }

variable_params = {"target_speed": np.arange(0.1, 1.0, 0.2)}

batch_run = BatchRunner(CTOModel,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=run_iterations,
                        max_steps=run_max_steps,
                        model_reporters={"Observation": verify_observation})
print ("kmeans com predicao variando o target speed")
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.target_speed, run_data.Observation)
plt.savefig('media_kmeans_predicao_variando_speed.png')
plt.clf()

# model = CTOModel(24, 12, 25, 150, 150)
# history_observation = []
# for i in range(1500):
#     model.step()
#     global_observation = set ([])
#     for agent in model.schedule.agents:
#         if ('o_' in agent.unique_id):
#             for target in agent.under_observation:
#                 if ('t_' in target.unique_id):
#                     #print (target.unique_id)
#                     global_observation.add(target.unique_id)
    
#     history_observation.append(len(global_observation))

# plt.hist(history_observation)
# plt.savefig('histograma.png')
# plt.clf()

# observers_counts = np.zeros((model.grid.width, model.grid.height))
# for cell in model.grid.coord_iter():
#     cell_content, x, y = cell
#     i = 0
#     for agent in cell_content:
#         if ('o_' in agent.unique_id):
#             i += 1
#     observers_counts[x][y] = i
# plt.imshow(observers_counts, interpolation='nearest')
# plt.colorbar()
# plt.savefig('observers_positions.png')
# plt.clf()

# targets_counts = np.zeros((model.grid.width, model.grid.height))
# for cell in model.grid.coord_iter():
#     cell_content, x, y = cell
#     i = 0
#     for agent in cell_content:
#         if ('t_' in agent.unique_id):
#             i += 1
#     targets_counts[x][y] = i
# plt.imshow(targets_counts, interpolation='nearest')
# plt.colorbar()
# plt.savefig('targets_positions.png')
