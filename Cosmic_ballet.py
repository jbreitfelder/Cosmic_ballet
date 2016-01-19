#########################################################
#
#   Title : "Cosmic Ballet" application
#   Author: Joanne Breitfelder
#
#   Description :
#   This script contains the main source code
#   for the Cosmic Ballet application.
#   The application allows to see the trajectories and
#   interactions between 3 cosmic bodies, 2 of them being
#   orbiting around each other at the beginning.
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
import CB_tools
import time


#########################################################
### Some initialisation..
#########################################################

G=9.86e-5 ## In the right units
# Distances are in UA, time in year, masses in Earth masses
option1, option2, option3 = False, False, False
again=1


#########################################################
### Welcome message!
#########################################################

print ''
print ''
print '*******************************************************'
print '*                                                     *'
print '*           Welcome to Cosmic Ballet ! =)             *'
print '*                                                     *'
print '*******************************************************'
print ''
print ''
print 'This application has been developed by Joanne Breitfelder'
print 'For details or questions, please write to :'
print 'joanne.breitfelder - at - gmail.com'
print ''
print ''
print 'The Cosmic Ballet allows you to see the trajectories and'
print 'interactions between three cosmic bodies, two of them being'
print 'initially orbiting around each other.'
print ''
print ''
raw_input('Press enter to continue...')
print ''
print ''
print 'Great! Now let'+"'"+'s have fun!'
print 'To begin, please choose between the following options :'
print '    (1) See pre-registered trajectories'
general_mode = input('    (2) Enter you own initial parameters\n')
print ''

if general_mode not in [1, 2]:
    general_mode = CB_tools.error(general_mode, [1, 2])

if general_mode==1:
    print 'I prepared some interesting scenarios for you... Make your choice!'
    print '    (1) Betelgeuse decides to visit the Jupiter-Sun system'
    print '    (2) An Earth-like planet evolves in a binary system'
    scenario = input('    (3) Comet 67P enters the Earth-Moon system!\n')
    print ''
    
    if scenario not in [1, 2]:
        scenario = CB_tools.error(scenario, [1, 2, 3])

    if scenario==1:
        option1, option2, option3 = True, False, False
        
    elif scenario==2:
        option1, option2, option3 = False, True, False
        
    elif scenario==3:
        option1, option2, option3 = False, False, True

elif general_mode==2:
    print '*******************************************************'
    print '*                                                     *'
    print '*  Courageous choice :)                               *'
    print '*  Here are some details to help you...               *'
    print '*                                                     *'
    print '*                                                     *'
    print '*  1. Units :                                         *'
    print '*                                                     *'
    print '*    - Distances --> in AU                            *'
    print '*    - Masses    --> in Earth masses                  *'
    print '*    - Time      --> in years                         *'
    print '*    - Velocity  --> in AU/year                       *'
    print '*                                                     *'
    print '*                                                     *'
    print '*  2. Typical distances :                             *'
    print '*                                                     *'
    print '*    - distance Earth-Sun :   1 AU                    *'
    print '*    - distance Earth-Moon :  0.002 AU                *'
    print '*                                                     *'
    print '*                                                     *'
    print '*  3. Typical masses :                                *'
    print '*                                                     *'
    print '*    - Earth-like planet :    1 to 100 Me             *'
    print '*    - Jupiter-like planet :  100 to 10000 Me         *'
    print '*    - Sun :                  3.33e5 Me               *'
    print '*    - Super-giant star :     2e6 to 5e6 Me           *'
    print '*    - Red dwarf star :       2e4 to 2e5 Me           *'
    print '*    - Moon :                 0.01 Me                 *'
    print '*    - Halley'+"'"+'s Comet :       5e-11 Me                *'
    print '*                                                     *'
    print '*                                                     *'
    print '*  4. Suggestions :                                   *'
    print '*                                                     *'
    print '*    - Write the names between quotation marks        *'
    print '*    - Try first a short simulation (~1-10 years).    *'
    print '*      If you see that the trajectories converge,     *'
    print '*      then use a bigger value to see what happens!   *'
    print '*    - To begin, just look at the final trajectories. *'
    print '*      Change the parameters according to the result  *'
    print '*      and once you are happy, look at the whole      *'
    print '*      animation :)                                   *'
    print '*    - Don'+"'"+'t forget that you can save the plots !     *'
    print '*                                                     *'
    print '*******************************************************'
    print ''
    print 'Now, it'+"'"+'s your turn!! :)'
    raw_input('Press enter to continue...')
    print ''
    
    names, m = [], []
    print 'First, we consider two bodies orbiting around each other'
    names.append(str(input('   Name of the first one : ')))
    names.append(str(input('   Name of the second one : ')))
    m.append(input('   mass of the first one : '))
    m.append(input('   mass of the second one : '))
    e = input('   excentricity of the orbit : ')
    if e==0:
        r = input('   distance between them : ')
    else:
        r = input('   semi-major axis : ')
    print ''
    print 'A third body wants to be part of the fun!'
    names.append(str(input('   Name of this little guy : ')))
    m.append(input('   mass : '))
    x3 = input('   initial position on the x-axis : ')
    y3 = input('   initial position on the y-axis : ')
    while(x3==0 and y3==0):
        print '   Oops! '+str(names[0])+' is already here.. Choose a new position :'
        x3 = input('      initial position on the x-axis : ')
        y3 = input('      initial position on the y-axis : ')
    while(x3==r*(1-e) and y3==0):
        print '   Oops! '+str(names[1])+' is already here.. Choose a new position :'
        x3 = input('      initial position on the x-axis : ')
        y3 = input('      initial position on the y-axis : ')
    V3x = input('   initial velocity on the x-axis : ')
    V3y = input('   initial velocity on the y-axis : ')
    tfin = input('   Period covered by the simulation : ')
    print ''
    
