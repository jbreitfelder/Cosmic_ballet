#########################################################
#
#   Title : Tools for the "cosmic ballet" application
#   Author: Joanne Breitfelder
#
#   Description :
#   This script gathers some functions
#   needed to solve the 3 bodies problem,
#   as well as to visualize the trajectories of
#   3 bodies in gravitational interaction.
#
#   How to use the application :
#   - All you need is a working python 2.7 distribution.
#   - Put Cosmic_ballet.py and CB_tools.py in your working directory
#   - Run Cosmic_ballet.py and enjoy !
#
#########################################################

import numpy as np
from scipy import *
import pylab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
import os
from matplotlib.collections import LineCollection
import matplotlib.colors as mcol


#########################################################
### Main functions (equation resolution and plotting)
#########################################################

def diff_eq(q, m):
    
    ##########
    ##  Differential equations for the 3 bodies problem
    ##  q is a position/velocity vector
    ##  m contains the bodies masses
    ##########
    
    c=3./2.
    G=9.86e-5 ## In the right units
    
    m1m2=((q[2]-q[0])*(q[2]-q[0])+(q[3]-q[1])*(q[3]-q[1]))**c
    m1m3=((q[4]-q[0])*(q[4]-q[0])+(q[5]-q[1])*(q[5]-q[1]))**c
    m2m3=((q[4]-q[2])*(q[4]-q[2])+(q[5]-q[3])*(q[5]-q[3]))**c

    qp = []
    
    qp.append(q[6])
    qp.append(q[7])
    
    qp.append(q[8])
    qp.append(q[9])
    qp.append(q[10])
    qp.append(q[11])
    
    qp.append(G*(m[1]*(q[2]-q[0])/m1m2+m[2]*(q[4]-q[0])/m1m3))
    qp.append(G*(m[1]*(q[3]-q[1])/m1m2+m[2]*(q[5]-q[1])/m1m3))
    
    qp.append(G*(m[0]*(q[0]-q[2])/m1m2+m[2]*(q[4]-q[2])/m2m3))
    qp.append(G*(m[0]*(q[1]-q[3])/m1m2+m[2]*(q[5]-q[3])/m2m3))
    
    qp.append(G*(m[0]*(q[0]-q[4])/m1m3+m[1]*(q[2]-q[4])/m2m3))
    qp.append(G*(m[0]*(q[1]-q[5])/m1m3+m[1]*(q[3]-q[5])/m2m3))

    qp = array(qp)
    return qp

def rKN(x, m, fx, n, dt):
    
    ##########
    ##  Runge-Kutta method in dimension n
    ##  x is a position/velocity vector
    ##  m contains the bodies masses
    ##  fx is the differential function to solve
    ##  dt is the step for the successive iterations 
    ##########
    
    k1, k2, k3, k4 = [], [], [], []
    xk = []
    for i in range(n):
        k1.append(fx(x, m)[i]*dt)
    for i in range(n):
        xk.append(x[i]+k1[i]*0.5) 
    for i in range(n):
        k2.append(fx(xk, m)[i]*dt)
    for i in range(n):
        xk[i] = x[i]+k2[i]*0.5
    for i in range(n):
        k3.append(fx(xk, m)[i]*dt)
    for i in range(n):
        xk[i] = x[i]+k3[i]
    for i in range(n):
        k4.append(fx(xk, m)[i]*dt)
    for i in range(n):
        x[i] = x[i]+(k1[i]+2*(k2[i]+k3[i])+k4[i])/6
    return x

