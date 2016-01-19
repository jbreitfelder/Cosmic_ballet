# Cosmic ballet - Readme
# Author : Joanne Breitfelder
---
## Introduction
## How to run the application ?
## The initial conditions 
## Content of the Cosmic ballet repository :

---
## Introduction :

The "Cosmic ballet" application calculates for you the trajectories of three bodies in 
gravitational interaction, after you enter your own initial conditions. The code is
designed so that the two first bodies are orbiting around each other; this choice has
been made by the author to simplify the initial conditions setting. 
The application also allows you to see some predefined examples :

* A comet enters the Earth/Moon system
* Betelguese decides to visit the solar system (represented by Jupiter and the Sun)
* A planet tries to survive in a binary stellar system 

You can choose between two ways of looking at the trajectories :

* Displaying a plot of the final trajectories
* See an animation of the trajectories

After you visualize the trajectory you can change the value of an initial condition
and see how it affects the calculation. You can also save the final plot in your 
working directory.

---
## How to run the application ?

1. You need is a working python 2.7 distribution. If you don't have one, you can 
[download it](https://www.python.org/downloads/) from the Python web page.

2. Download the whole Cosmic Ballet repository and set it as your working directory.

3. Run the "Cosmic_ballet.py" script, see the instructions and enjoy!

4. This application is still under developement.. Please report any kind of bug 
to joanne.breitfelder - at - gmail.com :)

---
## The initial conditions :

It can seem a bit complicated and/or tricky to determine good initial conditions...
But don't panic! With a bit of practice you will become an expert. The easiest is
to begin with initial conditions relative to known bodies (e.g. the Sun, Jupiter, 
Betelgeuse, the Earth), and then modify the initial conditions step-by-step to get
exactly what you want or discover some really crazy unexpected trajectories. The
initial conditions are described bellow.

For the two bodies orbiting around each other :
    * Name of the first one (between quotation marks)
    * Name of the second one (between quotation marks)
    * mass of the first one
    * mass of the second one 
    * excentricity e of the orbit 
    * distance between them (if e=0) / semi-major axis (if e>0)
    
Note : the center of mass of this system is originally at the coordinates (0, 0), 
and it has a null initial velocity. 

Third body initial conditions :
    * Name (between quotation marks)
    * mass 
    * initial position on the x-axis 
    * initial position on the y-axis
    * initial velocity on the x-axis 
    * initial velocity on the y-axis 
    
Other initial condition :
    * Period covered by the simulation

Note : be careful! The longer the period, the longer the computation time! 
Begin with a low value (typically 5-10 years) and make it bigger if you see the code
runs fast enough. If you are dealing with small planets, satellites or comets, 5 years may 
already be quite a long period of time to see the evolution of the system.

### Units :
- Distances --> in AU 
- Masses    --> in Earth masses
- Time      --> in years
- Velocity  --> in AU/year

### Typical distances : 
- distance Earth-Sun :   1 AU
- distance Earth-Moon :  0.002 AU

### Typical masses :
- Earth-like planet :    1 to 100 Me
- Jupiter-like planet :  100 to 10000 Me
- Sun :                  3.33e5 Me
- Super-giant star :     2e6 to 5e6 Me
- Red dwarf star :       2e4 to 2e5 Me
- Moon :                 0.01 Me
- Halley's Comet :       5e-11 Me

---
## Content of the Cosmic ballet repository :
* "Cosmic_ballet.py" : This is the main python script of the application.
* "CB_tools.py" : This script contains a series of little tools used in the main code.
* The "Examples" Folder contains some examples of trajectories.
* The present Readme file









