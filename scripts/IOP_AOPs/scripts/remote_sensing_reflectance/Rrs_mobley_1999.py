# -*- coding: utf-8 -*-
"""
Created on Tue May 29 17:31:06 2018

@author: Philipe Leal
"""

def Rrs(Lu_nm, Lsky_nm, Ed_nm):
    """
        Lu_nm: Radiância ascendente abaixo da linha d'água
        Lsky_nm: Radiância do céu uniforme com velocidade do vento abaixo de 5m/s (Mobley, 1999)
        Ed_nm: Irradiância descendente acima d'água
        
        Refe MObley (1999):
            Mobley CD. Estimation of the remote-sensing reflectance from above-surface measurements. Appl
Opt. 1999; 38(36):7442–55. PMID: 18324298
            
    """
    Rrs = Lu_nm * 0.022 * Lsky_nm / Ed_nm
    
    return Rrs
    