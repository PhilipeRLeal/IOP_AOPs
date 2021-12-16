# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 09:21:44 2018

@author: Philipe_Leal
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 30 09:52:05 2018

@author: Philipe_Leal
"""


import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt


## reflectancias iniciais
## nm iniciais


def Remocao_do_continuo(Rrs_dict, nm_min, nm_max, Exemplo=False):
    """ Função que retorna um dicionário com o contínuo removido.
    
        Atributos de Entrada:
            Rrs_dict: dicionário contendo nm e Rrs (ou nm, Lw)...
            nm_min: comprimento de onda mínimo para extração do contínuo
            nm_max: comprimento de onda máximo para extração do contínuo
            
        Exemplo: retorna um exemplo com a chamada da função.
    
        Retorna: dicionário com keys='nm' e values com contínuo removido.
        
    """
    
    
    if Exemplo ==True:
        Exemplo()

    

    nm_interp = np.array([nm_min, nm_max+1])
    
    f = interpolate.interp1d(nm_interp, (Rrs_dict[nm_min], Rrs_dict[nm_max]))
    
    nm_desejado = np.arange(nm_min, nm_max)
    
    Reflectancia_nm_desejada = f(nm_desejado)
    Reflectancia_nm_desejada_dict = {}
    i = 0
    for N in nm_desejado:
        Reflectancia_nm_desejada_dict[N] = Reflectancia_nm_desejada[i]
        i+=1
    
    
    
    plt.figure(1)
    plt.clf()
    
    plt.plot(sorted(Rrs_dict.keys()), sorted(Rrs_dict.values()), 'bo')
    plt.plot(sorted(Rrs_dict.keys()), sorted(Rrs_dict.values()), 'b--')
    
    plt.plot(sorted(Reflectancia_nm_desejada_dict.keys()), 
             sorted(Reflectancia_nm_desejada_dict.values()), 'ro')
    
    for key in sorted(Reflectancia_nm_desejada_dict.keys()):
        Rrs_dict[key] -= Reflectancia_nm_desejada_dict[key]
        
    plt.plot(sorted(Rrs_dict.keys()),
              sorted(Rrs_dict.values()), 'k-')
    
    plt.legend(['original', 'original', 'interpolada', 'Contínuo Remov'], loc='best')
    plt.show()
    
    
    
        
    plt.figure(2)    
    plt.plot(sorted(Rrs_dict.keys()),
              sorted(Rrs_dict.values()), 'r-')
    plt.legend(["Contínuo Removido"])
    plt.show()

    return Rrs_dict



def Exemplo():
    
    
    Rrs = np.linspace(10, 20., 11)

    nm = np.arange(401, 411)
    
    print("nm de exemplo min: {0}, max: {0} ".format(401, 411))
    
    Rrs_dict = {}
    
    
    for i in range(len(nm)):
        Rrs_dict[nm[i]] = Rrs[i]
    
    print("Dicionário Original: ", Rrs_dict)
    print("\n\n")
    
    nm_interp = np.array([401, 411])
    
    f = interpolate.interp1d(nm_interp, (Rrs_dict[401], Rrs_dict[410]))
    
    nm_desejado = np.arange(401, 411)
    
    Reflectancia_nm_desejada = f(nm_desejado)
    Reflectancia_nm_desejada_dict = {}
    i = 0
    for N in nm_desejado:
        Reflectancia_nm_desejada_dict[N] = Reflectancia_nm_desejada[i]
        i+=1
    
    
    
    plt.figure(1)
    plt.clf()
    
    plt.plot(nm, sorted(Rrs_dict.values()), 'bo')
    plt.plot(nm, sorted(Rrs_dict.values()), 'b--')
    plt.plot(sorted(Reflectancia_nm_desejada_dict.keys()), 
             sorted(Reflectancia_nm_desejada_dict.values()), 'ro')
    
    for key in sorted(Reflectancia_nm_desejada_dict.keys()):
        Rrs_dict[key] -= Reflectancia_nm_desejada_dict[key]
        
    plt.plot(sorted(Rrs_dict.keys()),
              sorted(Rrs_dict.values()), 'k-')
    
    plt.legend(['original', 'original', 'interpolada', 'Contínuo Remov'], loc='best')
    plt.show()
    
    
    
        
    plt.figure(2)    
    plt.plot(sorted(Rrs_dict.keys()),
              sorted(Rrs_dict.values()), 'r-')
    plt.legend(["Contínuo Removido"])
    plt.show()
    
Exemplo()