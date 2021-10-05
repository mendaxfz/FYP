# FYP

### Introduction

With the advent of Neuromorphic Computing, and its subsequent growth in popularity and utility, the demand for computational solutions that extend beyond the Von-Neumann bottleneck is on the rise; we explore biologically inspired solution for spatial navigation inspired by C.Elegans. C.Elegans is considered as the fundamental organism in development biology and due to the simplicity of its mapped out genome, it is widely used as a foundation in experimental biology. It comprises of 302 neurons and approximately 5000 chemical synapses. The worm is capable of complex behaviours such as responding to external stimuli like heat and chemicals(chemotaxis). In this project we developed a spiking neural network(SNN) inspired by the thermotaxis behaviour of the worm to navigate physical environments based on tracking variables like heat or light intensity, which could find applicabiliy in real world robotic applications.

<img src="img/worm.png" height="300">

### Structure
Implementation of an end-to-end software and hardware based solution to simulate the thermotaxis behavior of the worm. For the software based solution, the worm engages in tracking thermal isotherms and in hardware this is simulated with light intensity tracking instead of temperature.

<img src="img/structure.png" height="400">

### Simulation

2D heatmap with temperatures ranging from 17-23C, with a setpoint temperature set to 20C. The worm manages to perform contour tracking(white line represents the trajectory) and navigating to the appropriate environment where it's survival chances are optimal. 
<img src="img/simulation.png" height="400">


