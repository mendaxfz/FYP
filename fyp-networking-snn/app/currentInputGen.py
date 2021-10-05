def currentInputGen(T,Ts,alpha,beta):
    """
    T: Temperature Input
    Ts: Set Temperature Point
    alpha,beta: constants
    
    returns: Current Input for Neuron 1(pA)
    """
    return (alpha + (beta*(T-Ts)))
