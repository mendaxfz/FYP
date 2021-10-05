import numpy as np

def simulateLIF(dt,I,C,gL,EL,VT,W,ker,Nk,I_bias,tref=0,pcm=False):
    '''Approximate LIF Neuron dynamics by Euler's method.

    Parameters
    ----------
    dt :number
       Euler time-step (ms)
       
    C,gL,EL,VT:number
        neuronal parameters
     
    I:1D NumPy array
        Input current (pA)
    
    W:1D NumPy array
        Synaptic Weight Strengths  - Connectivity Matrix
    
    ker:1D NumPy Array
        Current Kernal
    
    Ibias: NumPy Array
        Current Bias
    
    tref: number
        Refractory Period (ms)
    
    Returns
    -------
    V,Isyn :  NumPy array (mV), NumPy array (pA)
        Approximation for membrane potential computed by Euler's method.
    '''
    
    V=EL*np.ones((np.shape(I)[0],2*np.shape(I)[1])) #initialising V
    stim=np.zeros((np.shape(I)[0],2*np.shape(I)[1])) #initialising synaptic stimulus
    Isyn=np.zeros((np.shape(I)[0],2*np.shape(I)[1])) #initialising synaptic current 
    spike_instants = np.zeros(np.shape(I)[0]) #spike instants for neurons
    for n in range(0,np.shape(I)[1]-1):
        neuron_refractory = np.where(n>spike_instants+(tref/dt))
        if(np.size(neuron_refractory)>0):
            V[neuron_refractory,n+1] = V[neuron_refractory,n] + (dt/C)*(I[neuron_refractory,n]
                                            +Isyn[neuron_refractory,n] 
                                            +I_bias[neuron_refractory,n] 
                                            -gL*(V[neuron_refractory,n]-EL))
        else:
            V[:,n+1] = EL
        error_check=np.where(V[:,n+1]<EL)[0]
        if np.size(error_check)>0:V[error_check,n+1]=EL #Set to EL when V goes below EL
        check=np.where(V[:,n+1]>VT)[0]
        if np.size(check)>0:
            V[check,n+1]=EL
            V[check,n]=VT #Artificial Spike
            spike_instants[check] = n
            stim[check,n+1:n+1+Nk] += ker
            if(pcm): Isyn[:,n+1:] = 1000*np.matmul(pcm_weights(W),stim[:,n+1:])
            else: Isyn[:,n+1:] = 1000*np.matmul(W,stim[:,n+1:])
            
    return V,Isyn