def animation(q=[], params={}, save_files=False, directory=os.getcwd()):
    
    ##########
    ##  Plotting the simulation
    ##  q is a position/velocity vector
    ##  params contains a dictionnary of parameters
    ##  save_files allows to save all successive images
    ##  directory is the path to save the images
    ##########
    
    ## If needed, creation of the directory to save the files
    if not os.path.exists(directory):
        os.makedirs(directory)

    xmax, xmin, ymax, ymin = limits(q)
    number = step(params['r'], params['tfin'])[1]

    ## Initializing the plot
    fig = plt.figure(0, figsize=(12, 6))
    plt.clf()
    ax = fig.add_subplot(111)
    
    ## Setting the axis for the plot
    X = (xmax-xmin)/15
    Y = (ymax-ymin)/15
    ax.set_xlim(xmin-(xmax-xmin)/20, xmax+(xmax-xmin)/1.9)
    ax.set_ylim(ymin-(ymax-ymin)/10, ymax+(ymax-ymin)/15)
    ax.set_xlabel(r'$position\,(AU)$', fontsize='x-large')
    ax.set_ylabel(r'$position\,(AU)$', fontsize='x-large')
    
    ## Adding some annotations about the inital conditions
    ax.annotate('Initial conditions :', (xmax, ymax), (xmax+X, ymax-3*Y))
    ax.annotate('System ' + params['names'][1] + '-' + params['names'][2] + ' :', (xmax, ymax), (xmax+X, ymax-5*Y))
    if params['e']>0:
        ax.annotate('semi-major axis = ' + format_e(params['r']) + ' $UA$', (xmax, ymax), (xmax+X, ymax-6*Y))
    else:
        ax.annotate('distance = ' + format_e(params['r']) + r' $UA$', (xmax, ymax), (xmax+X, ymax-6*Y))
    ax.annotate(r'$e\,=\,$' + str(params['e']), (xmax, ymax), (xmax+X, ymax-7*Y))
    ax.annotate(params['names'][0] + ' mass = ' + format_e(params['mass'][0]) + r' $M_\oplus$', (xmax, ymax), (xmax+X, ymax-8*Y))
    ax.annotate(params['names'][1] + ' mass = ' + format_e(params['mass'][1]) + r' $M_\oplus$', (xmax, ymax), (xmax+X, ymax-9*Y))
    ax.annotate(params['names'][2] + ' :', (xmax, ymax), (xmax+(xmax-xmin)/15, ymax-11*(ymax-ymin)/15))
    ax.annotate(r'$x\,=\,$' + format_e(params['x3']) + r'$\,UA$', (xmax, ymax), (xmax+X, ymax-12*Y))
    ax.annotate(r'$y\,=\,$' + format_e(params['y3']) + r'$\,UA$', (xmax, ymax), (xmax+X, ymax-13*Y))
    ax.annotate(r'$V_x\,=\,$' + format_e(params['V3x']) + r'$\,UA/yr$', (xmax, ymax), (xmax+X, ymax-14*Y))
    ax.annotate(r'$V_y\,=\,$' + format_e(params['V3y']) + r'$\,UA/yr$', (xmax, ymax), (xmax+X, ymax-15*Y))
    ax.annotate('mass = ' + format_e(params['mass'][2]) + r' $M_\oplus$', (xmax, ymax), (xmax+X, ymax-16*Y))
    
    ## Creating a collection of points (with good marker size)
    ms = marker_size(params['mass'], 4., 8.)
    point1, = ax.plot([], [], '-o', color='orange', ms=ms[0], label=params['names'][0])
    point2, = ax.plot([], [], '-o', color='SteelBlue', ms=ms[1], label=params['names'][1])
    point3, = ax.plot([], [], '-o', color='red', ms=ms[2], label=params['names'][2])
    
    ## Opening the interactive mode
    plt.ion()
    plt.show()
        
    ## Plotting the actual data
    j=-1
    time=float(params['tfin'])/float(number)
    for i in range(number):
        del ax.collections[:]
        number_=float(number)/149
        number_=int(number_)
        if i%number_==0:
            j=j+1
            n=300
            
            if i <= n:              
                colormap_plot(np.array(q[0][0:i]), np.array(q[1][0:i]), Oranges_new())                
                colormap_plot(np.array(q[2][0:i]), np.array(q[3][0:i]), 'Blues')
                colormap_plot(np.array(q[4][0:i]), np.array(q[5][0:i]), Reds_new())
                
            else:
                colormap_plot(np.array(q[0][i-n:i]), np.array(q[1][i-n:i]), Oranges_new())
                colormap_plot(np.array(q[2][i-n:i]), np.array(q[3][i-n:i]), 'Blues')
                colormap_plot(np.array(q[4][i-n:i]), np.array(q[5][i-n:i]), Reds_new())
            
            point1.set_data(q[0][i], q[1][i])
            point2.set_data(q[2][i], q[3][i])
            point3.set_data(q[4][i], q[5][i])
            
            plt.legend(fontsize='medium', loc='upper right', ncol=2, frameon=False, numpoints=1)    
            plt.title('trajectories calculated over ' + str(int(time)) + ' years', fontsize='x-large')
          
            fig.canvas.draw()
            fig.canvas.update()
            fig.canvas.flush_events()
            
            if save_files:
                fig.savefig(directory+'/'+str(j)+'.png')
        
        time+=float(params['tfin'])/float(number)

