# -*- coding: utf-8 -*-
"""
Created on Wed May  9 17:31:44 2018

@author: Philipe Leal
"""
# calculos segundo Smith (1985)


import numpy as np
from math import *

# funcoes de transporte:

def funcao_calculo_h (U_10_m):
    
    h = 0.072*exp(-0.215)*U_10_m
    return h


def funcao_Pw(borate_alkalinity , total_alkalinity, valor_pH):
    
    Var_aH = aH(valor_pH)
    
    Pw = ((Var_aH**2)*(total_alkalinity - borate_alkalinity - (Var_aH/Kw)))/(alfa*(K1*Var_aH + (2*K1*K2)))
    
    return Pw

Pw = (funcao_Pw())



def aH(pH):
    aH = 10**(-pH)
    
    return aH

def Taxa_CO2(Concentracao_CO2, Concentracao_bicarbonato, pH):
    Var_aH = aH(pH)
    
    Taxa_CO2 = ((-Concentracao_CO2) * (((K12*Var_aH) + (K13*Kw))/Var_aH))
    + (Concentracao_bicarbonato) * (((K12*Var_aH) + (K13*Kw))/K1)
    
    return Taxa_CO2






# constantes de velocidade de reação. 

K12 = 0.037 # [1/s]
K1 = 10**(-6) # [mol/L]
K21 = K12/K1 # [L/mol/s]
K13= 8500 # [L/mol/s]
Kw = 10**(-14) # [1/((mol*L)**2)]
K31=K13*Kw/K1 #[1/s]
alfa = 3.0*(10**(-5))
K2 = 10 **(-9)
h = 0.003 # cm
D = 1.9*10**(-5) # para 25°C para CO2
K = D * alfa/(funcao_calculo_h(3.1))  # [mol/cm*s*atm]
n = 0.15 # varia conforme o vento, mas eh um valor adequado para superficies aquaticas
Pa = 340  # [uatm] # pressao parcial atmosferica do gas (CO2). Varia ao longo do tempo (séculos) e com a temperatura, 
	      #mas na escala de meses pode ser considerado constante






Array_pH =np.linspace(1, 13,num=13)

Concentracao_CO2=np.linspace(0, 10,num=10) # mols/L

Concentracao_bicarbonato=np.linspace(0, 10,num=10)

Array_Taxa_CO2 = []

for i in range(len(Array_pH)):
    for j in range(len(Concentracao_CO2)):
        for k in range(len(Concentracao_bicarbonato)):
            
            CO2 = Concentracao_CO2[k]
            Bicarbonato = Concentracao_bicarbonato[k]
            pH_i = Array_pH[k]

            
            Array_Taxa_CO2.append(Taxa_CO2(CO2,Bicarbonato, pH_i))
            
Array_Taxa_CO2 = np.array(Array_Taxa_CO2)

Array_Taxa_CO2 = Array_Taxa_CO2.reshape((np.size(Array_pH), np.size(Array_pH), np.size(Array_pH)))    
    
import matplotlib.pyplot as plt

for i in range(10):
    A_i = Array_Taxa_CO2[:,:,i]
    plt.figure()
    plt.subplot(4,4,i+1)
    plt.imshow(Array_Taxa_CO2[:,:,0], cmap='rainbow')
    plt.colorbar()
    plt.show('hold')
plt.show()    
        


def Fluxo ():
       
    F = K * (Pa - Pw)
