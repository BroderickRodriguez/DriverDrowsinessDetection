import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import numpy as np

#############################################
style.use('fivethirtyeight')

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True)
fig2 = plt.figure()
# fig, (ax1) = plt.subplots()
# data = pd.read_csv('data030721132432.csv')
# print( data["Frame"] )
def animate(i):
    data = pd.read_csv('dddExport.csv')
    frames = data['Frame']
    perclos = data['PERCLOS']
    ear = data['Ear Value']
    level = data['Alarm Level']
    
    ax1.cla()
    ax1.plot(frames, perclos)
    
    ax2.cla()
    ax2.plot(frames, ear, linewidth=1)
    
    ax3.cla()
    ax3.plot(frames, level)
    
    ax1.set_ylim([0,100])
    ax1.set_ylabel('PERCLOS')
    
    ax2.set_ylabel('EAR')
    ax2.set_ylim([0,1])
    
    ax3.set_ylim([0,5])
    ax3.set_ylabel('Level')
    ax3.set_xlabel('Frame')
############################################

def animate2(i):
    data = pd.read_csv('dddExport.csv')
    awake = data['awake'].iloc[-1]
    sdrowsy = data['sdrowsy'].iloc[-1]
    drowsy = data['drowsy'].iloc[-1]
    
    objects = ('Awake', 'Slightly Drowsy', 'Drowsy')
    y_pos = np.arange(len(objects))
    performance = [awake, sdrowsy, drowsy]
    plt.cla()
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Votes')
    plt.title('State Voting')
    
    
    
ani = FuncAnimation(fig, animate, interval=250)
ani2 = FuncAnimation(fig2, animate2, interval=250)
plt.tight_layout()
plt.show()
