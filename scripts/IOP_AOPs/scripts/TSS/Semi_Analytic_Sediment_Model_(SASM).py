# -*- coding: utf-8 -*-
"""
Created on Tue May 29 17:56:27 2018

@author: Philipe Leal
"""
import math
class SASM():
    def __init__(self, Sensor):
        """ Semi-Analytic Sediment Model (SASM):
        
            Autor do algoritmo: Dorji et al. 2016
        
            Ref: Dorji P, Fearns P, Broomhall M. A Semi-Analytic Model for Estimating Total Suspended Sediment Con- centration in Turbid Coastal Waters of Northern Western Australia Using MODIS-Aqua 250mData. Remote Sensing. 2016; 8(7):556
        """
        self.Sensor = Sensor

    def Banda_por_sensor(self):
        """ Opcoes de sensores:
                'MODIS-Aqua'
                'Landsat-8 OLI'
                'World-View2'
        """
        if self.Sensor == 'MODIS-Aqua':
        
            self.Banda = 'banda 1'
        
        elif self.Sensor == 'Landsat-8 OLI':
            
            self.Banda = 'banda 4'
            
        elif self.Sensor == 'World-View2':
            
            self.Banda = 'red band'
        
        else:
            self.Banda = 'nao especificada'
        
        return ("Banda a ser utilizada para sensor {0}: {1}".format(self.Sensor, self.Banda))
    
    def referencia(self, modo='curto'):
        """ funcao que retorna a referência da funcao
        
            modo: como a funcao vai retornar a funcao: 
                  'longo': referencia completa
                  'curto' (padrão): referencia por citação
        """
        
        if modo == 'curto':
            Ref = 'Dorji et al. 2016'
        
        else:
            Ref = 'Ref: Dorji P, Fearns P, Broomhall M. A Semi-Analytic Model for Estimating Total Suspended Sediment Con- centration in Turbid Coastal Waters of Northern Western Australia Using MODIS-Aqua 250mData. Remote Sensing. 2016; 8(7):556'
        
        return Ref
    
    def Rrs_to_rrs_converter(self, Rrs_nm):
        """ converte Rrs em rrs com base no modelo de Mobley 1999
        
        """
        
        rrs_nm = Rrs_nm/(0.52 + 1.7*Rrs_nm)
        
        return rrs_nm
    
    def TSS(self, Rrs_nm):
        """ Retorna o valor de TSS g/m3 para um dado pixel
        
        
        """
        rrs_nm = self.Rrs_to_rrs_converter(Rrs_nm)
        
        g1, g2 = (0.084, 0.17)
        x = (-g1 + math.sqrt(g1 + 4*g2*rrs_nm))/2*g2
        
        if self.Sensor == 'MODIS-Aqua':
        
            TSS_var = 23.47*(x/1-x)/(1-0.69*(x/1-x))  
            
        elif self.Sensor == 'Landsat-8 OLI':
            TSS_var = 25.34*(x/1-x)/(1-0.69*(x/1-x))
            
        elif self.Sensor == 'World-View2':
            TSS_var = 26.37*(x/1-x)/(1-0.69*(x/1-x))
            
        return TSS_var
          
      
        
        