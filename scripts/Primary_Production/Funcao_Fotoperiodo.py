# -*- coding: utf-8 -*-
"""
Created on Wed May  9 16:20:39 2018

@author: Philipe Leal
"""

def Fracao_horas_fotossinteticas(lat, Dia_juliano):
        
    pi=3.1415926535
    latr=(lat/180.)*pi
    date=(Dia_juliano/365.)*2*pi
    soldec=((0.39637-22.9133*cos(date)+4.02543*sin(date)-
             0.3872*cos(2*(date))+0.052*sin(2*(date)))*pi)/180.0
    rt=-tan(latr)*tan(soldec)
    DLength = (24*acos(rt))/pi
    
    DLength(rt>1) =0
    DLength(rt<=-1)=24
    
    DLength = DLength
    
    return DLength