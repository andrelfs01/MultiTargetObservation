from model import * 
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules  import TextElement

class AttributeElement(TextElement):
    def __init__(self, attr_name):
        '''
        Create a new text attribute element.

        Args:
            attr_name: The name of the attribute to extract from the model.

        Example return: "happy: 10"
        '''
        self.attr_name = attr_name


utility_element = AttributeElement("under_observation")

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5,
                 "text": agent.under_observation,
                 "text_color": "black"}
    return portrayal

grid = CanvasGrid(agent_portrayal, 25, 25, 600, 600)
server = ModularServer(CTOModel,
                       [grid,utility_element],
                       "World Model",
                       model_params={'N':24, 'O': 12, 'sensorRange': 15, 'target_speed': 0.5, 'active_prediction': False, 'a': 1.0, 'width': 25, 'height': 25})
server.port = 8521 # The default
server.launch()