def final_trajectories(q=[], params={}, save_files=False, directory=os.getcwd(), filename='final_trajectory.png'):
    
    ##########
    ##  Plotting the final trajectory
    ##  q is a position/velocity vector
    ##  params contains a dictionnary of parameters
    ##  save_files allows to save all successive images
    ##  directory is the path to save the images
    ##########
    
    ## If needed, creation of the directory to save the files
    if not os.path.exists(directory):
        os.makedirs(directory)

    xmax, xmin, ymax, ymin = limits(q)
    number = step(params['r'], params['tfin'])[1]

    ## Initializing the plot
    fig = plt.figure(1, figsize=(12, 6))
    plt.clf()
    ax = fig.add_subplot(111)
    
    ## Setting the axis for the plot
    X = (xmax-xmin)/15
    Y = (ymax-ymin)/15
    ax.set_xlim(xmin-(xmax-xmin)/20, xmax+(xmax-xmin)/1.9)
    ax.set_ylim(ymin-(ymax-ymin)/10, ymax+(ymax-ymin)/15)
    ax.set_xlabel(r'$position\,(AU)$', fontsize='x-large')
    ax.set_ylabel(r'$position\,(AU)$', fontsize='x-large')
    
    ## Adding some annotations about the inital conditions
    ax.annotate('Initial conditions :', (xmax, ymax), (xmax+X, ymax-3*Y))
    ax.annotate('System ' + params['names'][0] + '-' + params['names'][1] + ' :', (xmax, ymax), (xmax+X, ymax-5*Y))
    if params['e']>0:
        ax.annotate('semi-major axis = ' + format_e(params['r']) + ' $UA$', (xmax, ymax), (xmax+X, ymax-6*Y))
    else:
        ax.annotate('distance = ' + format_e(params['r']) + r' $UA$', (xmax, ymax), (xmax+X, ymax-6*Y))
    ax.annotate(r'$e\,=\,$' + str(params['e']), (xmax, ymax), (xmax+X, ymax-7*Y))
    ax.annotate(params['names'][0] + ' mass = ' + format_e(params['mass'][0]) + r' $M_\oplus$', (xmax, ymax), (xmax+X, ymax-8*Y))
    ax.annotate(params['names'][1] + ' mass = ' + format_e(params['mass'][1]) + r' $M_\oplus$', (xmax, ymax), (xmax+X, ymax-9*Y))
    ax.annotate(params['names'][2] + ' :', (xmax, ymax), (xmax+(xmax-xmin)/15, ymax-11*(ymax-ymin)/15))
    ax.annotate(r'$x\,=\,$' + format_e(params['x3']) + r'$\,UA$', (xmax, ymax), (xmax+X, ymax-12*Y))
    ax.annotate(r'$y\,=\,$' + format_e(params['y3']) + r'$\,UA$', (xmax, ymax), (xmax+X, ymax-13*Y))
    ax.annotate(r'$V_x\,=\,$' + format_e(params['V3x']) + r'$\,UA/yr$', (xmax, ymax), (xmax+X, ymax-14*Y))
    ax.annotate(r'$V_y\,=\,$' + format_e(params['V3y']) + r'$\,UA/yr$', (xmax, ymax), (xmax+X, ymax-15*Y))
    ax.annotate('mass = ' + format_e(params['mass'][2]) + r' $M_\oplus$', (xmax, ymax), (xmax+X, ymax-16*Y))
    
    ## Creating a collection of points (with good marker size)
    ms = marker_size(params['mass'], 4., 8.)
    point1, = ax.plot([], [], '-o', color='orange', ms=ms[0], label=params['names'][0])
    point2, = ax.plot([], [], '-o', color='SteelBlue', ms=ms[1], label=params['names'][1])
    point3, = ax.plot([], [], '-o', color='red', ms=ms[2], label=params['names'][2])
    
    ## Plotting the actual data
    colormap_plot(np.array(q[0]), np.array(q[1]), Oranges_new())                
    colormap_plot(np.array(q[2]), np.array(q[3]), 'Blues')
    colormap_plot(np.array(q[4]), np.array(q[5]), Reds_new())

    point1.set_data(q[0][number-1], q[1][number-1])
    point2.set_data(q[2][number-1], q[3][number-1])
    point3.set_data(q[4][number-1], q[5][number-1])
  
    plt.legend(fontsize='medium', loc='upper right', ncol=2, frameon=False, numpoints=1)    
    plt.title('trajectories calculated over ' + str(params['tfin']) + ' years', fontsize='x-large')
  
    if save_files:
        fig.savefig(directory+'/'+filename)


#########################################################
### Useful little tools
#########################################################

