def gradientDetect(dt,I,C,gL,EL,VT,ker,Nk,I_bias,tref,c,tau_a,d,w45,w46,w56_initial,w66):
    '''Gradient Detection 

    Parameters
    ----------
    dx :number
       Euler time-step (ms)
       
    C,gL,EL,VT:number
        neuronal parameters
     
    I:1D NumPy array
        Input current (pA)
    
    ker:1D NumPy Array
        Current Kernal
    
    Ibias: NumPy Array
        Current Bias
    
    tref: number
        Refractory Period (ms)
    
    c,tau_a,d: number
        Weight Adaptation Parameters
    
    w45,w46,w56_initial,w66: number
        Synaptic Strengths
    
    Returns
    -------
    V,Isyn,w56_weights :  NumPy array (mV), NumPy array (pA), NumPy array
        
    '''
    W_gdetect = np.zeros((3,3))
    W_gdetect[1,0] = w45 
    W_gdetect[2,0] = w46
    W_gdetect[2,1] = w56_initial
    W_gdetect[2,2] = w66
    w56_weights=[]
    V=EL*np.ones((np.shape(I)[0],2*np.shape(I)[1])) #initialising V
    stim=np.zeros((np.shape(I)[0],2*np.shape(I)[1])) #initialising synaptic stimulus
    Isyn=np.zeros((np.shape(I)[0],2*np.shape(I)[1])) #initialising synaptic current 
    spike_instants = np.zeros(np.shape(I)[0]) #spike instants for neurons
    Ibias = np.zeros((np.shape(I)[0],2*np.shape(I)[1])) #initialising bias current 
    Ibias[1] = I_bias #Setting Neuron 5 bias current
    spike_instants = np.zeros(np.shape(I)[0]) #spike instants for neurons
    for n in range(0,np.shape(I)[1]-1):
        neuron_refractory = np.where(n>spike_instants+(tref/dt))
        if(np.size(neuron_refractory)>0):
            V[neuron_refractory,n+1] = V[neuron_refractory,n] +(dt/C)*(I[neuron_refractory,n]
                                            +Isyn[neuron_refractory,n] 
                                            + Ibias[neuron_refractory,n]
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
            Isyn[:,n+1:] = 1000*np.matmul(W_gdetect,stim[:,n+1:])
            if(V[1][n]==VT):
                W_gdetect[2,1] = W_gdetect[2,1] + ((c/tau_a)+ ((d-W_gdetect[2,1])/tau_a))
            else:
                W_gdetect[2,1]+= ((d-W_gdetect[2,1])/tau_a)
        w56_weights.append(W_gdetect[2,1])
#         print(W_gdetect[2,1])
    return V,Isyn,w56_weights


#Parameters
c,d,tau_a,w45,w46,w56_initial,w66,I_bias = (8.365406866817512, -5.7172469083885336, 22.993129497338796, -1.868965162763052, 6.8399624018718255, -2.7420209289913564, -4.202035141656892, 3811.0644999147507)


