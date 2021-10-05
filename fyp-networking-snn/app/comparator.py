import numpy as np
import matplotlib.pyplot as plt
import time
import simulateLIF
import currentKernal
from simulateLIF import simulateLIF
from currentKernal import currentKernal
from currentInputGen import currentInputGen
from pcm_weights import pcm_weights
from neuron_params import C, gL, EL, VT 

alpha = 3750 #pA
beta = 350 #pA/K
Numneurons = 2 

T = 300 #Simulation Time(ms)
dt=0.1
iter = int(T/dt)
# Obtaining kernel
kerlen = 80
tau1 = 15
tau2 = tau1/4
ker,Nk = currentKernal(dt,tau1,tau2,kerlen)

Ibias_positive = -2500 #pA
Ibias_negative = 8000 #pA
threshold_temp = 21 #celcius


def positive_comparator(T,Ts=threshold_temp,clone_to_pcm=False,tref=0):
	positive_comparator_weight = [[0,0],
                    			[7,0]]
	if(clone_to_pcm): positive_comparator_weight = pcm_weights(positive_comparator_weight)
	Iinp = currentInputGen(T,Ts,alpha,beta)*np.ones(iter)
	I1 = np.vstack((Iinp,np.zeros((Numneurons-1,np.shape(Iinp)[0]))))
	I_bias = np.zeros((Numneurons,iter))
	I_bias[1] = Ibias_positive #pA
	Vmem1,Isyn1 = simulateLIF(dt,I1,C,gL,EL,VT,positive_comparator_weight,ker,Nk,I_bias)
	spike_instants = np.where(Vmem1[1]==VT)
	if(np.size(spike_instants)>1):
		return True
	return False

def negative_comparator(T,Ts=threshold_temp,clone_to_pcm=False,tref=0):
	negative_comparator_weight = [[0,0],
                    			[-8,0]]
	if(clone_to_pcm): negative_comparator_weight = pcm_weights(negative_comparator_weight)
	Iinp = currentInputGen(T,Ts,alpha,beta)*np.ones(iter)
	I1 = np.vstack((Iinp,np.zeros((Numneurons-1,np.shape(Iinp)[0]))))
	I_bias = np.zeros((Numneurons,iter))
	I_bias[1] = Ibias_negative #pA
	Vmem1,Isyn1 = simulateLIF(dt,I1,C,gL,EL,VT,negative_comparator_weight,ker,Nk,I_bias)
	spike_instants = np.where(Vmem1[1]==VT)
	if(np.size(spike_instants)>1):
		return True
	return False
