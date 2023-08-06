import numpy as np
import matplotlib.pyplot as plt
import random

def sigmoid( x ):
    return 1 / ( 1 + np.exp( -x ) )

def plotSigmoid( start=-10, end=10 ):
    sub_x = np.linspace( start, end )
    plt.plot( sub_x, random_linear( sigmoid( sub_x ) ) )
