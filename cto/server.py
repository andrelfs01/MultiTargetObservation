from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from cto.agents import TargetAgent, ObserverAgent
from cto.model import Modelo as modelo


def cto_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is TargetAgent:
        portrayal["Shape"] = "cto/resources/sheep.png"
        # https://icons8.com/web-app/433/sheep
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is ObserverAgent:
        portrayal["Shape"] = "cto/resources/wolf.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = '1'
        portrayal["text_color"] = "White"

#    elif type(agent) is GrassPatch:
#        if agent.fully_grown:
#            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
#        else:
#            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
#        portrayal["Shape"] = "rect"
#        portrayal["Filled"] = "true"
#        portrayal["Layer"] = 0
#        portrayal["w"] = 1
#        portrayal["h"] = 1

    return portrayal

class UnderObservation(TextElement):
    '''
    Display a text count of how many under observation agents there are.
    '''

    def __init__(self):
        pass

    def render(self, model):
        return "Observed agents: " + str(model.targets_observed)


text_element = UnderObservation()
canvas_element = CanvasGrid(cto_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "Wolves", "Color": "#AA0000"},
                             {"Label": "Sheep", "Color": "#666666"}])

model_params = {#"grass": UserSettableParameter('checkbox', 'Grass Enabled', True),
                #"grass_regrowth_time": UserSettableParameter('slider', 'Grass Regrowth Time', 20, 1, 50),
                # "initial_sheep": UserSettableParameter('slider', 'Initial Sheep Population', 100, 10, 300),
                # "sheep_reproduce": UserSettableParameter('slider', 'Sheep Reproduction Rate', 0.04, 0.01, 1.0,
                #                                          0.01),
                # "initial_wolves": UserSettableParameter('slider', 'Initial Wolf Population', 50, 10, 300),
                # "wolf_reproduce": UserSettableParameter('slider', 'Wolf Reproduction Rate', 0.05, 0.01, 1.0,
                #                                         0.01,
                #                                         description="The rate at which wolf agents reproduce."),
                # "wolf_gain_from_food": UserSettableParameter('slider', 'Wolf Gain From Food Rate', 20, 1, 50),
                # "sheep_gain_from_food": UserSettableParameter('slider', 'Sheep Gain From Food', 4, 1, 10)
                
                "N": UserSettableParameter('slider', 'N', 1, 1, 30),
                "O": UserSettableParameter('slider', 'O', 1, 1, 96),
                "sensorRange": UserSettableParameter('slider', 'sensorRange', 5, 5, 25),
                "target_speed": UserSettableParameter('slider', 'target_speed', 0.1, 0.1, 2),
                "active_prediction": UserSettableParameter('checkbox', 'active_prediction', False),
                "a": UserSettableParameter('slider', 'a', 0.01, 0.01, 2)}

server = ModularServer(modelo, [canvas_element, chart_element, text_element], "CTO", model_params)
server.port = 8521