def format_e(n):
    
    ##########
    ##  Writes n in scientific notation, keeping only 2 decimal digits
    ##########
    
    a = '%E' % n
    return a.split('.')[0]+'.'+a.split('.')[1].split('E')[0][0:1]+'e'+a.split('E')[1]

def marker_size(m, ms_min=4, ms_max=8):
    
    ##########
    ##  Sets the size of the markers for the plot, depending on masses
    ##  m contains the bodies masses
    ##  ms_min is the minimal marker size, ms_mas the maximal
    ##########
    
    index_min, index_max = [], []
    index_middle = -1
    for i, value in enumerate(m):
        if value==min(m):index_min.append(i)
        if value==max(m):index_max.append(i)
        if min(m)<value<max(m):index_middle=i
    
    ms = [0, 0, 0]
    for i in index_min:ms[i] = ms_min
    for i in index_max:ms[i] = ms_max
    if index_middle>-1:
        ms[index_middle] = ms_min + (ms_max-ms_min)*((m[index_middle]-min(m))/(max(m)-min(m)))
    return ms

def step(r, tfin):
    
    ##########
    ##  Defines the step and the number of iterations
    ##  These parameters depend on the distance r between bodies
    ##  the 2 bodies orbiting around each other
    ##  tfin indicates the length of the simulation, in years
    ##########
    
    dt = 0.005*r**(1./3)
    number = int(tfin/dt)
    return dt, number

def step2(m, tfin):
    
    ##########
    ##  Defines the step and the number of iterations
    ##  These parameters depend on the minimal mass of the 3 bodies
    ##  m contains the bodies masses
    ##  tfin indicates the length of the simulation, in years
    ##########
    
    if min(m)<100.0:                ## Earth-like planets and big moons
        dt = 1.0/100
        number = int(tfin/dt)
    if min(m)<0.001:                ## Comets, small bodies
        dt = 1.0/500
        number = int(tfin/dt)
    else:                           ## Stars and big planets
        dt = 1.0/50
        number = int(tfin/dt)
    return dt, number


def limits(q):
    
    ##########
    ##  Defines the limits for the final plot
    ##  q is a position/velocity vector
    ##########
    
    xmax = max(max(q[0]), max(q[2]), max(q[4]))
    xmin = min(min(q[0]), min(q[2]), min(q[4]))
    ymax = max(max(q[1]), max(q[3]), max(q[5]))
    ymin = min(min(q[1]), min(q[3]), min(q[5]))
    return xmax, xmin, ymax, ymin

def colormap_plot(x, y, colormap):
    
    ##########
    ##  Plots a line with a color defined by a colormap
    ##  x, y are the variables to plot
    ##  colormap is a python colormap
    ##########
    
    t = np.linspace(0,1,x.shape[0])
    points = np.array([x, y]).transpose().reshape(-1,1,2)
    segs = np.concatenate([points[:-1],points[1:]],axis=1)
    lc = LineCollection(segs, cmap=plt.get_cmap(colormap))
    lc.set_array(t)
    plt.gca().add_collection(lc)
    return plt.gca().add_collection(lc)

def Oranges_new():
    
    ##########
    ##  Defining a new colormap which is a
    ##  subset of the Oranges colormap
    ##########
    
    lvTmp = np.linspace(0.0, 0.7, 100)
    cmTmp = plt.cm.Oranges(lvTmp)
    newOranges = mcol.ListedColormap(cmTmp)
    return newOranges

def Reds_new():
    
    ##########
    ##  Defining a new colormap which is a
    ##  subset of the Reds colormap
    ##########

    lvTmp = np.linspace(0.0, 0.7, 100)
    cmTmp = plt.cm.Reds(lvTmp)
    newReds = mcol.ListedColormap(cmTmp)
    return newReds

def error(answer, options):
    
    ##########
    ##  Returns an error message while the 
    ##  user enters wrong answers in command line
    ##  answer is the answer given by the user
    ##  options are the valid answers
    ##########
    
    error_messages = ['Hmm.. It seems that your answer is not valid..',
              'Do you want to break me? :o',
              'I am a machine, I have patience.',
              'What?? {}!? You must be kidding me!'.format(answer),
              'I just wanted to be your friend..',
              'Computer programs have feelings, you know?',
              ':o You are about to kill me!']
    i=0
    while(answer not in options):
        if i==len(error_messages):
            sys.exit('Aaaaah! You killed me!')
        else:
            print error_messages[i]
        answer = input('Make your choice and press enter.\n')
        i+=1
        print ''
    return answer

def number_frames(q):
#   --> plus vitesse elevee plus il faut garder de points
    return