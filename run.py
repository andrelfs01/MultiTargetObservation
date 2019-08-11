# run.py
import matplotlib.pyplot as plt
from model import *  
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from mesa.batchrunner import BatchRunner

run_iterations = 5
run_max_steps = 1500

#variando o sensor range: ~03:18 minutos
fixed_params = {"width": 150,
                "height": 150,
                "N": 24,
                "O": 12,
                "target_speed": 0.1,
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
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.sensorRange, run_data.Observation)
plt.savefig('geral_kmeans_variando_sensor.png')
plt.clf()

medias = run_data.groupby(['sensorRange']).mean()
plt.scatter(list(medias.Observation.index), medias.Observation.values)
plt.savefig('media_observacao_kmeans_variando_sensor.png')
plt.clf()

#variando o speed: ~05:00 minutos
fixed_params = {"width": 150,
                "height": 150,
                "N": 24,
                "O": 12,
                "sensorRange": 20,
                "active_prediction": False,
                "a" : 1.0
                }

variable_params = {"target_speed": [0.1, 0.2, 0.3, 0.5]}

batch_run = BatchRunner(CTOModel,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=run_iterations,
                        max_steps=run_max_steps,
                        model_reporters={"Observation": verify_observation})
print ("kmeans variando o target speed")
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.target_speed, run_data.Observation)
plt.savefig('geral_kmeans_variando_speed.png')
plt.clf()

medias = run_data.groupby(['target_speed']).mean()
plt.scatter(list(medias.Observation.index), medias.Observation.values)
plt.savefig('media_observacao_kmeans_variando_speed.png')
plt.clf()



#com predicao
#variando o sensor range: 03:22 minutos
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
plt.savefig('geral_kmeans_predicao_variando_sensor.png')
plt.clf()

medias = run_data.groupby(['sensorRange']).mean()
plt.scatter(list(medias.Observation.index), medias.Observation.values)
plt.savefig('media_observacao_kmeans_predicao_variando_sensor.png')
plt.clf()

#variando o speed: 

fixed_params = {"width": 150,
                "height": 150,
                "N": 24,
                "O": 12,
                "sensorRange": 20,
                "active_prediction": True,
                "a" : 1.0
                }

variable_params = {"target_speed": [0.1, 0.2, 0.3, 0.5]}

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
plt.savefig('geral_kmeans_predicao_variando_speed.png')
plt.clf()

medias = run_data.groupby(['target_speed']).mean()
plt.scatter(list(medias.Observation.index), medias.Observation.values)
plt.savefig('media_observacao_kmeans_predicao_variando_speed.png')
plt.clf()
