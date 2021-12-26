# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 18:23:49 2021

@author: coulo
"""
import numpy as np
import matplotlib.pyplot as pl

#bit_tested 0 to 7 where 0 is LSB

def bin_on_nbr_bits(nbr_bits,l):
    #print (l)
    liste=[]
    for e in l:
        e=e[2:]
        if nbr_bits>len(e):   
                e=(nbr_bits-len(e))*"0"+e
        if len(e)>nbr_bits:
            e=e[-nbr_bits:]
        liste.append(e)
    
    #print (liste)
    return liste
        
def generation(nbr_max,nbr_bits,nbr_sum):
    l_sum=[]
    
    for i in range (nbr_max+1):
        l_sum.append(bin(i+nbr_sum))
    
    return l_sum

def power(nbr_max,nbr_bits,nbr_sum):
    data_in=bin_on_nbr_bits(nbr_bits,generation(nbr_max,nbr_bits,0))
    data_out=bin_on_nbr_bits(nbr_bits,generation(nbr_max,nbr_bits,nbr_sum))
    
    ref=data_out[0]
    
    power=[]
    
    for i in range (len(data_out)):
        p=0
               
        for j in range (len(data_out[i])):
            
            if int(ref[-j])-int(data_out[i][-j])==1: # 1 to 0 power is 1
        
                p+=1
            if int(ref[-j])-int(data_out[i][-j])==-1: # 0 to 1 power is 2
                p+=2
        power.append(p)
    
    return (power)

def generation_class(nbr_max,nbr_bits,nbr_sum,bit_tested,key):
    data_in=bin_on_nbr_bits(nbr_bits,generation(nbr_max,nbr_bits,0))
    data_out=bin_on_nbr_bits(nbr_bits,generation(nbr_max,nbr_bits,nbr_sum))
    power_out=power(nbr_max,nbr_bits,key)
    
    listclass=[[[],[],[]],[[],[],[]]]
    
    #print (data_out,len(data_out))
    
    for i in range (len(data_out)):
        
        if data_out[i][-(bit_tested+1)]=="1":
            listclass[1][0].append(i)
            listclass[1][1].append(data_out[i])
            listclass[1][2].append(power_out[i])
            #print ("1",data_out[i])
            
        else: #if data_out[i][bit_tested]=="0":
            listclass[0][0].append(i)
            listclass[0][1].append(data_out[i])
            listclass[0][2].append(power_out[i])
            #print ("0",data_out[i])
                    
    
    return listclass

def average(l):
    s=sum(l)
    if len(l)==0:
        return False
    
    return s/len(l)

def average_class(nbr_max,nbr_bits,nbr_sum,bit_tested,key): #bit tested; 0=bit poids faible
    listclass=generation_class(nbr_max,nbr_bits,nbr_sum,bit_tested,key)
    
    print (listclass)
    average0=average(listclass[0][2])#power class 0
    
    average1=average(listclass[1][2])#power class 1
    
    if average0==False or average1==False:
        return 0
    return (abs(average0-average1))
            
def courbe(nbr_max,nbr_bits,bit_tested,key):
    print ("nbr_max=%d nbr_bits=%d bit_tested=%d key=%d" % (nbr_max,nbr_bits,bit_tested,key))
    x=np.linspace(0,nbr_max,nbr_max+1)
    #print (x)
    y=[]
    
    for i in range (nbr_max+1):
        y.append(average_class(nbr_max,nbr_bits,i,bit_tested,key))
    
    pl.plot(x,y,"+")
        
            