print 'Oooh.. This is getting so interesting!!'
print 'How would you like to display the result?'
print '    (1) See the animation'
display = input('    (2) See the final trajectories only\n')
print ''

if display not in [1, 2]:
    display = CB_tools.error(display, [1, 2])

if display==1: animation, final_trajectories = True, False
elif display==2: animation, final_trajectories = False, True

#########################################################
### Parameters - to be changed by the user
#########################################################

## Pre-defined options :

if option1 :
    ## Betelgeuse visiting the Jupiter-Sun system
    names = ['Sun', 'Jupiter', 'Betelgeuse']
    r = 5.202
    e = 0
    m = [3.33e5, 3.1e2, 2.5e6]
    V3x, V3y = 2, 0
    x3, y3 = -6e1, 3e1
    tfin = 80.

if option2:
    ## Earth-like planet evolving in a binary system
    names = ['Star1', 'Star2', 'Planet']
    r = 10.5
    e = 0.5
    m = [4e5, 4e5, 1]
    V3x, V3y = 0, -8.7
    x3, y3 = 4, 0
    tfin = 80.

if option3 :
    ## Comet 67P entering the Earth-Moon system!
    names = ['Earth', 'Moon', 'Comet 67P']
    r = 0.00257
    e = 0.0549
    m = [1, 0.0123, 1.67e-12]
    V3x, V3y = 0.02, 0.005
    x3, y3 = -0.08, 0
    tfin = 15.0


#########################################################
### Dictionnary of parameters and position/velocity vector
#########################################################

