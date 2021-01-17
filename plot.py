import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style


#############################################
style.use('fivethirtyeight')
fig = plt.figure()


def animate(i):
    data = pd.read_csv('data070120211620.csv')
    x = data['Frame']
    y = data['PERCLOS']
    
    plt.cla()
    plt.plot(x, y)
    ax = plt.gca()
    ax.set_ylim([0,100])
    ax.set_ylabel('PERCLOS')
    ax.set_xlabel('Frame')
############################################

ani = FuncAnimation(plt.gcf(), animate, interval=250)
plt.tight_layout()
plt.show()
