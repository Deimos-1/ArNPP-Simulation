## Main file, listens and executes user inputs 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from variables import *
from functions import *
from GUI import *
import sys

## IDEAS
# - make ++ and -- buttons
# pack with a better layout
# base defect on average temperature and hopefully make it less strong


print("#=============================#\n-> Simulation staring...")

## initiating the variables:
flux_values = initial_flux_values
v = Variables(**initial_variables)

## initiating the graph
print("-> Initiating the graph")
figure, ax = plt.subplots() ## create the space to draw the graph
line, = ax.plot(flux_values.keys(),flux_values.values(),'r') ## create the line to be displayed on fig
plt.xlabel('Time [0.1 s]')
plt.ylabel('Neutron Flux [%]')
plt.axis([-50,10, 0,150]) ## set the axes' scale

# target function for the animation
def graph(t):
    #print(f"Elapsed time: {t} [s]")
    
    if not running: ## Kills the graph if the program stopped
        plt.close()
        

    if not frozen:
        ## update variables
        global flux_values
        v.update()
        flux_values = axes_update(flux_values, v)
        line.set_data(list(flux_values.keys()),list(flux_values.values()))




print(F"-> Running the animation...\n#=============================#")
animation = FuncAnimation(figure, graph, interval=100, cache_frame_data=False)


gui = GUI(variable=v, fig=figure, anim=animation)
gui.start()        

## Lines to execute when program stops 
print("-> The Simulation has stopped. \n#=============================#")