while(again==1):
    params = {'names' : names,
        'r' : r,
        'e' : e,
        'mass' : m,
        'V3x' : V3x,
        'V3y' : V3y,
        'x3' : x3,
        'y3' : y3,
        'tfin' : tfin,
        'x1' : 0,
        'y1' : 0,
        'y2' : 0,
        'V1x' : 0,
        'V2x' : 0,
        'V1y' : sqrt((1+e)*G*(m[1]**2/(m[0]+m[1]))/(r*(1-e))),
        'V2y' : -sqrt((1+e)*G*(m[0]**2/(m[0]+m[1]))/(r*(1-e))),
        'x2' : r*(1-e)}
    
    q = [params['x1'], params['y1'], params['x2'], params['y2'],
         params['x3'], params['y3'], params['V1x'], params['V1y'],
         params['V2x'], params['V2y'], params['V3x'], params['V3y']]
    
    
    #########################################################
    ### Solving movement equations
    #########################################################
    
    ## Defining the step and number of iterations
    dt, number = CB_tools.step(params['r'], params['tfin'])
        
    q0, q1, q2, q3, q4, q5 = [], [], [], [], [], []
    V1, V2, V3 = [], [], []
    for i in range(number):
        q_new = CB_tools.rKN(q, params['mass'],
                        CB_tools.diff_eq, 12, dt) ## Equations solving
        q = q_new 
        q0.append(q[0])
        q1.append(q[1])
        q2.append(q[2])
        q3.append(q[3])
        q4.append(q[4])
        q5.append(q[5])
        V1.append(sqrt(q[6]**2+q[7]**2))
        V2.append(sqrt(q[6]**2+q[7]**2))
        V3.append(sqrt(q[6]**2+q[7]**2))
    
    q_all = [q0, q1, q2, q3, q4, q5]
    
    
    #########################################################
    ### Plotting the results and ask the user for new parameters
    #########################################################
       
    if animation :
        CB_tools.animation(q_all, params, save_files=False)
    if final_trajectories :
        print 'Do you want to save the graph?'
        print 'If yes, it will be saved in your current working directory.'
        print '    (1) Yes'
        save = input('    (2) No\n')
        print ''
        
        if save not in [1, 2]:
            save = CB_tools.error(save, [1, 2])
        
        if save==1: save_files=True
        elif save==2: save_files=False
        CB_tools.final_trajectories(q_all, params, save_files, directory=os.getcwd(), filename=names[0]+'-'+names[1]+'-'+names[2]+'.png')
    
    if general_mode==2:
        print 'Do you want to test new parameters?'
        print '    (1) Yes'
        again = input('    (2) No\n')
        print ''
        
        if again not in [1, 2]:
            again = CB_tools.error(again, [1, 2])
        if again==2:
            print 'We had fun!! See you soon!'
        elif again==1:
            print 'What parameter do you want to change?'
            print '    (1) mass of '+names[0]
            print '    (2) mass of '+names[1]
            print '    (3) mass of '+names[2]
            print '    (4) excentricity of the orbit'
            if params['e']==0:
                print '    (5) distance '+names[0]+'-'+names[1]
            else:
                print '    (5) semi-major axis'
            print '    (6) initial position of '+names[2]
            print '    (7) initial velocity of '+names[2]
            new_param = input('    (8) duration of the simulation\n')
            print ''
            if new_param not in [1, 2, 3, 4, 5, 6, 7, 8]:
                new_param = CB_tools.error(new_param, [1, 2, 3, 4, 5, 6, 7, 8])
            if new_param==1:
                m = [input('new mass : '), m[1], m[2]]
            elif new_param==2:
                m = [m[0], input('new mass : '), m[2]]
            elif new_param==3:
                m = [m[0], m[1], input('new mass : ')]
            elif new_param==4:
                e = input('new excentricity : ')
            elif new_param==5:
                r = input('new value : ')
            elif new_param==6:
                x3 = input('new initial position on the x-axis : ')
                y3 = input('new initial position on the y-axis : ')
                while(x3==0 and y3==0):
                    print ''
                    print '   Oops! '+str(names[0])+' is already here.. Choose a new position :'
                    x3 = input('   new initial position on the x-axis : ')
                    y3 = input('   new initial position on the y-axis : ')
                while(x3==r*(1-e) and y3==0):
                    print ''
                    print '   Oops! '+str(names[1])+' is already here.. Choose a new position :'
                    x3 = input('   new initial position on the x-axis : ')
                    y3 = input('   new initial position on the y-axis : ')
            elif new_param==7:
                V3x = input('new initial velocity on the x-axis : ')
                V3y = input('new initial velocity on the y-axis : ')
            elif new_param==8:
                tfin = input('new duration : ')
            
            print ''
            print 'How would you like to display the result?'
            print '    (1) See the animation'
            display = input('    (2) See the final trajectories only\n')
            print ''
            
            if display not in [1, 2]:
                display = CB_tools.error(display, [1, 2])
            
            if display==1: animation, final_trajectories = True, False
            elif display==2: animation, final_trajectories = False, True

    elif general_mode==1:
        again=0
        print 'We had fun!! See you soon!'
    
    
    
    
    
    