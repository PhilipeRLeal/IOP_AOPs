# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 15:53:33 2018

@author: Philipe Leal
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


l = np.linspace(300, 700, 701-300, dtype=float) # wavelenths sampled

# vector of ratios Acdom/Anap
r = np.array([1/16., 1/8., 1/4., 1/2., 1., 2., 4., 8., 16.])


# vector of cdom 'slopes' [1/nm]
scdom = np.array([0.01, 0.001, 0.026])

 # vector of nap 'slopes' [1/nm]
snap = np.array([0.008, 0.001, 0.018])

r2 = np.zeros(shape=(np.size(scdom), np.size(snap), np.size(r)))
rmse = np.zeros(shape=(np.size(scdom), np.size(snap), np.size(r)))
beta= np.zeros(shape=(np.size(scdom), np.size(snap), np.size(r)))
s = np.zeros(shape=(np.size(scdom), np.size(snap), np.size(r)))

def func(a, A, S, B):
    
    Absorcao_espectral_modelo = (A * np.exp(-S * ((a) * np.exp(B))))
    
    return Absorcao_espectral_modelo


for i in range( 1):
    for j in range(1):
        for k in range(1):
            
            alfa = np.exp(-scdom[i] * l)
            
            beta = np.exp(-snap[j] * l)
            
            teta = r[k] * beta
            
            a = alfa + teta
            
            a = a/np.max(a)
            
            plt.plot(a)
            plt.show()
            
            popt, pcov = curve_fit(func, (l-299), a, sigma=None, method="trf", bounds= ([0., 0.0001, 0.0], ['inf', 'inf', 1.]))
            
            
            beta[i,j,k] = popt[2]
            s[i,j,k] = popt[1]

            
            r2[i,j,k] = np.sum(pcov)
            
            rmse[i,j,k] = np.mean(pcov)*100.
            
            print([i,j,k])  # print where you are
            print(rmse)
            print(r2)
            
            print("Melhor ajuste para os parâmetros: A, B, C: ", popt)

            plt.plot(a, func(a, *popt), 'r--', label='fit: a=%5.3f, S=%5.3f, B=%5.3f' % tuple(popt))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.show()
            
            perr = np.sqrt(np.mean(np.diag(pcov)))

            
            plt.imshow(pcov)
            plt.show()
            
     
#clear ans a_coeffs a_fit a_gof ft fo a;
